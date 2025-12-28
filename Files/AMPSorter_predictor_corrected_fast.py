import os
import pandas as pd
import argparse
import torch
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from transformers import (
    GPT2Config,
    GPT2Tokenizer,
    GPT2ForSequenceClassification,
)

# =========================
#  SPEED OPTIMIZATIONS
# =========================
# Use TF32 and cuDNN autotune on A100 for much faster matmuls/convs
if torch.cuda.is_available():
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.benchmark = True


class PeptideDataset(Dataset):
    def __init__(self, data):
        # store sequences as a simple list for fast indexing
        self.texts = [seq for seq in data["Sequence"]]
        self.n_examples = len(self.texts)

    def __len__(self):
        return self.n_examples

    def __getitem__(self, item):
        # supports both int and slice (slice returns sublist)
        return {"text": self.texts[item]}


class Gpt2ClassificationCollator(object):
    def __init__(self, use_tokenizer, max_sequence_len=None):
        self.use_tokenizer = use_tokenizer
        self.max_sequence_len = (
            use_tokenizer.model_max_length
            if max_sequence_len is None
            else max_sequence_len
        )

    def __call__(self, sequences):
        texts = [sequence["text"] for sequence in sequences]

        # Tokenize a whole batch at once (already vectorized, this is OK)
        inputs = self.use_tokenizer(
            text=texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_sequence_len,
        )

        return inputs


def Prediction(model, dataloader, device):
    predictions_labels = []
    predictions_probs = []

    model.eval()

    # Evaluate data for one epoch
    for batch in tqdm(dataloader, total=len(dataloader)):
        # Move batch to GPU
        batch = {k: v.type(torch.long).to(device, non_blocking=True) for k, v in batch.items()}

        with torch.no_grad():
            outputs = model(**batch)
            logits = outputs[0]
            probs = F.softmax(logits, dim=1)
            predict_content = logits.argmax(axis=-1).flatten().tolist()
            predictions_labels += predict_content
            predictions_probs.extend(probs[:, 1].tolist())

    return predictions_labels, predictions_probs


def main():
    parser = argparse.ArgumentParser()

    # Use a single GPU by default (A100) – MUCH faster than DataParallel
    parser.add_argument(
        "--device",
        default="0",
        type=str,
        required=False,
        help="CUDA device id, e.g. '0'",
    )
    parser.add_argument(
        "--max_length", default=50, type=int, required=False, help="max_length"
    )
    parser.add_argument(
        "--batch_size", default=32, type=int, required=False, help="batch size"
    )

    # NEW: let user control DataLoader workers
    parser.add_argument(
        "--num_workers",
        type=int,
        default=0,
        required=False,
        help="Number of DataLoader workers",
    )

    parser.add_argument(
        "--raw_data_path",
        default="/Data/Sequence.csv",
        type=str,
        required=False,
        help="peptide dataset path",
    )
    parser.add_argument(
        "--model_path",
        default="/AMP_models/ProteoGPT/",
        type=str,
        required=False,
        help="pretrained model path",
    )
    parser.add_argument(
        "--classifier_path",
        default="/AMP_models/AmpSorter/best_model.pt",
        type=str,
        required=False,
        help="classifier model path",
    )
    parser.add_argument(
        "--output_path",
        default="/Data/Sequence_pred.csv",
        type=str,
        required=False,
        help="antimicrobial activity prediction results output path",
    )
    parser.add_argument(
        "--candidate_amp_path",
        default="/Data/Sequence_c_amps.csv",
        type=str,
        required=False,
        help="candidate amp path",
    )

    args = parser.parse_args()
    print("args:\n" + args.__repr__())

    # Set visible CUDA device
    os.environ["CUDA_VISIBLE_DEVICES"] = args.device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("using device:", device)

    max_length = args.max_length
    batch_size = args.batch_size
    raw_data_path = args.raw_data_path
    model_path = args.model_path
    classifier_path = args.classifier_path
    output_path = args.output_path
    candidate_amp_path = args.candidate_amp_path

    labels_ids = {"neg": 0, "pos": 1}
    n_labels = len(labels_ids)  # not used but kept for compatibility

    print("Loading tokenizer...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    # default to left padding
    tokenizer.padding_side = "left"
    # Define PAD Token = EOS Token = 50256
    tokenizer.pad_token = tokenizer.eos_token

    # Load model config from your fine-tuned directory
    model_config = GPT2Config.from_pretrained(model_path, num_labels=2)

    # Build model
    model = GPT2ForSequenceClassification(config=model_config)

    # Load classifier weights
    state_dict = torch.load(classifier_path, map_location=device)
    model.load_state_dict(state_dict, strict=False)

    # Resize tokenizer embeddings & set padding
    model.resize_token_embeddings(len(tokenizer))
    model.config.pad_token_id = model.config.eos_token_id

    # Move model to GPU
    model.to(device)
    model.eval()
    print("Model loaded to `%s`" % device)

    # Create data collator
    gpt2_classificaiton_collator = Gpt2ClassificationCollator(
        use_tokenizer=tokenizer, max_sequence_len=max_length
    )

    pepbase = pd.read_csv(raw_data_path)

    print("Dealing with Pepbase...")
    predicted_set = PeptideDataset(data=pepbase)
    print("Created `predicted_set` with %d examples!" % len(predicted_set))

    # Optimized DataLoader: workers, pinned memory, prefetch
    predicted_dataloader = DataLoader(
    predicted_set,
    batch_size=batch_size,
    shuffle=False,
    collate_fn=gpt2_classificaiton_collator,
    num_workers=args.num_workers,
    pin_memory=True,
    persistent_workers=True if args.num_workers > 0 else False,
    prefetch_factor=None
)

    print("Created `predicted_dataloader` with %d batches!" % len(predicted_dataloader))

    # Get predictions
    predictions_labels, predictions_probs = Prediction(model, predicted_dataloader, device)

    # Recover sequences
    peptide = predicted_dataloader.dataset[:]["text"]

    df = pd.DataFrame(
        {
            "ID": pepbase["ID"].tolist(),
            "Sequence": peptide,
            "Predicted Labels": predictions_labels,
            "Predicted Probabilities": predictions_probs,
        }
    )

    df_extracted = df[df["Predicted Labels"] == 1]
    df.sort_values(by="Predicted Probabilities", inplace=True, ascending=False)
    df_extracted = df_extracted.sort_values(
        by="Predicted Probabilities", ascending=False
    )

    df.to_csv(output_path, index=None)
    df_extracted.to_csv(candidate_amp_path, index=None)


if __name__ == "__main__":
    main()

# 🧬 MSA-Classifier Mask Pipeline for Antimicrobial Peptide Design

This repository provides a **Google Colab–ready pipeline** for the design, screening, and structural filtering of antimicrobial peptide (AMP) variants.

The workflow integrates:
- BLAST against AMPDB
- Multiple sequence alignment (MSA)–based conservation
- Mask enumeration and variant generation
- AMPSorter activity prediction
- NetSurfP-3.0 secondary structure prediction
- Q8-based SOV structural filtering

The pipeline is designed to run **entirely in Google Colab** and relies on **external tools and datasets stored in Google Drive**.

---

## IMPORTANT — Google Drive Is Required

This pipeline **expects specific files to be located in Google Drive** under: drive/My Drive/ 



If files are missing or paths differ, the pipeline will fail.

---

## 📁 Required Files and Where to Put Them

##### 1️⃣ Files INCLUDED in this GitHub repository

This repository includes a `Files/` directory containing all files required to run the pipeline.

Note :you must **manually upload the following files from `Files/` into your Google Drive root**: drive/My Drive/


| File | Description |
|----|----|
| `AMPDB_Master_Dataset.fasta` | AMPDB v1-Anti-microbial Peptide Database version 1 |
| `AMPSorter_predictor_corrected_fast.py` | AMPSorter inference script |
| `model.pt` | Trained AMPSorter PyTorch model |
| `SOV_refine.pl` | Perl script for Q8 SOV calculation |

✅ After upload, the paths **must be exactly**:

```text
/content/drive/My Drive/AMPDB_Master_Dataset.fasta
/content/drive/My Drive/AMPSorter_predictor_corrected_fast.py
/content/drive/My Drive/model.pt
/content/drive/My Drive/SOV_refine.pl



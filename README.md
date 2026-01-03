# 🧬 MSA-Classifier Mask Pipeline for Antimicrobial Peptide Design

This repository provides a **Google Colab–ready pipeline** for the design, screening, and structural filtering of antimicrobial peptide (AMP) variants.

The workflow integrates:
- BLAST against the AMPDBv1 database  
- Multiple sequence alignment (MSA)–based conservation analysis  
- Mask enumeration and variant generation  
- AMPSorter antimicrobial activity prediction  
- NetSurfP-3.0 secondary structure prediction  
- Q8-based SOV structural filtering  

The pipeline is designed to run **entirely in Google Colab** and relies on **external tools and datasets stored in Google Drive**.

---

## ⚠️ IMPORTANT — Google Drive Is Required

This pipeline **expects specific files to be located in Google Drive** under:

/content/drive/My Drive/

If files are missing or paths differ, the pipeline **will fail**.

---

## 📁 Required Files

### 1️⃣ Files Included in This GitHub Repository

This repository contains a `Files/` directory with all **core scripts and auxiliary resources** required to run the pipeline.

Due to licensing, file size, and redistribution restrictions, **some external tools and pretrained models are NOT included directly in this repository** and must be downloaded manually by the user.

---

### 2️⃣ External Tools & Models (Must Be Downloaded Separately)

#### 🔹 NetSurfP-3.0 (Required)

NetSurfP-3.0 is **not included** in this repository.

Users must download **NetSurfP-3.0 (Linux version)** directly from the official DTU website:

https://services.healthtech.dtu.dk/services/NetSurfP-3.0/

After download, upload the file:

netsurfp-3.0.Linux.zip

to the **root of Google Drive (`My Drive/`)**.

---

#### 🔹 ProteoGPT Pretrained Model (Required)

Due to its **large file size**, the **ProteoGPT pretrained model is not stored in this GitHub repository**.

Users must download the model from the following Google Drive link:

https://drive.google.com/drive/folders/19cOtRtZzU3JAglaRFLbc5M1aMmjYTUgV

After download, upload the **entire ProteoGPT directory** to:

My Drive/

⚠️ **Do not rename files or directories**, as the pipeline assumes fixed paths.

---

### 3️⃣ Additional External Tools (Included in `Files/`)

For user convenience, the following tools are included directly in the `Files/` directory:

- `tango_x86_64_release` — TANGO aggregation predictor  
- `Protein-Sol/` — Protein-Sol solubility predictor  

---

## 📄 Summary of Required Files in Google Drive

| File / Directory | Description |
|------------------|-------------|
| AMPDB_Master_Dataset.fasta | AMP reference database for BLAST |
| AMPSorter_predictor_corrected_fast.py | AMPSorter inference script |
| model.pt | Trained AMPSorter PyTorch model |
| requirements.txt | Python dependencies for AMPSorter |
| SOV_refine.pl | Perl script for Q8 SOV calculation |
| netsurfp-3.0.Linux.zip | NetSurfP-3.0 secondary structure predictor |
| ProteoGPT/ | Pretrained ProteoGPT model directory |
| tango_x86_64_release | TANGO aggregation predictor |
| Protein-Sol/ | Protein-Sol solubility predictor |

---

## ✅ Required Google Drive Paths (Must Match Exactly)

/content/drive/My Drive/AMPDB_Master_Dataset.fasta  
/content/drive/My Drive/AMPSorter_predictor_corrected_fast.py  
/content/drive/My Drive/model.pt  
/content/drive/My Drive/requirements.txt  
/content/drive/My Drive/SOV_refine.pl  
/content/drive/My Drive/netsurfp-3.0.Linux.zip  
/content/drive/My Drive/ProteoGPT/  
/content/drive/My Drive/tango_x86_64_release  
/content/drive/My Drive/Protein-Sol/  

---

## 🚀 Notes
- The pipeline is optimized for **Google Colab GPU environments**
- Users are strongly advised **not to modify directory names or paths**

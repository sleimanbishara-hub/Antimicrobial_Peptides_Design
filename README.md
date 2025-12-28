# 🧬 MSA-Classifier Mask Pipeline for Antimicrobial Peptide Design

This repository provides a **Google Colab–ready pipeline** for the design, screening, and structural filtering of antimicrobial peptide (AMP) variants.

The workflow integrates:
- BLAST against AMPDBv1 Database
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

## 📁 Required Files

##### 1️⃣ Files Included in this GitHub repository


This repository contains a `Files/` directory with all core scripts and auxiliary resources required to run the pipeline.

Due to licensing and redistribution restrictions, **NetSurfP-3.0 is not included in this repository**.  
Users must download **NetSurfP-3.0 (Linux version)** directly from the official website:

https://services.healthtech.dtu.dk/services/NetSurfP-3.0/

After download, the file **`netsurfp-3.0.Linux.zip`** should be uploaded manually to the root of the user’s Google Drive (`My Drive/`).

In addition, the `Files/` directory includes other external tools provided for user convenience, such as:
- `tango_x86_64_release`
- `Protein-Sol/`

Before running the pipeline in Google Colab, users should ensure that:
- All contents of the `Files/` directory are uploaded to `My Drive/`
- `netsurfp-3.0.Linux.zip` (downloaded separately) is also uploaded to `My Drive/`


| File | Description |
|------|------------|
| AMPDB_Master_Dataset.fasta | AMP reference database for BLAST |
| AMPSorter_predictor_corrected_fast.py | AMPSorter inference script |
| model.pt | Trained AMPSorter PyTorch model |
| requirements.txt | Python dependencies required for AMPSorter |
| SOV_refine.pl | Perl script for Q8 SOV calculation |
| netsurfp-3.0.Linux.zip | NetSurfP-3.0 secondary structure predictor |
| tango_x86_64_release | TANGO aggregation predictor  |
| Protein-Sol/ | Protein-Sol solubility predictor |


✅ After upload, the paths **must be exactly**:

```text
/content/drive/My Drive/AMPDB_Master_Dataset.fasta
/content/drive/My Drive/AMPSorter_predictor_corrected_fast.py
/content/drive/My Drive/model.pt
/content/drive/My Drive/SOV_refine.pl
/content/drive/My Drive/requirements.txt
/content/drive/My Drive/netsurfp-3.0.Linux.zip
/content/drive/My Drive/tango_x86_64_release
/content/drive/My Drive/Protein-Sol/

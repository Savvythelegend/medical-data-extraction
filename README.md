# medical-data-extraction
An OCR-based system to extract structured patient and prescription information from medical documents.
![alt text](image.png)
[Pipeline](https://excalidraw.com/#json=Dvm9ywHFl9tryX5qQ-MlZ,iKWRni68K9onmD_TV11IcA)
<!--
README for the Medical Data Extraction project.
This file preserves the original pipeline link while providing
expanded documentation, badges/icons, install and usage instructions.
-->

# Medical Data Extraction

An OCR-based system to extract structured patient and prescription information from medical documents (PDFs, images). The project combines PDF→image conversion, image preprocessing, Tesseract OCR and custom parser logic to return structured JSON for downstream applications.

<!-- BADGES -->
[![Last Commit](https://img.shields.io/github/last-commit/Savvythelegend/medical-data-extraction?style=flat-square)](https://github.com/Savvythelegend/medical-data-extraction/commits)
[![Top Language](https://img.shields.io/github/languages/top/Savvythelegend/medical-data-extraction?style=flat-square)](https://github.com/Savvythelegend/medical-data-extraction)
[![Languages Count](https://img.shields.io/github/languages/count/Savvythelegend/medical-data-extraction?style=flat-square)](https://github.com/Savvythelegend/medical-data-extraction)

---

## Quick links
- Project on GitHub: https://github.com/Savvythelegend/medical-data-extraction

---

## Table of contents

- [medical-data-extraction](#medical-data-extraction)
- [Medical Data Extraction](#medical-data-extraction-1)
  - [Quick links](#quick-links)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation (Python \& project deps)](#installation-python--project-deps)
  - [Usage](#usage)
  - [Project structure](#project-structure)
  - [Testing](#testing)
  - [Development tips](#development-tips)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)

---

## Overview

This repository implements an end-to-end OCR pipeline focused on medical documents. It extracts text from PDFs/images and parses the result into structured fields (for example: patient name, age, medication, dosage). The core components are:

- PDF → image conversion (poppler / `pdftoppm`)
- Image preprocessing (contrast, denoise, binarization)
- Tesseract OCR integration (`pytesseract`)
- Parsers for prescriptions and patient details

The code is designed so the OCR step is only executed when required; importing modules for testing or static analysis will not fail if system binaries are absent.

## Features

- Convert multipage PDFs into images and run OCR per page
- Preprocessing hooks to improve OCR accuracy
- Prescription parser that extracts medication names and dosages
- Patient-details parser that extracts name, age, gender, address, etc.
- Helpful runtime checks and clear install instructions when required system binaries are missing

---

## Prerequisites

- Python 3.10+ (this repo uses pyproject/uv; adjust if you use another toolchain)
- System binaries (required for full OCR):
	- Tesseract OCR (tesseract)
	- Poppler utilities (pdftoppm)

Install system packages (examples):

Debian / Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip tesseract-ocr poppler-utils
```

Fedora / RHEL:

```bash
sudo dnf install -y python3 python3-venv python3-pip tesseract poppler-utils
```

macOS (Homebrew):

```bash
brew install tesseract poppler
```

Windows:

- Install Tesseract from: https://github.com/tesseract-ocr/tesseract
- Add the installed `tesseract.exe` to your PATH
- Install Poppler (e.g., use https://github.com/oschwartz10612/poppler-windows) and add `pdftoppm.exe` to your PATH

Note: Installing these system binaries is required to run the OCR end-to-end. Unit tests that only import modules (and don't call `extract()`) will work without them.

---

## Installation (Python & project deps)

Create a virtual environment and install Python deps. This repo uses `uv` in examples, but standard venv + pip works too.

Using venv + pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt   # if present
# or use the pyproject tooling (uv/poetry/pipx) as configured in this repo
```

Using uv (if you use the project's recommended workflow):

```bash
uv sync --all-extras --dev
```

---

## Usage

Run the OCR extractor directly (simple example). Make sure the system binaries are installed and your venv is active.

```bash
python src/ocr/extractor.py
```

Or call the `extract()` function from Python:

```py
from src.ocr.extractor import extract

data = extract('/path/to/document.pdf', 'prescription')
print(data)
```

Docker (example): build and run a container that has Tesseract/Poppler installed.

```bash
docker build -t medical-ocr:latest .
docker run --rm -v $(pwd)/src/resources:/app/resources medical-ocr:latest python src/ocr/extractor.py
```

Notes on logs and debugging:
- The extractor provides clear runtime errors when `tesseract` or `pdftoppm` are not found. Follow the install instructions above if you see those errors.

---

## Project structure

Keep the pipeline diagram in the original README. The project layout (top-level) is:

```
medical-data-extraction/
├── Makefile
├── README.md
├── readme-ai.md
├── docker/
├── frontend/
├── notebooks/
├── pyproject.toml
├── src/
│   ├── api/
│   ├── db/
│   ├── ocr/
│   ├── resources/
│   ├── tests/
│   └── utils/
```

Key files under `src/ocr/`:

- `extractor.py` — main entrypoint for converting PDFs to images, preprocessing, running Tesseract, and dispatching to parsers
- `util.py` — image preprocessing utilities
- `prescription_parser.py` — parser for prescriptions
- `patient_details_parser.py` — parser for patient demographics
- `generic_parser.py` — shared parsing helpers

Original pipeline (kept from project root):

Pipeline diagram: https://excalidraw.com/#json=Dvm9ywHFl9tryX5qQ-MlZ,iKWRni68K9onmD_TV11IcA

---

## Testing

Run unit tests (pytest) inside the project (vague locations because your project contains tests under `src/tests`):

```bash
uv run pytest src/tests/  # if you use uv
# or
pytest src/tests/
```

Note: Tests that exercise the OCR pipeline will require system binaries. You can skip heavy integration tests by passing markers or using pytest -k to run unit-only tests.

---

## Development tips

- Strip notebook outputs before committing (use `nbstripout` or a pre-commit hook) to keep the repo small and avoid merge noise.
- When adding new parsers, create unit tests that feed representative text into your parser class rather than depending on full OCR output. That isolates parsing logic from OCR variations.
- Use the branch naming convention like `feature/ocr-<short-desc>` or `fix/<issue>`.

Example Git workflow (already used in this repo):

```bash
git checkout -b feature/ocr-improvements
git add -A
git commit -m "feat(ocr): improve preprocessing and parser accuracy"
git push -u origin feature/ocr-improvements
```

---

## Roadmap

- Improve parser accuracy via training lists and fuzzy matching
- Add CI steps to run linting and tests
- Add a lightweight web UI to upload PDFs and show parsed results

---

## Contributing

1. Fork the repo
2. Create a topic branch
3. Add tests and changes
4. Submit a pull request

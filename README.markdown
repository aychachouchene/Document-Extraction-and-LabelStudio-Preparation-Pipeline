# Document Extraction and LabelStudio Preparation Pipeline

Welcome to the **LABELSTUDIO_PIPELINE** project! This tool automates the conversion and preparation of PDF and Excel files for annotation in LabelStudio, streamlining workflows for data annotation tasks in machine learning and document processing pipelines.

## Overview

In today’s data-driven world, extracting meaningful information from diverse document formats (PDFs, Excel files) and preparing them for annotation is a critical yet time-consuming challenge. This project addresses that need by providing a robust, end-to-end pipeline that converts, extracts, and formats data into LabelStudio-compatible tasks. Built with precision and scalability in mind, it leverages advanced libraries and custom logic to handle complex document structures, making it an invaluable asset for AI-driven document analysis projects.

Developed by a skilled engineer with expertise in Python, OCR, and data processing, this project showcases proficiency in automation, file manipulation, and integration with annotation tools—skills highly sought after in the tech industry.

## Features

- **Multi-Format Support**: Handles both PDF and Excel files, converting them into a unified workflow.
- **OCR Integration**: Utilizes PaddleOCR for accurate text and bounding box extraction from images.
- **Image Conversion**: Converts PDFs to high-resolution images (JPG/PNG) with customizable DPI settings.
- **LabelStudio Readiness**: Generates JSON tasks with bounding boxes and transcriptions tailored for LabelStudio annotation.
- **Modular Design**: Organized into extractors, converters, processors, and utils for maintainable and extensible code.
- **Error Handling**: Robust exception management ensures reliable processing of large document sets.

## Project Structure

```
LABELSTUDIO_PIPELINE/
├── converters/
│   ├── excel_to_pdf.py
│   ├── pdf_to_images.py
├── extractors/
│   ├── excel_extractor.py
│   ├── pdf_extractor.py
├── processors/
│   ├── labelstudio_preparer.py
├── utils/
│   ├── json_loader.py
│   ├── save_json.py
├── data/
│   ├── input/              # Original PDF or Excel files
│   ├── output/
│   │   ├── ocr_json/       # Extracted bounding boxes in JSON
│   │   ├── images/         # Generated images from PDFs
│   │   ├── labelstudio/    # Final LabelStudio task files
├── .gitignore
├── README.md
├── requirements.txt
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aychachouchene/Document-Extraction-and-LabelStudio-Preparation-Pipeline.git
   cd LABELSTUDIO_PIPELINE
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.8+ installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   **Note**: Dependencies include `pdf2image`, `pdfplumber`, `PaddleOCR`, `pandas`, `pillow`, and `pywin32` (for Excel-to-PDF conversion on Windows).

3. **Set Up Poppler**:
   For `pdf2image` to work, install Poppler (e.g., via `conda install -c conda-forge poppler` or download from [poppler official site](https://poppler.freedesktop.org/)).

4. **Verify Setup**:
   Test the installation by running the script with a sample file:
   ```bash
   python main.py data/input/sample.pdf
   ```

## Usage

### Running the Pipeline
The script processes individual files or entire folders. Use the following command:
```bash
python main.py <path>
```
- `<path>`: Path to a single PDF/Excel file or a directory containing such files (defaults to `data/input`).

### Example
Process a folder of documents:
```bash
python main.py data/input
```
This will:
- Convert Excel files to PDFs with text wrapping and auto-fit adjustments.
- Extract bounding boxes and text using OCR or PDF parsing.
- Generate images and create LabelStudio tasks in `data/output/labelstudio`.

### Output
- **OCR JSON**: Bounding box data in `data/output/ocr_json/`.
- **Images**: High-resolution images in `data/output/images/`.
- **LabelStudio Tasks**: Annotation-ready JSON files in `data/output/labelstudio/`.

## Skills Demonstrated
This project reflects a strong command of:
- **Python Programming**: Efficient use of `argparse`, `pathlib`, and modular code design.
- **Data Processing**: Expertise in handling PDFs and Excel files with `pdfplumber`, `pandas`, and `win32com`.
- **OCR Technology**: Integration of PaddleOCR for multilingual text extraction.
- **Automation**: End-to-end pipeline for document preparation and annotation.
- **Problem-Solving**: Custom logic for merging numeric tokens and handling diverse document layouts.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature-name"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

Please ensure code follows PEP 8 standards and includes tests where applicable.

## License
This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For questions or collaboration, reach out at [aycha.chouchene@etudiant-enit.utm.tn](mailto:aycha.chouchene@etudiant-enit.utm.tn)
 or [choucheneaycha03@gmail.com](mailto:choucheneaycha03@gmail.com).
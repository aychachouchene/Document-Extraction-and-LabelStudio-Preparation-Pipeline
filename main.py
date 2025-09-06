import argparse
import json
from pathlib import Path
from PIL import Image

#from extractors.excel_extractor import extract_excel_words_boxes
from extractors.pdf_extractor import extract_pdf_words_boxes
from converters.excel_to_pdf import excel_to_pdf
from converters.pdf_to_images import convert_pdf_to_images
from utils.json_loader import load_tokens_per_page
from processors.labelstudio_preparer import create_labelstudio_tasks
from utils.save_json import save_to_json

# ------------------ PARAMÈTRES ------------------

PDF_DPI = 300
PDF_WIDTH = 595.2756   # A4
PDF_HEIGHT = 841.8898
IMG_FORMAT = "jpg"

# Chemins racines des données
DATA_DIR = Path("data")
INPUT_DIR = DATA_DIR / "input"                   # ← Fichiers PDF ou Excel originaux
OCR_DIR = DATA_DIR / "output/ocr_json"           # ← Résultats d'extraction en JSON (bboxes)
IMG_DIR = DATA_DIR / "output/images"             # ← Images générées depuis PDF
TASKS_DIR = DATA_DIR / "output/labelstudio"      # ← Fichiers finaux pour Label Studio

for d in [OCR_DIR, IMG_DIR, TASKS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------


def process_file(file_path: Path):
    ext = file_path.suffix.lower()
    file_stem = file_path.stem

    if ext == ".xlsx":
        # 🔹 Étape 1 : Excel vers PDF sélectionnable
        temp_dir = DATA_DIR / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = temp_dir / f"{file_stem}.pdf"
        excel_to_pdf(file_path, pdf_path)

        # 🔹 Étape 2 : Extraction des bboxes depuis l'Excel
        bboxes = extract_pdf_words_boxes(pdf_path)
        json_path = OCR_DIR / f"{file_stem}.json"
        save_to_json(bboxes, json_path)

    elif ext == ".pdf":
        # 🔹 Étape 1 : Extraction des bboxes depuis le PDF
        bboxes = extract_pdf_words_boxes(file_path)
        json_path = OCR_DIR / f"{file_stem}.json"
        save_to_json(bboxes, json_path)

    else:
        print(f"[ERREUR] Format non supporté : {ext}")
        return

    # 🔹 Étape 3 : Conversion du PDF en images
    pdf_input_path = pdf_path if ext == ".xlsx" else file_path
    task_dir = TASKS_DIR / file_stem
    task_dir.mkdir(parents=True, exist_ok=True)

    image_paths = convert_pdf_to_images(pdf_input_path, task_dir, dpi=PDF_DPI, img_format=IMG_FORMAT)
    # 🔹 Étape 4 : Chargement OCR
    ocr_pages = load_tokens_per_page(json_path)

    # 🔹 Étape 5 : Génération des tâches Label Studio
    tasks = create_labelstudio_tasks(image_paths, ocr_pages, pdf_width=PDF_WIDTH, pdf_height=PDF_HEIGHT)
    task_output_path = task_dir / f"{file_stem}_tasks.json"
    save_to_json(tasks, task_output_path)

    #print(f"\n✅ {file_path.name} traité avec succès. Tâches LS sauvegardées dans {task_output_path}")


def process_folder(input_folder: Path):
    for file_path in input_folder.glob("*"):
        if file_path.suffix.lower() in [".pdf", ".xlsx"]:
            process_file(file_path)


def main():
    parser = argparse.ArgumentParser(description="Pipeline complet : extraction -> Label Studio")
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default="data/input",
        help="Chemin vers un fichier ou dossier (par défaut: data/input)"
    )
    args = parser.parse_args()

    input_path = Path(args.path).resolve()

    if input_path.is_file():
        process_file(input_path)
    elif input_path.is_dir():
        process_folder(input_path)
    else:
        print("[ERREUR] Chemin invalide.")



if __name__ == "__main__":
    main()

import os

from extractors.pdf_extractor import extract_pdf_words_boxes
from utils.save_json import save_to_json



def process_pdf_folder(pdf_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            result = extract_pdf_words_boxes(pdf_path)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.json")
            save_to_json(result, output_file)
            print(f"[INFO] {filename} traité et sauvegardé dans {output_file}")
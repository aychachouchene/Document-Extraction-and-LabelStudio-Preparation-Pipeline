import os
import json
from pathlib import Path
from paddleocr import PaddleOCR
from PIL import Image
from pdf2image import convert_from_path
import traceback

def convert_pdf_to_images(pdf_path, out_dir, dpi=300, img_format="jpg"):
    pdf_path = Path(pdf_path)
    out_dir = Path(out_dir)
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    image_paths = []
    out_dir.mkdir(parents=True, exist_ok=True)
    pil_format = "JPEG" if img_format.lower() in ("jpg", "jpeg") else "PNG"

    for idx, page in enumerate(pages):
        img_name = f"{pdf_path.stem}_page-{idx+1:04d}.{img_format}"
        img_path = out_dir / img_name
        page.save(str(img_path), pil_format)
        image_paths.append(img_path)
        print(f"[INFO] {pdf_path.name} - Page {idx+1} convertie -> {img_path.name}")

    return image_paths

def process_images_in_folder(folder_path):
    ocr = PaddleOCR(use_textline_orientation=True, lang='fr')
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            print(f"\n📂 Traitement de l'image : {filename}")
            img = Image.open(image_path)
            img_width, img_height = img.size
            try:
                results = ocr.predict(image_path)
            except Exception as e:
                print(f"[ERREUR] OCR sur {filename} : {e}")
                traceback.print_exc()
                continue
            bboxes = []
            for line in results[0]:
                box = line[0]
                text = line[1][0]
                conf = line[1][1]
                x_coords = [pt[0] for pt in box]
                y_coords = [pt[1] for pt in box]
                x_min = min(x_coords)
                y_min = min(y_coords)
                x_max = max(x_coords)
                y_max = max(y_coords)
                bbox_dict = {
                    "x0": int(x_min),
                    "y0": int(y_min),
                    "x1": int(x_max),
                    "y1": int(y_max),
                    "text": text,
                    "conf": conf
                }
                bboxes.append(bbox_dict)
            output_json_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.json")
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(bboxes, f, ensure_ascii=False, indent=2)
            print(f"✅ JSON généré : {output_json_path}")
            print(f"[INFO] OCR terminé pour {filename}")

if __name__ == "__main__":
    input_path = input("Chemin du PDF ou dossier d'images : ").strip()
    if not input_path:
        print("[ERREUR] Chemin non fourni.")
        exit()

    if input_path.lower().endswith(".pdf"):
        pdf_path = Path(input_path)
        images_dir = pdf_path.parent / f"{pdf_path.stem}_images"
        convert_pdf_to_images(pdf_path, images_dir)
        process_images_in_folder(images_dir)
    elif os.path.isdir(input_path):
        process_images_in_folder(input_path)
    else:
        print("[ERREUR] Chemin non reconnu (ni PDF ni dossier d'images).")
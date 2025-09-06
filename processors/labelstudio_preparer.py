import json
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image


INPUT_DIR = Path("input_pdf_bis")
OUTPUT_ROOT = Path("output_pdf_to_labelstudio")

PDF_DPI = 300  
PDF_WIDTH = 595.2756   # A4
PDF_HEIGHT = 841.8898
IMG_FORMAT = "jpg" 

def create_labelstudio_tasks(images, ocr_pages, pdf_width, pdf_height):
    tasks = []

    for page_idx, (img_path, tokens) in enumerate(zip(images, ocr_pages)):
        with Image.open(img_path) as im:
            img_w, img_h = im.size

            # 🔍 Afficher la taille de l'image utilisée pour l'annotation
            print(f"[TAILLE] Image utilisée pour annotation {img_path.name} : {img_w} x {img_h}")

        results = []
        for tok in tokens:
            text = tok.get("text", "")
            x0, y0, x1, y1 = tok["x0"], tok["y0"], tok["x1"], tok["y1"]

            left_px = (x0 / pdf_width) * img_w
            top_px = (y0 / pdf_height) * img_h
            width_px = ((x1 - x0) / pdf_width) * img_w
            height_px = ((y1 - y0) / pdf_height) * img_h

            x_pct = (left_px / img_w) * 100
            y_pct = (top_px / img_h) * 100
            w_pct = (width_px / img_w) * 100
            h_pct = (height_px / img_h) * 100

            results.append({
                "from_name": "bbox",
                "to_name": "image",
                "type": "rectangle",
                "value": {
                    "x": x_pct,
                    "y": y_pct,
                    "width": w_pct,
                    "height": h_pct,
                    "rotation": 0,
                    "original_width": img_w,
                    "original_height": img_h
                },
                "origin": "manual"
            })

            results.append({
                "from_name": "transcription",
                "to_name": "image",
                "type": "textarea",
                "value": {"text": [text]},
                "origin": "manual"
            })

        task = {
            "data": {"image": img_path.name},
            "predictions": [{"result": results}]
        }
        tasks.append(task)

    return tasks
from pdf2image import convert_from_path
from PIL import Image



def convert_pdf_to_images(pdf_path, out_dir, dpi=300, img_format="jpg"):
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    image_paths = []
    out_dir.mkdir(parents=True, exist_ok=True)
    pil_format = "JPEG" if img_format.lower() in ("jpg", "jpeg") else "PNG"

    for idx, page in enumerate(pages):
        img_name = f"{pdf_path.stem}_page-{idx+1:04d}.{img_format}"
        img_path = out_dir / img_name
        page.save(str(img_path), pil_format)
        image_paths.append(img_path)

        # 🔍 Afficher la taille de l'image générée
        with Image.open(img_path) as im:
            print(f"[TAILLE] Image générée {img_name} : {im.size} (largeur x hauteur)")

        print(f"[INFO] {pdf_path.name} - Page {idx+1} convertie -> {img_path.name}")

    return image_paths
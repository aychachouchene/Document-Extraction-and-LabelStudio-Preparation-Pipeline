from pathlib import Path
from converters.excel_to_pdf import excel_to_pdf


OUTPUT_ROOT = "output_excel_to_pdf"

def process_folder(input_folder):
    """Convertit tous les fichiers Excel d'un dossier en PDF complet."""
    input_folder = Path(input_folder).resolve()
    output_root = Path(OUTPUT_ROOT).resolve()
    output_root.mkdir(exist_ok=True)

    excel_files = [f for f in input_folder.glob("*.xlsx")]
    if not excel_files:
        print(f"[INFO] Aucun fichier Excel trouvé dans {input_folder}")
        return

    for excel_file in excel_files:
        pdf_full = (output_root / f"{excel_file.stem}_full.pdf").resolve()
        excel_to_pdf(excel_file.resolve(), pdf_full)

    print(f"\n✅ Conversion terminée. Les PDF complets sont dans {output_root}")
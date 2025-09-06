
from pathlib import Path
import win32com.client


def excel_to_pdf(excel_path, pdf_path):
    """Convertir un fichier Excel en un PDF complet sélectionnable avec ajustements de texte."""
    excel_path = str(Path(excel_path).resolve())
    pdf_path = str(Path(pdf_path).resolve())
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    wb = None
    try:
        wb = excel.Workbooks.Open(excel_path)
        print(f"[INFO] Conversion : {excel_path} -> {pdf_path}")
        for sheet in wb.Sheets:
            # ✅ Activer le retour à la ligne
            sheet.Cells.WrapText = True
            # ✅ Ajuster hauteur lignes et largeur colonnes
            sheet.Cells.EntireRow.AutoFit()
            sheet.Cells.EntireColumn.AutoFit()
            # ✅ Mise en page : adapter à la largeur de page
            sheet.PageSetup.Zoom = False
            sheet.PageSetup.FitToPagesWide = 1
            sheet.PageSetup.FitToPagesTall = False  # pour ne pas écraser verticalement

        # Export en PDF
        wb.ExportAsFixedFormat(0, pdf_path)

    except Exception as e:
        print(f"[ERREUR] Impossible de convertir {excel_path} : {e}")
    finally:
        if wb is not None:
            wb.Close(False)
        excel.Quit()
import pandas as pd

def extract_excel_words_boxes(excel_path, cell_width=50, cell_height=20):
    data = []

    xls = pd.ExcelFile(excel_path)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

        for row_idx, row in df.iterrows():
            for col_idx, cell_value in enumerate(row):
                if pd.isna(cell_value):
                    continue

                word = str(cell_value)

                x0 = col_idx * cell_width
                y0 = row_idx * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height

                data.append({
                    "text": word,
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "sheet": sheet_name,
                    "row_idx": row_idx,
                    "col_idx": col_idx
                })

    return data
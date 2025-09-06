import re
import pdfplumber


def extract_pdf_words_boxes(pdf_path, max_gap=10):
    data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            words = page.extract_words()

            merged = []
            i = 0
            while i < len(words):
                word = words[i]
                text = word["text"]

                # Cas 1: token = 1-3 chiffres, suivi d'un token décimal OU d'un token avec espace et décimale
                if re.match(r"^-?\d{1,3}$", text):
                    if i + 1 < len(words):
                        next_word = words[i + 1]
                        next_text = next_word["text"]
                        close_enough = int(next_word["x0"]) - int(word["x1"]) < max_gap
                        same_line = abs(int(next_word["top"]) - int(word["top"])) < 3
                        # Cas 1a: token décimal simple (ex: 517.49 ou 000.00-)
                        if close_enough and same_line and re.match(r"^\d{3}[,.]\d{2}-?$", next_text):
                            merged_text = f"{text} {next_text}"
                            x0, y0 = int(word["x0"]), int(word["top"])
                            x1, y1 = int(next_word["x1"]), int(next_word["bottom"])
                            merged.append({
                                "text": merged_text,
                                "x0": x0,
                                "y0": y0,
                                "x1": x1,
                                "y1": y1,
                                "page": page_num
                            })
                            i += 2
                            continue
                        # Cas 1b: token avec espace et décimale (ex: 159 982,16)
                        if close_enough and same_line and re.match(r"^\d{3}( \d{3})*[,.]\d{2}-?$", next_text):
                            merged_text = f"{text} {next_text}"
                            x0, y0 = int(word["x0"]), int(word["top"])
                            x1, y1 = int(next_word["x1"]), int(next_word["bottom"])
                            merged.append({
                                "text": merged_text,
                                "x0": x0,
                                "y0": y0,
                                "x1": x1,
                                "y1": y1,
                                "page": page_num
                            })
                            i += 2
                            continue

                # Cas 2: token déjà complet (ex: 53 320.86 ou 000.00- seul)
                if re.match(r"^\d{1,3}( \d{3})*[,.]\d{2}-?$", text) or re.match(r"^\d{3}[,.]\d{2}-?$", text):
                    merged.append({
                        "text": text,
                        "x0": int(word["x0"]),
                        "y0": int(word["top"]),
                        "x1": int(word["x1"]),
                        "y1": int(word["bottom"]),
                        "page": page_num
                    })
                    i += 1
                    continue

                # Sinon, mot normal
                merged.append({
                    "text": text,
                    "x0": int(word["x0"]),
                    "y0": int(word["top"]),
                    "x1": int(word["x1"]),
                    "y1": int(word["bottom"]),
                    "page": page_num
                })
                i += 1

            data.extend(merged)

    return data


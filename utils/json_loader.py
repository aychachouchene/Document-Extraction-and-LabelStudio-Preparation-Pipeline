import json


def load_tokens_per_page(ocr_file):
    with ocr_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return [data["ocr"]] if "ocr" in data else [data]
    elif isinstance(data, list):
        pages = {}
        for tok in data:
            page_num = tok.get("page", 0)
            pages.setdefault(page_num, []).append(tok)
        return [pages[k] for k in sorted(pages.keys())]
    else:
        raise ValueError("Format OCR inconnu")

# import os
#
# import requests
#
# from config import OUTPUT_FOLDER, logger
#
# def save_html(filename: str, content: str) -> None:
#     filepath = os.path.join(OUTPUT_FOLDER, filename)
#     with open(filepath, "w", encoding="utf-8") as out_file:
#         out_file.write(content)
#     size = os.path.getsize(filepath)
#     logger.info(f"Saved: {filepath} ({format_size(size)})")
#
#
# def download_and_save(page_index: int, url: str) -> str:
#     """Download and save a single URL. If skip_cleanup is True the HTML cleanup step is skipped."""
#     html_text = download_page(url)
#     filename = str(page_index) + ".html"
#     save_html(filename, html_text)
#     return html_text
#

def format_size(num_bytes: int) -> str:
    num = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024.0 or unit == "TB":
            if unit == "B":
                return f"{int(num)} {unit}"
            return f"{num:.2f} {unit}"
        num /= 1024.0
    return ''


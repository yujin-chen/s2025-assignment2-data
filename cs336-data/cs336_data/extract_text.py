from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text

def extract_text_from_html_bytes(html_bytes):

    try:
        # Decode using UTF-8
        html_str = html_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # Detect encoding
        detected_encoding = detect_encoding(html_bytes)

        # Ensure getting actual encoding string, not an object
        encoding = detected_encoding if isinstance(detected_encoding, str) else detected_encoding.encoding

        # If encoding detection fails, default to 'latin-1'
        html_str = html_bytes.decode(encoding or "latin-1", errors="replace")

    # Extract visible text from the decoded HTML
    return extract_plain_text(html_str)


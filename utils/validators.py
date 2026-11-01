"""
CipherVault – Input Validation Utilities
"""


def validate_caesar_shift(shift_input: str) -> int:
    """Parse and return an integer shift value. Raises ValueError on bad input."""
    if shift_input is None or str(shift_input).strip() == "":
        raise ValueError("Shift value is required.")
    try:
        return int(shift_input)
    except (TypeError, ValueError):
        raise ValueError(f"Shift must be an integer. Got: '{shift_input}'")


def validate_vigenere_keyword(keyword: str) -> str:
    """Validate that the keyword is non-empty and purely alphabetic."""
    if not keyword or not keyword.strip():
        raise ValueError("Keyword is required.")
    keyword = keyword.strip()
    if not keyword.isalpha():
        raise ValueError("Keyword must contain only letters (A-Z, a-z).")
    return keyword


def validate_text_input(text: str, field_name: str = "Input text") -> str:
    """Ensure text is not empty."""
    if text is None or str(text).strip() == "":
        raise ValueError(f"{field_name} must not be empty.")
    return text


def validate_uploaded_file(uploaded_file) -> str:
    """
    Validate an uploaded file: must be .txt and ≤ 1 MB.
    Returns the decoded text content.
    """
    MAX_SIZE = 1 * 1024 * 1024  # 1 MB

    if uploaded_file is None:
        raise ValueError("No file uploaded.")

    name = uploaded_file.name
    if not name.lower().endswith(".txt"):
        raise ValueError(f"Only .txt files are supported. Got: '{name}'")

    raw = uploaded_file.read()
    if len(raw) > MAX_SIZE:
        raise ValueError(f"File exceeds the 1 MB size limit ({len(raw):,} bytes).")

    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("File is not valid UTF-8 text.")

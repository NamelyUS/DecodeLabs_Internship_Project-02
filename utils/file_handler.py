"""
CipherVault – File Handler Utilities
Read and prepare text file content for encryption/decryption.
"""


def read_text_file(uploaded_file) -> str:
    """Read and decode an uploaded Streamlit file object."""
    raw = uploaded_file.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Cannot decode file. Ensure it is UTF-8 encoded.")


def prepare_download(text: str, filename: str = "ciphervault_output.txt") -> tuple[str, str]:
    """Return (text_content, filename) ready for Streamlit download button."""
    return text, filename

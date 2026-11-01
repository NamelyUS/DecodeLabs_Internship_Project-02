# CipherVault – Project Notes

## Architecture Decisions

1. **Single-file Streamlit app** (`app.py`) with sidebar radio navigation — avoids multi-page file overhead while keeping clean section separation.
2. **Algorithm modules** (`algorithms/`) are pure functions with no Streamlit dependency — easily testable and reusable.
3. **Utils modules** (`utils/`) handle validation, file I/O, and history — separated from business logic and UI.
4. **Session-state history** — no database needed; history lives in `st.session_state` and resets per session. No plaintext or keys logged.
5. **Custom CSS** injected via `st.markdown` — dark cybersecurity theme with Inter + JetBrains Mono fonts, gradient accents, hover effects.
6. **Only dependency: Streamlit** — everything else uses stdlib. Pandas is bundled with Streamlit.

## Key Design Choices

- Caesar shift normalized via `% 26` — handles negative shifts and shifts > 26 correctly.
- Vigenère keyword validated to be purely alphabetic (non-alpha chars in keyword rejected).
- Non-alphabetic characters (spaces, digits, punctuation) pass through unchanged in both ciphers.
- File uploads limited to `.txt`, max 1 MB, UTF-8 only.
- Download uses a new filename (`{original}_encrypted.txt`) — never overwrites the original.
- Brute force displays all 25 shifts in a DataFrame table.
- Frequency analysis uses `collections.Counter` and Streamlit's built-in bar chart.

## Testing Strategy

- `unittest` (stdlib) — no pytest dependency needed.
- 42 tests covering all specified scenarios.
- Tests are standalone (no Streamlit required to run).

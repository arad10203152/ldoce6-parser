# LDOCE6 to Anki Pipeline & Parser

## Overview & Project Goal
The objective of this project is to parse the raw **Longman Dictionary of Contemporary English 6th Edition (LDOCE6)** MDX files into a structured, relational hierarchy. By transforming unstructured dictionary data into a clean **SQLite** database (`ldoce.db`), this project provides the foundational backend required for automated, high-fidelity **Anki flashcard generation** via Anki-Connect. Additionally, a lightweight **Flask** web application is included to visualize the hierarchical entries in real-time.

---

## Data Sources & Raw Assets
The raw MDX/MDD container files used for parsing are sourced from community releases:
* **Repository/Release:** [Sorosliu1029/English-Dictionaries (LDOCE6)](https://github.com/Sorosliu1029/English-Dictionaries/releases/tag/longman_dictionary_of_contemporary_english_6th_edition)
* **Local Storage:** Place the downloaded `.mdx` and `.mdd` files inside a `data/` directory or reference them correctly in your parsing scripts using `pathlib`.

---

## Tech Stack & Environment
* **OS:** macOS
* **Environment Manager:** `uv` (for fast Python package and dependency management)
* **Core Libraries:** 
  * `BeautifulSoup4` & `lxml` (for robust HTML parsing)
  * `readmdict` (for native MDX file extraction)
  * `Flask` (for local visualization and web inspection)
  * `sqlite3` (built-in relational storage)

---

## Project File Structure & Descriptions

| File Name | Description & Purpose |
| :--- | :--- |
| `better_parser.py` | **Core Parser & DB Migrator:** Extracts structured data (Headwords, Phonetics, POS, Signposts, Definitions, and Corpus Examples) from the MDX file and commits them relationally into `ldoce.db`. |
| `app.py` | **Flask Web Viewer:** Serves a local web interface (`http://127.0.0.1:5000`) to visually inspect the parsed hierarchical records from SQLite. |
| `ldoce.db` | **SQLite Database:** Stores normalized relational records (`words` and `senses` tables linked via foreign keys). |
| `pipeline.py` | **Anki Integration (Upcoming):** Designed to fetch records from `ldoce.db` and push them into Anki via Anki-Connect. |
| `jsonl_to_sqlite.py` | **Migration Utility:** Handles batch transfer of intermediate JSONL structured data into SQLite. |
| `extract_media.py` | **Asset Extractor:** Extracts associated multimedia (images/audio) from the MDX container. |

---

## Database Schema (`ldoce.db`)

### 1. `words` Table
Stores unique headword entries and phonetics.
```sql
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE,
    phonetic TEXT
);

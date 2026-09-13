import json
from pathlib import Path
from tqdm import tqdm
from readmdict import MDX
from parse_single_entry import LDOCE6StructuralParser
from extract_media import find_and_save_audio

MDX_PATH = Path("../longman_dictionary_of_contemporary_english_6th_edition.mdx")
OUTPUT_JSONL_PATH = Path("output_json/ldoce6_bulk_extracted.jsonl")

def run_bulk_parsing(extract_audio_simultaneously=False):
    """
    Iterates through the entire MDX database, parses every dictionary entry 
    structurally, and exports the collection into a high-performance JSONL file.
    """
    if not MDX_PATH.exists():
        print(f"Error: MDX file not found at {MDX_PATH}")
        return

    print("Initializing MDX database entry loop...")
    mdx = MDX(str(MDX_PATH))
    
    # Ensure parent directory for output exists
    OUTPUT_JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    skipped_count = 0

    print("Starting bulk parsing pipeline. This might take a few minutes...")
    
    # Open the JSONL file in append/write mode with UTF-8 encoding
    with open(OUTPUT_JSONL_PATH, "w", encoding="utf-8") as jsonl_file:
        # Wrap mdx.items() with tqdm to display a live progress bar in terminal
        for key, value in tqdm(mdx.items(), desc="Parsing Entries"):
            try:
                word = key.decode("utf-8", errors="ignore")
                html_content = value.decode("utf-8", errors="ignore")

                # Skip internal MDX metadata keys if they appear
                if word.startswith("file://") or not word.strip():
                    skipped_count += 1
                    continue

                # Parse the structural schema using our BeautifulSoup core module
                parser = LDOCE6StructuralParser(html_content)
                parsed_entry = parser.parse()

                if not parsed_entry:
                    skipped_count += 1
                    continue

                # If flag is explicitly set, trigger binary extraction from MDD
                if extract_audio_simultaneously and parsed_entry.get("Audio"):
                    for audio_link in parsed_entry["Audio"]:
                        find_and_save_audio(audio_link)

                # Write a single line containing the isolated entry JSON
                json_line_string = json.dumps(parsed_entry, ensure_ascii=False)
                jsonl_file.write(json_line_string + "\n")
                
                success_count += 1

            except Exception as entry_error:
                # Keep loop running even if an individual malformed entry fails
                skipped_count += 1
                continue

    print("\n" + "=" * 60)
    print("BULK PROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"✓ Total successfully parsed entries: {success_count}")
    print(f"✓ Total skipped or empty entries:    {skipped_count}")
    print(f"✓ Final database artifact stored at: {OUTPUT_JSONL_PATH}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    # Set to True only if you want to extract ALL audio files at once (highly time consuming)
    run_bulk_parsing(extract_audio_simultaneously=False)

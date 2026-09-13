import sys
import json
from pathlib import Path
from readmdict import MDX
from parse_single_entry import LDOCE6StructuralParser
from extract_media import find_and_save_audio

MDX_PATH = Path("../longman_dictionary_of_contemporary_english_6th_edition.mdx")
OUTPUT_DATA_DIR = Path("output_json")

def run_pipeline(target_word):
    """
    Runs the complete pipeline: Parses HTML from MDX and extracts associated 
    audio files from MDD based on the extracted entry data.
    """
    if not MDX_PATH.exists():
        print(f"Error: MDX file not found at {MDX_PATH}")
        return

    mdx = MDX(str(MDX_PATH))
    entry_found = False

    # Search for the target word inside MDX dictionary keys
    for key, value in mdx.items():
        word = key.decode("utf-8", errors="ignore")

        if word.lower() == target_word.lower():
            entry_found = True
            html_content = value.decode("utf-8", errors="ignore")

            # 1. Parse text and structural data
            parser = LDOCE6StructuralParser(html_content)
            parsed_data = parser.parse()

            # 2. Extract and download associated audio links if present
            audio_links = parsed_data.get("Audio", [])
            print(f"\nFound {len(audio_links)} audio reference(s) for '{target_word}'.")
            
            for link in audio_links:
                # Triggers the logic from extract_media to search and save raw bytes
                find_and_save_audio(link)

            # 3. Save clean structural JSON output
            OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
            json_file_path = OUTPUT_DATA_DIR / f"{target_word.lower()}.json"
            
            with open(json_file_path, "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, indent=4, ensure_ascii=False)

            print("-" * 60)
            print(f"✓ Structured JSON saved to: {json_file_path}")
            print(f"✓ Process complete for target: {target_word}\n")
            break

    if not entry_found:
        print(f"✗ Target word '{target_word}' could not be located in MDX database.")

if __name__ == "__main__":
    # Fallback to default word 'take' if no CLI argument is supplied
    word_arg = sys.argv[1] if len(sys.argv) > 1 else "take"
    run_pipeline(word_arg)

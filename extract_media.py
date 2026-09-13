import sys
from pathlib import Path
from readmdict import MDD

MDD_PATH = Path("../longman_dictionary_of_contemporary_english_6th_edition.mdd")

def find_and_save_audio(mdd_link, output_dir="output_media"):
    """
    Extracts binary audio data from MDD using a sound:// link reference.
    """
    if not MDD_PATH.exists():
        print(f"Error: MDD file not found at {MDD_PATH}")
        return False

    # Clean protocols and leading slashes
    cleaned_key = mdd_link.replace("sound://", "").replace("sound:", "")
    if cleaned_key.startswith("/"):
        cleaned_key = cleaned_key[1:]
    if cleaned_key.startswith("\\"):
        cleaned_key = cleaned_key[1:]
    
    # Generate potential variations used in MDX keys
    variants = {
        cleaned_key.lower(),
        cleaned_key.replace("/", "\\").lower(),
        cleaned_key.replace("\\", "/").lower(),
        (chr(92) + cleaned_key.replace("/", "\\")).lower(), # Leading backslash '\'
        ("/" + cleaned_key.replace("\\", "/")).lower()     # Leading forward slash '/'
    }

    print(f"Searching MDD for variations of: {cleaned_key}")
    
    mdd = MDD(str(MDD_PATH))
    audio_data = None

    # Iterate through MDD keys to find a match
    for key, value in mdd.items():
        mdd_key_str = key.decode('utf-8', errors='ignore').lower()
        if mdd_key_str in variants:
            audio_data = value
            actual_matched_key = mdd_key_str
            break

    if audio_data:
        # Determine clean local filename
        filename = Path(cleaned_key).name
        out_path = Path(output_dir) / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        out_path.write_bytes(audio_data)
        print(f"✓ Success! Matched key: '{actual_matched_key}'")
        print(f"✓ Audio successfully saved to: {out_path}")
        return True
    
    print("✗ Audio key could not be found inside the MDD index.")
    return False

if __name__ == "__main__":
    test_audio_link = "sound://hwd/bre/a/take_n0205.mp3"
    find_and_save_audio(test_audio_link)

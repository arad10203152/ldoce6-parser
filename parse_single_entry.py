import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup
from readmdict import MDX

MDX_PATH = Path("../longman_dictionary_of_contemporary_english_6th_edition.mdx")

class LDOCE6StructuralParser:
    def __init__(self, html_content):
        # Use lxml for high-performance parsing of large dictionary entries
        self.soup = BeautifulSoup(html_content, "lxml")
        # Remove navigation menus and popups to prevent data duplication
        for button_node in self.soup.select(".buttons, [nattr='at-link']"):
            button_node.decompose()

    def parse(self):
        entry_node = self.soup.select_one(".entry")
        if not entry_node:
            return {}

        # 1. Extract Headword (General Information)
        head_node = entry_node.select_one(".entryhead")
        word = head_node.select_one(".hwd").get_text(strip=True) if head_node and head_node.select_one(".hwd") else ""
        phonetic = head_node.select_one(".pron").get_text(strip=True) if head_node and head_node.select_one(".pron") else ""
        pos = head_node.select_one(".pos").get_text(strip=True) if head_node and head_node.select_one(".pos") else ""
        
        stars = ""
        stars_node = head_node.select_one(".level") if head_node else None
        if stars_node:
            stars = stars_node.get_text(strip=True)

        frequencies = []
        if head_node:
            frequencies = [f.get_text(strip=True) for f in head_node.select(".freq")]

        # Extract headword pronunciation audio links
        audio_urls = []
        if head_node:
            audio_urls = [a['href'] for a in head_node.select("a[href^='sound://']")]

        # 2. Extract Senses Hierarchically
        senses_data = []
        sense_nodes = entry_node.select(".Sense, .sense")
        
        for idx, s_node in enumerate(sense_nodes, 1):
            # Skip nested senses inside sub-panels like Thesaurus
            if self._is_sub_panel(s_node):
                continue

            sensenum = s_node.select_one(".sensenum")
            signpost = s_node.select_one(".signpost")
            gram = s_node.select_one(".gram, .grammar")
            definition = s_node.select_one(".def")

            # Extract sense-specific examples
            examples = []
            for ex in s_node.select(".example"):
                if ex.find_parent(class_=["Thesaurus", "Panel"]) is None:
                    txt = ex.get_text(" ", strip=True)
                    if txt:
                        examples.append(txt)

            # Extract sense-specific collocations
            collocations = []
            for col in s_node.select(".colloc, .COLLOC, .collocationsbox .w"):
                if col.find_parent(class_=["Thesaurus", "Panel"]) is None:
                    txt = col.get_text(" ", strip=True)
                    if txt:
                        collocations.append(txt)

            senses_data.append({
                "sense_index": idx,
                "number": sensenum.get_text(strip=True) if sensenum else str(idx),
                "signpost": signpost.get_text(strip=True) if signpost else "",
                "grammar": gram.get_text(strip=True) if gram else "",
                "definition": definition.get_text(" ", strip=True) if definition else "",
                "examples": list(dict.fromkeys(examples)),
                "collocations": list(dict.fromkeys(collocations))
            })

        # 3. Extract Global Fields
        common_errors = [e.get_text(" ", strip=True) for e in entry_node.select(".errorbox, .common-error")]
        corpus_examples = [c.get_text(" ", strip=True) for c in entry_node.select(".colloinexa")]

        return {
            "Word": word,
            "Phonetic": phonetic,
            "POS": pos,
            "Stars": stars,
            "Frequency": frequencies,
            "Audio": audio_urls,
            "Senses": senses_data,
            "GlobalCommonErrors": list(dict.fromkeys(common_errors)),
            "GlobalCorpus": list(dict.fromkeys(corpus_examples))
        }

    def _is_sub_panel(self, node):
        """Check if the node belongs to auxiliary panels (e.g., Thesaurus)."""
        parent = node.parent
        while parent:
            if hasattr(parent, 'attrs') and 'class' in parent.attrs:
                classes = parent['class']
                if any(cls in ['Thesaurus', 'thesaurus', 'Panel', 'Business'] for cls in classes):
                    return True
            parent = parent.parent
        return False


def test_word(target):
    mdx = MDX(str(MDX_PATH))

    for key, value in mdx.items():
        word = key.decode("utf-8", errors="ignore")

        if word.lower() == target.lower():
            html = value.decode("utf-8", errors="ignore")

            print("\n" + "=" * 100)
            print(f"STRUCTURAL PARSED ENTRY FOR: {target}")
            print("=" * 100)

            parser = LDOCE6StructuralParser(html)
            parsed = parser.parse()

            print(json.dumps(parsed, indent=4, ensure_ascii=False))
            return

    print("Word not found:", target)


if __name__ == "__main__":
    word = sys.argv[1] if len(sys.argv) > 1 else "take"
    test_word(word)


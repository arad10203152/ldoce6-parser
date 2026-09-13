




from bs4 import BeautifulSoup
from readmdict import MDX
import re


def dedupe_keep_order(items):
    seen = set()
    result = []

    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)

    return result


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    text = text.replace("·", "")
    text = text.replace("SYN ", "")
    text = text.replace("OPP ", "")

    return text.strip()



def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_entry(html):

    soup = BeautifulSoup(html, "lxml")

    data = {
        "word": "",
        "phonetic": "",
        "pos": "",
        "grammar": "",
        "definitions": [],
        "examples": [],
        "phrases": [],
        "collocations": [],
        "synonyms": [],
        "opposites": [],
        "common_errors": [],
        "etymology": "",
        "frequency": "",
	"stars": "",
    }

    # headword
    hwd = soup.select_one(".hwd")
    if hwd:
        data["word"] = clean_text(hwd.get_text())

    # pronunciation
    pron = soup.select_one(".pron")
    if pron:
        data["phonetic"] = clean_text(pron.get_text())

    # POS
    pos = soup.select_one(".pos")
    if pos:
        data["pos"] = clean_text(pos.get_text())

    # grammar
    gram = soup.select_one(".gram")
    if gram:
        data["grammar"] = clean_text(gram.get_text())

    # level / frequency
    level = soup.select_one(".level")
    if level:
        data["level"] = clean_text(level.get_text())

    freq = soup.select_one(".freq")
    if freq:
        data["frequency"] = clean_text(freq.get_text())

    # definitions
    for d in soup.select(".sense .def"):
        txt = clean_text(d.get_text(" ", strip=True))
        if txt and txt not in data["definitions"]:
            data["definitions"].append(txt)

    # subsenses
    for d in soup.select(".subsense .def"):
        txt = clean_text(d.get_text(" ", strip=True))
        if txt and txt not in data["definitions"]:
            data["definitions"].append(txt)

    # examples
    for ex in soup.select(".example"):
        txt = clean_text(ex.get_text(" ", strip=True))
        if txt:
            data["examples"].append(txt)

    # phrases / expressions
    for phrase in soup.select(".phrasetext, .lexunit"):
        txt = clean_text(phrase.get_text())
        if txt:
            data["phrases"].append(txt)

    # collocations
    for coll in soup.select(".colloc"):
        txt = clean_text(coll.get_text())
        if txt:
            data["collocations"].append(txt)

    # synonyms
    for syn in soup.select(".syn"):
        txt = clean_text(syn.get_text())
        if txt:
            data["synonyms"].append(txt)

    # opposites
    for opp in soup.select(".opp"):
        txt = clean_text(opp.get_text())
        if txt:
            data["opposites"].append(txt)

    # common errors
    for err in soup.select(".error, .warning, .badexa"):
        txt = clean_text(err.get_text())
        if txt:
            data["common_errors"].append(txt)

    # etymology
    etym = soup.select_one(".etymology")
    if etym:
        data["etymology"] = clean_text(etym.get_text(" ", strip=True))

    return data


mdx = MDX(
    "../longman_dictionary_of_contemporary_english_6th_edition.mdx"
)

items = mdx.items()

target_word = "take"

for key, value in items:

    word = key.decode(
        "utf-8",
        errors="ignore"
    )

    if word.lower() == target_word:

        html = value.decode(
            "utf-8",
            errors="ignore"
        )

        entry = extract_entry(html)

        print("\n" + "=" * 80)
        print("WORD:", entry["word"])
        print("=" * 80)

        for k, v in entry.items():

            if k == "word":
                continue

            print(f"\n{k.upper()}")

            if isinstance(v, list):
                for item in v[:20]:
                    print("-", item)
            else:
                print(v)

        break

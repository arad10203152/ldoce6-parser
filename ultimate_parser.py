from bs4 import BeautifulSoup
from readmdict import MDX
import re


MDX_PATH = "../longman_dictionary_of_contemporary_english_6th_edition.mdx"

TARGET_WORD = "take"


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    replacements = {
        "·": "",
        "SYN ": "",
        "OPP ": "",
        "\xa0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


def dedupe_keep_order(items):
    seen = set()
    result = []

    for item in items:
        item = clean_text(item)

        if item and item not in seen:
            seen.add(item)
            result.append(item)

    return result


def extract_entry(html):

    soup = BeautifulSoup(html, "lxml")

    data = {
        "word": "",
        "phonetic": "",
        "part_of_speech": "",
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

    # ----------------------------
    # BASIC INFO
    # ----------------------------

    hwd = soup.select_one(".hwd")
    if hwd:
        data["word"] = clean_text(
            hwd.get_text()
        )

    pron = soup.select_one(".pron")
    if pron:
        data["phonetic"] = clean_text(
            pron.get_text()
        )

    pos = soup.select_one(".pos")
    if pos:
        data["part_of_speech"] = clean_text(
            pos.get_text()
        )

    gram = soup.select_one(".gram")
    if gram:
        data["grammar"] = clean_text(
            gram.get_text()
        )

    # ----------------------------
    # FREQUENCY / LEVEL
    # ----------------------------

    freq = soup.select_one(".frequent")
    if freq:
        data["frequency"] = clean_text(
            freq.get_text()
        )

    level = soup.select_one(".level")
    if level:
        data["stars"] = clean_text(
            level.get_text()
        )

    # ----------------------------
    # DEFINITIONS
    # ----------------------------

    for d in soup.select(".sense .def"):
        txt = clean_text(
            d.get_text(" ", strip=True)
        )

        if txt:
            data["definitions"].append(txt)

    for d in soup.select(".subsense .def"):
        txt = clean_text(
            d.get_text(" ", strip=True)
        )

        if txt:
            data["definitions"].append(txt)

    # ----------------------------
    # EXAMPLES
    # ----------------------------

    for ex in soup.select(".example"):
        txt = clean_text(
            ex.get_text(" ", strip=True)
        )

        if txt:
            data["examples"].append(txt)

    # ----------------------------
    # PHRASES / EXPRESSIONS
    # ----------------------------

    for phrase in soup.select(
        ".phrasetext, .lexunit"
    ):
        txt = clean_text(
            phrase.get_text(
                " ",
                strip=True
            )
        )

        if txt:
            data["phrases"].append(txt)

    # ----------------------------
    # COLLOCATIONS
    # ----------------------------

    for coll in soup.select(".colloc"):

        txt = clean_text(
            coll.get_text(
                " ",
                strip=True
            )
        )

        if not txt:
            continue

        # noisy junk
        if len(txt) < 5:
            continue

        if "..." in txt:
            continue

        data["collocations"].append(txt)

    # ----------------------------
    # SYNONYMS
    # ----------------------------

    for syn in soup.select(".syn"):
        txt = clean_text(
            syn.get_text(
                " ",
                strip=True
            )
        )

        if txt:
            data["synonyms"].append(txt)

    # ----------------------------
    # OPPOSITES
    # ----------------------------

    for opp in soup.select(".opp"):
        txt = clean_text(
            opp.get_text(
                " ",
                strip=True
            )
        )

        if txt:
            data["opposites"].append(txt)

    # ----------------------------
    # COMMON ERRORS
    # ----------------------------

    for err in soup.select(
        ".error, .warning, .badexa"
    ):
        txt = clean_text(
            err.get_text(
                " ",
                strip=True
            )
        )

        if txt:
            data["common_errors"].append(txt)

    # ----------------------------
    # ETYMOLOGY
    # ----------------------------

    etym = soup.select_one(
        ".etymology"
    )

    if etym:
        data["etymology"] = clean_text(
            etym.get_text(
                " ",
                strip=True
            )
        )

    # ----------------------------
    # CLEANUP
    # ----------------------------

    for key in data:

        if isinstance(
            data[key],
            list
        ):
            data[key] = (
                dedupe_keep_order(
                    data[key]
                )
            )

    data["definitions"] = (
        data["definitions"][:10]
    )

    data["examples"] = (
        data["examples"][:10]
    )

    data["collocations"] = (
        data["collocations"][:20]
    )

    data["phrases"] = (
        data["phrases"][:20]
    )

    return data


def print_entry(entry):

    print("\n" + "=" * 80)
    print(
        "WORD:",
        entry["word"]
    )
    print("=" * 80)

    for key, value in entry.items():

        if key == "word":
            continue

        title = (
            key.upper()
            .replace("_", " ")
        )

        print(
            "\n"
            + "-" * 80
        )
        print(title)
        print(
            "-" * 80
        )

        if isinstance(
            value,
            list
        ):

            if not value:
                print("(empty)")
                continue

            for item in value:
                print(
                    "•",
                    item
                )

        else:
            print(
                value
                if value
                else "(empty)"
            )


def main():

    print(
        "\nOpening MDX..."
    )

    mdx = MDX(MDX_PATH)

    print(
        "Searching word:",
        TARGET_WORD
    )

    found = False

    for key, value in mdx.items():

        word = key.decode(
            "utf-8",
            errors="ignore"
        )

        if (
            word.lower()
            == TARGET_WORD.lower()
        ):

            html = value.decode(
                "utf-8",
                errors="ignore"
            )

            entry = (
                extract_entry(
                    html
                )
            )

            print_entry(
                entry
            )

            found = True
            break

    if not found:
        print(
            "\nWord not found."
        )


if __name__ == "__main__":
    main()

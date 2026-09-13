from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from readmdict import MDX


MDX_PATH = Path(
    "../longman_dictionary_of_contemporary_english_6th_edition.mdx"
)


def inspect_classes(limit=300):

    mdx = MDX(str(MDX_PATH))

    class_counter = Counter()

    processed = 0

    for key, value in mdx.items():

        html = value.decode(
            "utf-8",
            errors="ignore"
        )

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        for tag in soup.find_all(True):

            classes = tag.get("class", [])

            for c in classes:
                class_counter[c] += 1

        processed += 1

        if processed >= limit:
            break

    print("\nTOP HTML CLASSES\n")
    print("=" * 80)

    for cls, count in class_counter.most_common(200):
        print(f"{cls:30} {count}")


inspect_classes()

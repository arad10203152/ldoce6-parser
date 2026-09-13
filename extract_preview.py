from pathlib import Path
from readmdict import MDX


MDX_PATH = Path(
    "../longman_dictionary_of_contemporary_english_6th_edition.mdx"
)


def preview_entries(limit=10):
    print("Opening MDX...")

    mdx = MDX(str(MDX_PATH))

    print("Reading entries...")

    count = 0

    for key, value in mdx.items():
        word = key.decode("utf-8", errors="ignore")

        try:
            html = value.decode("utf-8", errors="ignore")
        except:
            html = str(value)

        print("\n" + "=" * 80)
        print("WORD:", word)
        print("=" * 80)

        print(html[:3000])

        count += 1

        if count >= limit:
            break


preview_entries()

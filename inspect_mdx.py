from pathlib import Path
import struct


def inspect_binary(path, read_size=256):
    path = Path(path)

    print("=" * 80)
    print("FILE:", path.name)
    print("SIZE:", round(path.stat().st_size / 1024 / 1024, 2), "MB")
    print("=" * 80)

    with open(path, "rb") as f:
        header = f.read(read_size)

    print("\nHEX HEADER:")
    print(header[:128].hex(" "))

    print("\nASCII VIEW:")
    ascii_preview = "".join(
        chr(b) if 32 <= b <= 126 else "."
        for b in header[:256]
    )
    print(ascii_preview)

    print("\nPOSSIBLE MAGIC BYTES:")

    magic_checks = {
        b"\x78\x9c": "zlib",
        b"PK\x03\x04": "zip",
        b"SQLite format 3": "sqlite",
        b"\x1f\x8b": "gzip",
    }

    found = False
    for sig, name in magic_checks.items():
        if sig in header:
            print(f"Found: {name}")
            found = True

    if not found:
        print("No common signatures found.")

    print("\nUINT32 Preview:")

    for i in range(0, min(len(header), 64), 4):
        chunk = header[i:i+4]
        if len(chunk) == 4:
            val = struct.unpack("<I", chunk)[0]
            print(f"{i:04d}: {val}")


inspect_binary(
    "../longman_dictionary_of_contemporary_english_6th_edition.mdx"
)

inspect_binary(
    "../longman_dictionary_of_contemporary_english_6th_edition.mdd"
)

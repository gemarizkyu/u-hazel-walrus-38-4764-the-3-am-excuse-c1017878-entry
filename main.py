# The 3 AM Excuse - make.fun entry program.
#
# This program is the whole entry. It loads the one-line excuse a
# hardware wallet gives for refusing to sign a transaction at 3 AM,
# stored beside it in excuse.txt, and writes that line, unchanged,
# to /output/entry.txt, where the sealed gate scorer reads it.
#
# No model calls, no randomness, no clock, no network: the same
# line on every run, so the replay matches the live run exactly.

from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCUSE_FILE = HERE / "excuse.txt"
OUTPUT_FILE = Path("/output/entry.txt")


def load_excuse() -> str:
    """Read the excuse line, resolved from this file's own location."""
    text = EXCUSE_FILE.read_text(encoding="utf-8")
    line = text.strip("\r\n")
    if not line or line.strip() == "":
        raise ValueError("excuse.txt holds no excuse line")
    if line != line.strip():
        raise ValueError("the excuse must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("the excuse must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError(f"excuse is {len(line)} characters, must be 1-200")
    return line


def main() -> None:
    excuse = load_excuse()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(excuse, encoding="utf-8")
    # Read back and confirm the output is byte-identical to the excuse.
    written = OUTPUT_FILE.read_text(encoding="utf-8")
    if written != excuse:
        raise ValueError("read-back of /output/entry.txt differs from excuse")
    print(f"Wrote {len(excuse)} characters to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

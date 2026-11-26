from pathlib import Path

ROOT = Path(r"E:\du-an\Sach AI")
TARGETS = [
    ROOT / "index.html",
    ROOT / "reader.html",
    ROOT / "assets" / "js" / "reader.js",
    ROOT / "assets" / "js" / "library.js",
]

OLD_VER = "20261126-v12"
NEW_VER = "20261126-v13"

for path in TARGETS:
    txt = path.read_text(encoding="utf-8")
    cnt = txt.count(OLD_VER)
    if cnt == 0:
        raise RuntimeError(f"Expected {OLD_VER} in {path}, found 0")
    path.write_text(txt.replace(OLD_VER, NEW_VER), encoding="utf-8")
    print(f"Updated {cnt} occurrence(s) of {OLD_VER} -> {NEW_VER} in {path.relative_to(ROOT)}")

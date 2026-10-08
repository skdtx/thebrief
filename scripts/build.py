#!/usr/bin/env python3
"""Собирает dist/: thebrief.zip (для загрузки скилла) и thebrief-full.md (всё одним файлом для проектов в чатах)."""
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "thebrief"
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

with zipfile.ZipFile(DIST / "thebrief.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(SKILL.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            z.write(f, pathlib.Path("thebrief") / f.relative_to(SKILL))

order = [
    "SKILL.md",
    "references/formats/telegram.md",
    "references/formats/presentation.md",
    "references/formats/one-pager.md",
    "references/cleanup.md",
    "references/finance.md",
    "references/examples.md",
]
parts = ["# TheBrief — все правила одним файлом\n\nСобрано из skills/thebrief. Править нужно исходные файлы, этот файл пересобирается скриптом scripts/build.py.\n"]
for rel in order:
    text = (SKILL / rel).read_text(encoding="utf-8")
    if rel == "SKILL.md" and text.startswith("---"):
        text = text.split("---", 2)[2].lstrip()
    parts.append(f"\n\n<!-- {rel} -->\n\n{text.strip()}\n")
(DIST / "thebrief-full.md").write_text("".join(parts), encoding="utf-8")
print("dist/thebrief.zip, dist/thebrief-full.md")

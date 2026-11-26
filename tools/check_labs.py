#!/usr/bin/env python3
"""Structure check for Orrery Labs repositories. Standard library only.

Checks:
  1. Every lab folder in labs/ has a README.md with the required sections.
  2. Every build page in builds/ names a target and the job it retires.
  3. Every relative Markdown link points at a file that exists.
  4. No file over 5 MB and no text that looks like a credential.
Exit code 0 means pass. Any failure is printed with the file and the reason.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB_SECTIONS = [
    "## What you will be able to do",
    "## Before you start",
    "## Steps",
    "## Check your work",
    "## Known limits",
]
BUILD_FIELDS = ["**Target:**", "**Retire:**", "**Prove it:**"]
MAX_BYTES = 5 * 1024 * 1024
SECRET = re.compile(
    r"(AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}"
    r"|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|AccountKey=[A-Za-z0-9+/=]{40,})"
)
LINK = re.compile(r"\]\(([^)\s]+)\)")
SKIP_DIRS = {".git"}

failures = []


def fail(path, reason):
    failures.append(f"{path.relative_to(ROOT)}: {reason}")


def files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not SKIP_DIRS.intersection(p.relative_to(ROOT).parts):
            yield p


labs = ROOT / "labs"
if labs.is_dir():
    for lab in sorted(d for d in labs.iterdir() if d.is_dir()):
        readme = lab / "README.md"
        if not readme.is_file():
            fail(lab, "lab folder has no README.md")
            continue
        text = readme.read_text(encoding="utf-8")
        if "**Status:**" not in text:
            fail(readme, "missing **Status:** line")
        for section in LAB_SECTIONS:
            if section not in text:
                fail(readme, f"missing section '{section}'")

builds = ROOT / "builds"
if builds.is_dir():
    for page in sorted(builds.glob("*.md")):
        if page.name == "README.md":
            continue
        text = page.read_text(encoding="utf-8")
        for field in BUILD_FIELDS:
            if field not in text:
                fail(page, f"missing field {field}")

for p in files():
    if p.stat().st_size > MAX_BYTES:
        fail(p, "file is over 5 MB; keep large data out of the repository")
    if p.suffix in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}:
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if SECRET.search(text):
        fail(p, "contains text that looks like a credential")
    if p.suffix == ".md":
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            dest = (p.parent / target.split("#", 1)[0]).resolve()
            if not dest.exists():
                fail(p, f"broken link '{target}'")

if failures:
    print(f"FAIL: {len(failures)} problem(s)")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
lab_count = len([d for d in labs.iterdir() if d.is_dir()]) if labs.is_dir() else 0
print(f"PASS: {lab_count} lab folder(s) checked, links and files clean")

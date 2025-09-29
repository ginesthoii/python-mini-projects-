#!/usr/bin/env python3
"""
watermark.py — modern, flexible PDF watermarking (pypdf 6.x)

Features
- Single PDF or whole folder (batch)
- Default watermark (PDF or generated text)
- Any number of per-range rules:
    --rule pages=first,wm=cover.pdf,pos=center,scale=0.9
    --rule pages=2-6,text='DRAFT',opacity=0.15,rotate=35,pos=tr,offset=10 10
    --rule pages=odd,text='CONFIDENTIAL',opacity=0.12,pos=center

Usage (single file):
  python3 watermark.py input.pdf -o output.pdf --text "CONFIDENTIAL" --opacity 0.15 --rotate 45
  python3 watermark.py input.pdf -o output.pdf --wm logo.pdf --pos br --scale 0.5

Usage (per-range rules; default applies to pages not matched by a rule):
  python3 watermark.py input.pdf -o output.pdf \
    --wm logo.pdf --pages all --pos br --scale 0.35 \
    --rule pages=first,text='Company Internal',opacity=0.20,pos=center,rotate=18,scale=0.95 \
    --rule pages=2-6,text='DRAFT',opacity=0.12,pos=tl,offset=16 16

Batch (folder in → folder out, keeps filenames):
  python3 watermark.py --in-dir ./reports --out-dir ./out \
    --text "INTERNAL" --opacity 0.12 --rotate 45 --pos center

Notes
- Opacity requires either a transparent watermark asset *or* using --text
  (we generate a semi-transparent PDF via ReportLab).
- Page selectors: all|first|last|odd|even|1,3,5|2-7|mix (comma-combinable, 1-based in CLI).
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
import tempfile
from typing import Dict, List, Optional, Set, Tuple

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf._page import PageObject  # type: ignore


# ---------- Text watermark generation (ReportLab) ----------
def build_text_watermark_pdf(
    text: str,
    width: float,
    height: float,
    font: str = "Helvetica-Bold",
    font_size: int = 48,
    opacity: float = 0.15,
    rotate: float = 45,
) -> Path:
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import Color
    except Exception as e:
        raise SystemExit(
            f"[error] ReportLab is required for text watermarks: {e}\n"
            "Install with: pip install reportlab"
        )

    tmp = Path(tempfile.mkstemp(suffix=".pdf")[1])
    c = canvas.Canvas(str(tmp), pagesize=(width, height))
    opacity = max(0.0, min(1.0, opacity))
    color = Color(0, 0, 0, alpha=opacity)  # black with alpha

    c.saveState()
    c.setFillColor(color)
    c.setFont(font, font_size)
    c.translate(width / 2, height / 2)
    c.rotate(rotate)
    tw = c.stringWidth(text, fontName=font, fontSize=font_size)
    c.drawString(-tw / 2, -font_size / 2, text)
    c.restoreState()

    c.showPage()
    c.save()
    return tmp


# ---------- Page selection ----------
def parse_pages_arg(pages_arg: str, total_pages: int) -> Set[int]:
    pages_arg = pages_arg.strip().lower()
    if pages_arg == "all":
        return set(range(total_pages))
    selected: Set[int] = set()
    tokens = [t.strip() for t in pages_arg.split(",") if t.strip()]
    for tok in tokens:
        if tok == "first":
            selected.add(0)
        elif tok == "last":
            selected.add(total_pages - 1)
        elif tok == "odd":
            selected |= {i for i in range(total_pages) if (i + 1) % 2 == 1}
        elif tok == "even":
            selected |= {i for i in range(total_pages) if (i + 1) % 2 == 0}
        elif "-" in tok:
            a, b = tok.split("-", 1)
            start = max(1, int(a))
            end = min(total_pages, int(b))
            if start > end:
                start, end = end, start
            selected |= {i - 1 for i in range(start, end + 1)}
        else:
            n = int(tok)
            if not (1 <= n <= total_pages):
                raise ValueError(f"Page {n} out of range 1..{total_pages}")
            selected.add(n - 1)
    return selected


# ---------- Positioning ----------
def compute_translation(
    page: PageObject,
    wm: PageObject,
    position: str,
    offset: Tuple[float, float],
    scale: float,
) -> Tuple[float, float]:
    pw, ph = float(page.mediabox.width), float(page.mediabox.height)
    ww, wh = float(wm.mediabox.width) * scale, float(wm.mediabox.height) * scale
    ox, oy = offset
    position = position.lower()
    if position == "center":
        tx, ty = (pw - ww) / 2 + ox, (ph - wh) / 2 + oy
    elif position == "tl":
        tx, ty = 0 + ox, ph - wh + oy
    elif position == "tr":
        tx, ty = pw - ww + ox, ph - wh + oy
    elif position == "bl":
        tx, ty = 0 + ox, 0 + oy
    elif position == "br":
        tx, ty = pw - ww + ox, 0 + oy
    else:  # 'custom' absolute
        tx, ty = ox, oy
    return tx, ty


# ---------- Rule model ----------
@dataclass
class Rule:
    pages: str
    wm_path: Optional[Path] = None
    text: Optional[str] = None
    position: str = "center"
    offset: Tuple[float, float] = (0.0, 0.0)
    scale: float = 1.0
    rotate: float = 0.0
    opacity: Optional[float] = None  # used only for text


def parse_rule_arg(arg: str) -> Rule:
    """
    Parse --rule 'pages=2-6,text=DRAFT,opacity=0.15,pos=tr,offset=10 20,scale=0.7,rotate=30,wm=logo.pdf'
    Keys:
      pages (required), text, opacity, pos, offset, scale, rotate, wm
    """
    kv: Dict[str, str] = {}
    # split on commas not within quotes
    chunks: List[str] = []
    cur, in_quotes = [], False
    for ch in arg.strip():
        if ch in "\"'":
            in_quotes = not in_quotes
            cur.append(ch)
        elif ch == ',' and not in_quotes:
            chunks.append(''.join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        chunks.append(''.join(cur).strip())

    for c in chunks:
        if "=" not in c:
            raise ValueError(f"Bad rule fragment: {c}")
        k, v = c.split("=", 1)
        kv[k.strip().lower()] = v.strip().strip("'").strip('"')

    if "pages" not in kv:
        raise ValueError("Rule requires pages=...")

    pos = kv.get("pos", "center")
    off = kv.get("offset")
    if off:
        parts = off.split()
        if len(parts) != 2:
            raise ValueError("offset must be two numbers: 'X Y'")
        offset = (float(parts[0]), float(parts[1]))
    else:
        offset = (0.0, 0.0)

    wm = kv.get("wm")
    wm_path = Path(wm) if wm else None

    return Rule(
        pages=kv["pages"],
        wm_path=wm_path,
        text=kv.get("text"),
        position=pos,
        offset=offset,
        scale=float(kv.get("scale", "1.0")),
        rotate=float(kv.get("rotate", "0.0")),
        opacity=float(kv["opacity"]) if "opacity" in kv else None,
    )


# ---------- Core watermarking for one PDF ----------
def apply_watermark_file(
    input_pdf: Path,
    output_pdf: Path,
    default_rule: Rule,
    rules: List[Rule],
) -> None:
    if not input_pdf.exists():
        raise FileNotFoundError(f"Input not found: {input_pdf}")
    if output_pdf.resolve() == input_pdf.resolve():
        raise SystemExit("[error] Output equals input; choose a different -o / out-dir.")

    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()

    # Probe size for text watermarks
    first = reader.pages[0]
    base_w, base_h = float(first.mediabox.width), float(first.mediabox.height)

    def build_wm_page(rule: Rule, page: PageObject) -> PageObject:
        # Choose source: text or wm_path
        if rule.text:
            tmp = build_text_watermark_pdf(
                text=rule.text,
                width=base_w,
                height=base_h,
                opacity=rule.opacity if rule.opacity is not None else 0.15,
                rotate=rule.rotate,
            )
            wm_reader = PdfReader(str(tmp))
            wm_pg = wm_reader.pages[0]
            tmp.unlink(missing_ok=True)
        elif rule.wm_path:
            if not rule.wm_path.exists():
                raise FileNotFoundError(f"Watermark not found: {rule.wm_path}")
            wm_reader = PdfReader(str(rule.wm_path))
            wm_pg = wm_reader.pages[0]
        else:
            # No rule-specific watermark → fall back to default
            if default_rule.text:
                tmp = build_text_watermark_pdf(
                    text=default_rule.text,
                    width=base_w,
                    height=base_h,
                    opacity=(default_rule.opacity if default_rule.opacity is not None else 0.15),
                    rotate=default_rule.rotate,
                )
                wm_reader = PdfReader(str(tmp))
                wm_pg = wm_reader.pages[0]
                tmp.unlink(missing_ok=True)
            elif default_rule.wm_path:
                wm_reader = PdfReader(str(default_rule.wm_path))
                wm_pg = wm_reader.pages[0]
            else:
                raise ValueError("No watermark defined (default or rule).")
        return wm_pg

    total = len(reader.pages)
    # Precompute page sets per rule (0-based indices)
    rule_sets: List[Tuple[Rule, Set[int]]] = [
        (r, parse_pages_arg(r.pages, total)) for r in rules
    ]
    default_pages = parse_pages_arg(default_rule.pages, total)

    for i, page in enumerate(reader.pages):
        # choose the first matching rule; else default if it covers this page; else skip
        chosen: Optional[Rule] = None
        for r, s in rule_sets:
            if i in s:
                chosen = r
                break
        if chosen is None and i in default_pages:
            chosen = default_rule

        if chosen:
            wm_page = build_wm_page(chosen, page)  # PageObject
            tx, ty = compute_translation(
                page, wm_page, chosen.position, chosen.offset, chosen.scale
            )
            t = (
                Transformation()
                .scale(chosen.scale)
                .rotate(chosen.rotate)
                .translate(tx, ty)
            )
            # pypdf 6.x: apply transform at merge time (no clone/add_transformation)
            page.merge_transformed_page(wm_page, t)

        writer.add_page(page)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as f:
        writer.write(f)


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Flexible PDF watermarking (batch + rules).")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("input", nargs="?", type=Path, help="Input PDF (single file mode)")
    src.add_argument("--in-dir", type=Path, help="Directory of PDFs to process (batch)")

    ap.add_argument("-o", "--output", type=Path, help="Output PDF (single file)")
    ap.add_argument("--out-dir", type=Path, help="Output directory (batch mode)")

    # Default watermark (applies to pages specified by --pages unless a rule overrides)
    dm = ap.add_mutually_exclusive_group(required=False)
    dm.add_argument("--wm", type=Path, help="Default watermark PDF (first page used)")
    dm.add_argument("--text", type=str, help="Default text watermark")
    ap.add_argument("--opacity", type=float, help="Default opacity for text watermark 0..1")
    ap.add_argument("--pos", "--position", dest="position", default="center",
                    choices=["center", "tl", "tr", "bl", "br", "custom"])
    ap.add_argument("--offset", nargs=2, type=float, default=(0.0, 0.0), metavar=("X", "Y"))
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--rotate", type=float, default=0.0)
    ap.add_argument("--pages", default="all",
                    help="Default pages: all|first|last|odd|even|1,3,5|2-7|mix (default: all)")

    # Per-range rules (repeatable)
    ap.add_argument("--rule", action="append", default=[],
                    help="Per-range rule, e.g.: "
                         "pages=first,text='CONFIDENTIAL',opacity=0.2,pos=center,scale=0.9 "
                         "| pages=2-6,wm=logo.pdf,pos=tr,offset=10 10,rotate=20,scale=0.6")

    args = ap.parse_args()

    # Build default rule
    default_rule = Rule(
        pages=args.pages,
        wm_path=args.wm,
        text=args.text,
        position=args.position,
        offset=tuple(args.offset),
        scale=args.scale,
        rotate=args.rotate,
        opacity=args.opacity,
    )
    rules = [parse_rule_arg(r) for r in args.rule] if args.rule else []

    # Modes
    if args.input:
        if not args.output:
            raise SystemExit("In single-file mode you must provide -o/--output.")
        apply_watermark_file(args.input, args.output, default_rule, rules)
        print(f"[ok] {args.input.name} → {args.output}")
    else:
        # Batch
        in_dir: Path = args.in_dir
        out_dir: Path = args.out_dir or in_dir / "watermarked"
        out_dir.mkdir(parents=True, exist_ok=True)

        pdfs = [p for p in in_dir.glob("*.pdf") if p.is_file()]
        if not pdfs:
            raise SystemExit(f"[error] No PDFs found in {in_dir}")

        for p in pdfs:
            out = out_dir / p.name
            try:
                apply_watermark_file(p, out, default_rule, rules)
                print(f"[ok] {p.name} → {out}")
            except Exception as e:
                print(f"[fail] {p.name}: {e}")


if __name__ == "__main__":
    main()
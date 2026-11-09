"""Genera artifact.html (versión para claude.ai) a partir de index.html (versión PWA).
Quita solo el bloque de cabecera PWA (manifest, iconos, window.CAZUELA_PWA)."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")
out = re.sub(r'<link rel="manifest".*?<script>window\.CAZUELA_PWA=true;</script>\n', '', src, flags=re.S)
assert "CAZUELA_PWA=true" not in out
(root / "artifact.html").write_text(out, encoding="utf-8")
print("artifact.html escrito")

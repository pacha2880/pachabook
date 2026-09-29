"""Genera web/consejos.js con los 112 consejos de contenido.tex.

Uso (desde la raíz del repo):  py -3 web/generar_consejos.py
Volver a correrlo cada vez que cambien los consejos.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
tex = (RAIZ / "contenido.tex").read_text(encoding="utf-8")

consejos, seccion, en_lista = [], None, False
for linea in tex.splitlines():
    m = re.match(r"\\section\*?\{(.+?)\}", linea)
    if m:
        seccion = m.group(1)
        continue
    if re.search(r"\\begin\{enumerate\}", linea):
        en_lista = True
        continue
    if re.search(r"\\end\{enumerate\}", linea):
        en_lista = False
        continue
    if en_lista:
        m = re.match(r"\s*\\item\s+(.*)", linea)
        if m:
            consejos.append({"seccion": seccion, "texto": m.group(1).strip()})
        elif linea.strip():
            consejos[-1]["texto"] += " " + linea.strip()

js = "// Generado por web/generar_consejos.py a partir de contenido.tex. No editar a mano.\n"
js += "const CONSEJOS = " + json.dumps(consejos, ensure_ascii=False, indent=1) + ";\n"
(RAIZ / "web" / "consejos.js").write_text(js, encoding="utf-8")
print(f"{len(consejos)} consejos -> web/consejos.js")

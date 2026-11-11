"""Genera la versión web del libro a partir de contenido.tex.

Produce:
  libro.html       el libro completo para leer en línea
  web/consejos.js  los 112 consejos (para el "consejo al azar" de index.html)

Uso (desde la raíz del repo):  py -3 web/generar_web.py
Volver a correrlo cada vez que cambie contenido.tex.
"""
import html
import json
import re
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
TEX = RAIZ / "contenido.tex"
MAIN = RAIZ / "main.tex"
PLANTILLA = RAIZ / "web" / "plantilla_libro.html"


# ---------------------------------------------------------------- utilidades

def slug(texto):
    t = texto.lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def sin_comentarios(linea):
    """Quita comentarios LaTeX (% no escapado)."""
    return re.sub(r"(?<!\\)%.*", "", linea)


def reemplazar_comando(texto, nombre, fn):
    """Reemplaza \\nombre{...} (llaves balanceadas, de adentro hacia afuera)."""
    patron = re.compile(r"\\" + nombre + r"\{([^{}]*)\}")
    while True:
        nuevo = patron.sub(lambda m: fn(m.group(1)), texto)
        if nuevo == texto:
            return texto
        texto = nuevo


def enlazar_consejos(texto):
    """'consejo 56', 'consejos del 10 al 12', 'consejos 5 y 6' -> enlaces."""
    def num(n):
        return f'<a class="ref-consejo" href="#consejo-{n}">{n}</a>'

    def fn(m):
        s = m.group(0)
        return re.sub(r"\d+", lambda d: num(d.group(0)), s)

    return re.sub(r"\bconsejos?\s+(?:del\s+)?\d+(?:\s+(?:al|y|a)\s+\d+)?", fn, texto)


class Libro:
    def __init__(self):
        self.citas = {}          # clave -> número de referencia
        self.consejos = []       # [{"n", "seccion", "texto"}]
        self.indice = []         # [(nivel, id, titulo)]

    def en_linea(self, t):
        """Convierte comandos LaTeX en línea a HTML."""
        t = html.escape(t, quote=False)
        t = t.replace("\\&amp;", "&amp;").replace("\\%", "%").replace("\\_", "_")
        t = t.replace("``", "“").replace("''", "”")
        t = t.replace("---", "—").replace("--", "–")
        # Matemática simple: \( ... \) con potencias
        t = re.sub(r"\\\((.*?)\\\)",
                   lambda m: re.sub(r"\^(\w+)", r"<sup>\1</sup>", m.group(1)), t)
        t = reemplazar_comando(t, "url", lambda u: f'<a href="{u if u.startswith("http") else "https://" + u}">{u}</a>')
        t = reemplazar_comando(t, "cite", self._cita)
        for cmd, tag in (("textit", "em"), ("emph", "em"), ("textbf", "strong")):
            t = reemplazar_comando(t, cmd, lambda x, tag=tag: f"<{tag}>{x}</{tag}>")
        t = re.sub(r"\\(scriptsize|small|large|Large|centering|noindent)\b\s*", "", t)
        t = reemplazar_comando(t, "large", lambda x: x)
        # URLs sueltas (bibliografía) que no estén ya dentro de un enlace
        t = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<]+)', r'<a href="\1">\1</a>', t)
        t = t.replace("{", "").replace("}", "")
        return re.sub(r"\s+", " ", t).strip()

    def _cita(self, claves):
        partes = []
        for c in claves.split(","):
            c = c.strip()
            n = self.citas.get(c, "?")
            partes.append(f'<a class="cita" href="#ref-{c}">[{n}]</a>')
        return "".join(partes)


# ---------------------------------------------------------------- conversión

def convertir(tex):
    libro = Libro()
    lineas = [sin_comentarios(l).rstrip() for l in tex.splitlines()]

    # Numeración de la bibliografía (orden de \bibitem)
    for l in lineas:
        m = re.match(r"\s*\\bibitem\{(.+?)\}", l)
        if m:
            libro.citas[m.group(1)] = len(libro.citas) + 1

    salida = []
    parrafo = []
    seccion_actual = None
    i = 0

    def cerrar_parrafo():
        if parrafo:
            texto = libro.en_linea(" ".join(parrafo))
            if texto:
                salida.append(f"<p>{enlazar_consejos(texto)}</p>")
            parrafo.clear()

    def bloque(fin):
        """Lee líneas hasta \\end{fin}; devuelve la lista de líneas internas."""
        nonlocal i
        contenido = []
        i += 1
        while not re.match(r"\s*\\end\{" + fin + r"\}", lineas[i]):
            contenido.append(lineas[i])
            i += 1
        return contenido

    while i < len(lineas):
        l = lineas[i]
        s = l.strip()

        if not s or s in ("{", "}") or re.fullmatch(r"\\(pagebreak|clearpage|newpage)", s) \
                or s.startswith("\\vspace"):
            cerrar_parrafo()

        elif m := re.match(r"\\(sub)?section\*?\{(.+)\}", s):
            cerrar_parrafo()
            titulo = libro.en_linea(m.group(2))
            nivel = 3 if m.group(1) else 2
            ident = slug(re.sub(r"<[^>]+>", "", titulo))
            if nivel == 2:
                seccion_actual = re.sub(r"<[^>]+>", "", titulo)
                if salida:
                    salida.append("</section>")
                salida.append(f'<section id="{ident}">')
            libro.indice.append((nivel, ident, titulo))
            if nivel == 2:
                salida.append(f"<h2>{titulo}</h2>")
            else:
                salida.append(f'<h3 id="{ident}">{titulo}</h3>')

        elif s.startswith("\\begin{center}"):
            cerrar_parrafo()
            titulo = re.sub(r"<[^>]+>", "", libro.en_linea(" ".join(bloque("center"))))
            ident = "introduccion"
            seccion_actual = "Introducción"
            salida.append("</section>")
            salida.append(f'<section id="{ident}">')
            libro.indice.append((2, ident, "Introducción"))
            salida.append(f'<h2 class="titulo-intro">{titulo}</h2>')

        elif s.startswith("\\begin{flushright}"):
            cerrar_parrafo()
            filas = " ".join(bloque("flushright")).split("\\\\")
            filas = [libro.en_linea(f) for f in filas if f.strip()]
            salida.append('<p class="firma">' + "<br>".join(filas) + "</p>")

        elif s.startswith("\\begin{enumerate}") or s.startswith("\\begin{itemize}"):
            cerrar_parrafo()
            tipo = "enumerate" if "enumerate" in s else "itemize"
            items = []
            for linea in bloque(tipo):
                if m := re.match(r"\s*\\item\s*(.*)", linea):
                    items.append(m.group(1))
                elif linea.strip() and items:
                    items[-1] += " " + linea.strip()
            if tipo == "enumerate":
                salida.append('<ol class="consejos">')
                for it in items:
                    n = len(libro.consejos) + 1
                    texto = libro.en_linea(it)
                    libro.consejos.append({"n": n, "seccion": seccion_actual,
                                           "texto": re.sub(r"<[^>]+>", "", texto)})
                    salida.append(
                        f'<li id="consejo-{n}"><a class="num" href="#consejo-{n}" '
                        f'aria-label="Enlace al consejo {n}">{n}</a>'
                        f"<span>{enlazar_consejos(texto)}</span></li>")
                salida.append("</ol>")
            else:
                salida.append('<ul class="bonus">')
                salida += [f"<li>{libro.en_linea(it)}</li>" for it in items]
                salida.append("</ul>")

        elif s.startswith("\\begin{figure}"):
            cerrar_parrafo()
            interno = " ".join(bloque("figure"))
            img = re.search(r"\\includegraphics(?:\[.*?\])?\{(.+?)\}", interno).group(1)
            resto = re.sub(r"\\includegraphics(?:\[.*?\])?\{.+?\}", "", interno)
            fuente = libro.en_linea(resto)
            ancho, alto = Image.open(RAIZ / img).size
            salida.append(f'<figure><img src="{img}" width="{ancho}" height="{alto}" alt="Gráfico de estadísticas de la '
                          f'regional latinoamericana ICPC 2024" loading="lazy">'
                          f"<figcaption>Fuente: {fuente}</figcaption></figure>")

        elif s.startswith("\\begin{thebibliography}"):
            cerrar_parrafo()
            refs, actual = [], None
            for linea in bloque("thebibliography"):
                if m := re.match(r"\s*\\bibitem\{(.+?)\}\s*(.*)", linea):
                    actual = [m.group(1), m.group(2)]
                    refs.append(actual)
                elif linea.strip() and actual:
                    actual[1] += " " + linea.strip()
            salida.append("</section>")
            salida.append('<section id="referencias">')
            libro.indice.append((2, "referencias", "Referencias"))
            salida.append("<h2>Referencias</h2>")
            salida.append('<ol class="referencias">')
            salida += [f'<li id="ref-{k}">{libro.en_linea(v)}</li>' for k, v in refs]
            salida.append("</ol>")

        elif s.endswith("\\\\"):
            parrafo.append(s[:-2])
            cerrar_parrafo()
        else:
            parrafo.append(s)
        i += 1

    cerrar_parrafo()
    salida.append("</section>")
    return libro, "\n".join(salida)


def indice_html(indice):
    partes, abierta = ["<ol>"], False
    for nivel, ident, titulo in indice:
        if nivel == 2:
            if abierta:
                partes.append("</ol></li>")
                abierta = False
            elif len(partes) > 1:
                partes.append("</li>")
            partes.append(f'<li><a href="#{ident}">{titulo}</a>')
        else:
            if not abierta:
                partes.append("<ol>")
                abierta = True
            partes.append(f'<li><a href="#{ident}">{titulo}</a></li>')
    partes.append("</ol></li>" if abierta else "</li>")
    partes.append("</ol>")
    return "\n".join(partes)


def epigrafe(libro):
    """Toma el epígrafe (quote + autor) de la sección EPÍGRAFE de main.tex."""
    tex = MAIN.read_text(encoding="utf-8")
    m = re.search(r"EPÍGRAFE.*?\\begin\{quote\}(.*?)\\end\{quote\}\s*\\hfill\s*--\s*(.+?)\n", tex, re.S)
    if not m:
        return ""
    frase = libro.en_linea(m.group(1))
    autor = libro.en_linea(m.group(2))
    return (f'<figure class="epigrafe"><blockquote><p>{frase}</p></blockquote>'
            f"<figcaption>— {autor}</figcaption></figure>")


def main():
    libro, cuerpo = convertir(TEX.read_text(encoding="utf-8"))
    cuerpo = epigrafe(libro) + "\n" + cuerpo

    pagina = PLANTILLA.read_text(encoding="utf-8")
    pagina = pagina.replace("{{INDICE}}", indice_html(libro.indice))
    pagina = pagina.replace("{{CONTENIDO}}", cuerpo)
    (RAIZ / "libro.html").write_text(pagina, encoding="utf-8")

    consejos = [{"seccion": c["seccion"], "texto": c["texto"]} for c in libro.consejos]
    js = "// Generado por web/generar_web.py a partir de contenido.tex. No editar a mano.\n"
    js += "const CONSEJOS = " + json.dumps(consejos, ensure_ascii=False, indent=1) + ";\n"
    (RAIZ / "web" / "consejos.js").write_text(js, encoding="utf-8")

    print(f"libro.html: {len(libro.indice)} entradas de índice, {len(libro.consejos)} consejos")


if __name__ == "__main__":
    main()

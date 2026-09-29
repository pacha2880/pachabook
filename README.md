# Programación Competitiva Universitaria

**112 consejos para dominar la ICPC**, por Rodrigo Salguero.

Guía de bolsillo con consejos prácticos para el entrenamiento y la competencia en programación competitiva universitaria (ICPC): desde los primeros pasos, pasando por el entrenamiento individual y en equipo, hasta qué hacer antes, durante y después de una competencia.

📖 **[Ver el PDF](pachabook.pdf)** · 🌐 **[Página web](https://pacha2880.github.io/pachabook/)** · 📚 **[Leer en línea](https://pacha2880.github.io/pachabook/libro.html)**

## Contenido

- Presentación
- Prólogo
- Inicio
- Entrenamiento individual
- Entrenamiento en equipo
- Antes de la competencia
- Durante la competencia (simulación)
- Durante la competencia (competencia real)
- Después de la competencia
- Bonus y Epílogo

## Archivos

| Archivo | Descripción |
|---|---|
| `main.tex` | Documento principal: formato, tapa, epígrafe y contratapa |
| `contenido.tex` | Texto del libro |
| `tapa.png`, `contratapa.png` | Tapa y contratapa (incluyen 3 mm de sangrado) |
| `aceptados.png`, `envios.png` | Imágenes usadas en el contenido |
| `pachabook.pdf` | Libro compilado |
| `index.html`, `libro.html`, `web/` | Página web (GitHub Pages). Tras cambiar `contenido.tex`: `py -3 web/generar_web.py` |

## Compilar

Se compila con **XeLaTeX** (dos pasadas, para las referencias):

```bash
xelatex -jobname=pachabook main.tex
xelatex -jobname=pachabook main.tex
```

También funciona en Overleaf, eligiendo XeLaTeX como compilador.

Tamaño de página: cuarto de hoja oficio (10.8 × 13.95 cm).

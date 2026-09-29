# Programación Competitiva Universitaria

**112 consejos para dominar la ICPC**, por Rodrigo Salguero.

Guía de bolsillo con consejos prácticos para el entrenamiento y la competencia en programación competitiva universitaria (ICPC): desde los primeros pasos, pasando por el entrenamiento individual y en equipo, hasta qué hacer antes, durante y después de una competencia.

📖 **[Ver el PDF](https://pacha2880.github.io/pachabook/pachabook.pdf)** · 🌐 **[Página web](https://pacha2880.github.io/pachabook/)** · 📚 **[Leer en línea](https://pacha2880.github.io/pachabook/libro.html)**

🖨️ Para imprenta: **[PDF sin tapa ni contratapa](https://pacha2880.github.io/pachabook/pachabook-sin-tapas.pdf)** (interior, con las páginas en blanco intencionales)

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
| `pachabook-sin-tapas.tex` | Genera el PDF sin tapa ni contratapa (activa `\sintapas` y carga `main.tex`) |
| `tapa.jpg`, `contratapa.jpg` | Tapa y contratapa (CMYK, 300 dpi, tamaño exacto de página) |
| `aceptados.png`, `envios.png` | Imágenes usadas en el contenido |
| `index.html`, `web/` | Página web (GitHub Pages); `libro.html` se genera desde `contenido.tex` |

## Publicación automática

Cada push a `main` compila los PDF (completo y sin tapas), genera la web y la publica en GitHub Pages
(ver [`.github/workflows/publicar.yml`](.github/workflows/publicar.yml)).
Basta con editar `contenido.tex` y hacer push; el avance se ve en la pestaña **Actions**.

## Compilar en local (opcional, para revisar antes de subir)

Con **XeLaTeX**, dos pasadas (para las referencias):

```bash
xelatex -jobname=pachabook main.tex
xelatex -jobname=pachabook main.tex
xelatex pachabook-sin-tapas.tex   # opcional, dos veces
py -3 web/generar_web.py
```

También funciona en Overleaf, eligiendo XeLaTeX como compilador.
Los archivos generados (`pachabook.pdf`, `pachabook-sin-tapas.pdf`, `libro.html`, `web/consejos.js`) no se suben al repositorio.

Tamaño de página: cuarto de hoja carta (10.8 × 13.95 cm).

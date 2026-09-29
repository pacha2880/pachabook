# pachabook

Libro *Programación Competitiva Universitaria: 112 consejos para dominar la ICPC* (Rodrigo Salguero, Equipo ICPC – UMSS) en LaTeX, más su sitio web.
Web publicada: https://pacha2880.github.io/pachabook/

## Archivos

- `main.tex`: formato, tapa, epígrafe y contratapa; hace `\input{contenido}`.
- `pachabook-sin-tapas.tex`: define `\sintapas` y carga `main.tex`; sale el libro sin tapa ni contratapa (para la imprenta), con las mismas páginas en blanco.
- `contenido.tex`: todo el texto (presentación, prólogo, consejos, bonus, epílogo, bibliografía).
- `tapa.jpg`, `contratapa.jpg`: versión final del diseñador, CMYK, 300 dpi, tamaño exacto de página (**sin sangrado**). No retocarlas.
- `index.html`: portada web, escrita a mano.
- `web/generar_web.py` + `web/plantilla_libro.html`: generan `libro.html` y `web/consejos.js` desde `contenido.tex` (el epígrafe lo toman de `main.tex`).
- `web/tapa.jpg`: copia web de la tapa (sin sangrado), hecha a mano.

## Publicación

- Cada push a `main` ejecuta `.github/workflows/publicar.yml`: compila `pachabook.pdf` y `pachabook-sin-tapas.pdf` (XeLaTeX), corre `generar_web.py` y publica en GitHub Pages.
- `pachabook.pdf`, `pachabook-sin-tapas.pdf`, `libro.html` y `web/consejos.js` son generados y están en `.gitignore`: **no commitearlos**.
- Local (Windows): `xelatex -jobname=pachabook main.tex` (dos veces) y `py -3 web/generar_web.py`. `gh` está instalado y autenticado.

## Decisiones que no hay que revertir

- La fuente TeX Gyre Heros se carga por nombre de archivo (`texgyreheros-*.otf`); por nombre de familia no compila en el CI (Linux).
- Tapa y contratapa se colocan con `eso-pic` (`\paginaimagen`); con TikZ salían desfasadas.
- La contratapa se fuerza a página par. Los consejos son una sola lista continua (`resume=icpc`), del 1 al 112.
- Presentación: versión extendida de Leticia Blanco y Vladimir Costas, sin su tercer párrafo (redundaba). La versión corta se descartó porque repite la contratapa.
- Portada web: "Consejo del día" (mismo consejo para todos ese día) con el botón "🎲 Otro consejo" **arriba** de la tarjeta, para que no se mueva.
- El PDF se abre en la misma pestaña (sin `target="_blank"` ni `download`).

## Lo que no se actualiza solo

- Si cambia la cantidad de consejos, buscar "112" en todo el repo (`index.html`, `contenido.tex`) y avisar que la tapa también lo dice.
- Si cambia `tapa.jpg`, regenerar `web/tapa.jpg` (convertir a RGB, 640 px de ancho).
- El texto de "Sobre el libro" en `index.html` es el de la contratapa: si cambia uno, actualizar el otro.
- `generar_web.py` solo convierte los comandos LaTeX que el libro usa hoy. Si se agrega uno nuevo (tablas, notas al pie, fórmulas), adaptar el conversor y revisar `libro.html`.

## Pendiente

- Falta el archivo de tapa para imprenta: una sola pieza contratapa + lomo + tapa, con 3 mm de sangrado. Lo ideal es que lo arme el diseñador.

## Forma de trabajo

- Todo en español, incluidos los commits.
- Hacer commit o push solo cuando el usuario lo pida.
- Revisar visualmente antes de entregar. Edge headless no baja de ~500 px de ancho: para ver el celular, usar un iframe de 390 px.

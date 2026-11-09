# Cazuela – instrucciones para Claude

App de menú semanal para el Lidl de Paiporta (Valencia). Usuario: David, habla español; todo lo que veas y escribas para él, en español.

## Archivos
- `index.html`: la app (PWA). Contiene el catálogo `ING` (id → [nombre, pasillo, tamaño envase, unidad, precio €, flags]), las recetas `BASE_RECIPES` y la constante `const DATA = {...}` con las ofertas embebidas.
- `data.json`: misma estructura que `DATA`. La PWA lo descarga al abrirse, así que es lo que hace llegar las ofertas nuevas al móvil.
- `tools/make_artifact.py`: genera `artifact.html` (versión sin cabecera PWA) para publicar en claude.ai.
- Artifact en claude.ai: slug `749bc5fa-6ba4-4ba7-94af-cf97860cc784`.

## Formato de DATA / data.json
```
{ "version": "AAAA-MM-DD",
  "prices": { "<id ING>": <precio normal corregido> },
  "ingredients": { "<id nuevo>": ["Nombre","Pasillo",tamaño,"g|ml|ud",precio,"flags"] },
  "recipes": [ { id, name, min, kcal, prot, ings:[[idING, cantidad por persona]], steps:[...], opcional light/lunch/fresh/need } ],
  "folleto": { "id": "AAAA-MM-DD (lunes de inicio)", "name": "Folleto D–D mes",
               "items": { "<id ING>": { "price": €, "pack": tamaño en la unidad del ING, "from": "AAAA-MM-DD", "until": "AAAA-MM-DD", "plus": true si es con Lidl Plus, "note": "texto corto" } } } }
```
Pasillos válidos: Fruta y verdura, Panadería, Carne, Pescado, Huevos y lácteos, Refrigerados, Legumbres y conservas, Pasta, arroz y cereales, Despensa, Congelados, Otros. Flags: m carne, f pescado, d lácteo, e huevo, g gluten, n frutos secos, p básico de despensa.

## Actualización semanal (tarea de los domingos)
1. En el navegador integrado abre https://www.lidl.es/c/descubre-nuevas-ofertas-cada-semana-folletos-lidl/s10087402 y localiza el enlace "FOLLETO ALIMENTACIÓN" de la semana que empieza el lunes siguiente. Si sale el aviso de cookies, pulsa RECHAZAR.
2. En la página del folleto, con JavaScript: `fetch("https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=<slug del folleto>&region_id=0&region_code=0")` y lee `flyer.pages[].altText` y `keyWords` para ver qué hay en cada página.
3. Para las páginas con productos que encajan con ingredientes de `ING` (o alternativas claras), cambia de página con `history.pushState` a `.../view/flyer/page/N` + `dispatchEvent(new PopStateEvent("popstate"))` y haz zoom de captura para leer precio, precio anterior, tamaño, fechas y si es "Con Lidl Plus". Los números de keyWords son ambiguos: confirma siempre con la imagen.
4. Actualiza `folleto` en `data.json` y en la constante `DATA` de `index.html` (mismo contenido). Ajusta `prices` si ves un precio normal (sin tachar) distinto del catálogo. Añade `ingredients`/`recipes` solo si hay un producto nuevo de alimentación básica que encaje con cocina casera.
5. Comprueba la sintaxis (extraer el `<script>` y `node --check`), haz commit y push a `main`.
6. `python3 tools/make_artifact.py` y publica `artifact.html` como `index.html` del artifact (publish_files con slug, base_version de get_artifact, modo patch).
7. Envía a David un resumen corto: las 5–8 ofertas más útiles con precio y fechas, y qué requiere Lidl Plus.
Si el navegador no está disponible (ordenador apagado o app cerrada), no inventes ofertas: avisa a David de que mande capturas del folleto.

# Tokens de design

- `tokens.dtcg.json`: formato W3C Design Tokens (camadas `ref` → `sys` → `comp`). É a fonte de verdade.
- `tokens.css`: o mesmo, como CSS custom properties. Tema claro e variante de alto contraste (`data-contrast="high"` ou `prefers-contrast: more`).

Gerados a partir da cor-semente `#4A47C2` com a biblioteca `@material/material-color-utilities` (v0.3.0).
Todos os pares de texto e de contorno foram verificados: AA (4,5:1 texto, 3:1 contornos) em claro e em alto contraste.
Ver `docs/DESIGN-RULES.md`.

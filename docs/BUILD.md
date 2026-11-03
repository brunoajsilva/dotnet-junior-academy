# Gerar e publicar o site

## Requisitos

- Python 3.9 ou superior (só biblioteca standard).
- Para os testes: Node 18+ e `npm i playwright` (uma vez), mais `npx playwright install chromium`.

## Comandos

```bash
python3 src/validate.py content/modules/<id>.json      # valida um módulo
python3 src/build.py --out index.html                  # gera o site completo
node src/tests/smoke.js index.html                     # abre todas as páginas, mobile e desktop
```

O `build.py` lê `content/modules/*.json` (ignora os que começam por `_`), valida cada um e para se algum for inválido.

## O que o build junta

1. Módulos da base: Academia (`src/mods.py`), C# e .NET (`src/m1.json`, `src/m2.json`), Autenticação (`src/mod_auth.py`).
2. Módulos novos (`content/modules/*.json`), por ordem alfabética do nome de ficheiro.
3. Projeto final (`src/mod4_bank.py`, gerado por `src/asm.py` a partir de `m4_head.py`, `m4_tail.py` e `m4_stories.py`).
4. O modelo `src/tpl.html` (layout, CSS, JavaScript), onde os dados são injetados.

Para mudar a **ordem** de módulos novos, prefixa o nome do ficheiro (`10-logging.json`, `20-efcore.json`).

## Publicar

O GitHub Pages serve o `index.html` na raiz do ramo `main`.

```bash
git add index.html content/ src/
git commit -m "Add module: <tema>"
git push
```

A publicação demora cerca de um a dois minutos.

## Notas

- `src/tests/smoke.js` falha se uma página tiver erro de JavaScript, não tiver título, ou tiver scroll horizontal (mobile 400 px).
- O estado do aluno fica em `localStorage` (`academia-dotnet-v1`). Mudar ids de lições apaga o progresso dessas lições.

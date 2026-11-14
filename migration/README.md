# Migração para Starlight

Pasta temporária com tudo o que é preciso para migrar a academia do motor próprio para Starlight. É apagada na última fase.

- `PLAN.md`: o guião, fase a fase. Começa aqui.
- `prompts/fase-0.md` a `prompts/fase-5.md`: o texto a colar no Claude Code no início de cada fase.
- `tools/convert.ts`: gera o site novo e a solução de referência a partir de `content/`.
- `tools/verify.ts`: confirma que nada se perdeu na conversão.
- `templates/site/`: o site Starlight vazio, com a configuração da academia.
- `templates/ci/`: modelos do pipeline (Azure DevOps e GitHub Actions).
- `out/` (gerada): relatório da conversão, correspondência de URLs e correções ao C#.

Antes da fase 1, preenche os parâmetros no ponto 2 do `PLAN.md`.

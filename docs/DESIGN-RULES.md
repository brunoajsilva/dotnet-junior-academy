# Regras de design (para quem escreve conteúdo)

**Quem escreve conteúdo não decide design.** O site aplica o estilo sozinho a cada tipo de lição.
Este documento explica o que isso significa na prática e onde vivem os tokens.

## O que acontece quando acrescentas um módulo

- Aparece no menu do topo, antes do "Projeto final", com um número atribuído automaticamente.
- Recebe uma cor própria, escolhida de uma paleta de seis cores já validada para contraste (`--c-x0` a `--c-x5`).
- Cada tipo de lição (`code`, `cards`, `table`, `exercise`) tem aparência fixa, os blocos de código têm botão "Copiar", e o quiz tem feedback correto e incorreto.
- O progresso do aluno (lições vistas, quiz) aparece no menu lateral e na barra de topo sem trabalho extra.

## O que não fazes

- Não escreves CSS, HTML, cores nem tamanhos. Se sentires que precisas, o pedido é de design, não de conteúdo.
- Não alteras `src/tpl.html`. Se um tipo de lição novo faria falta, descreve-o ao utilizador (para que serve, que campos teria) e pára.

## Fundações de design (Material Design 3)

O site segue o Material Design 3, **só tema claro**, com variante de alto contraste.

- `design/tokens.dtcg.json`: tokens no formato W3C Design Tokens, em três camadas: `ref` (valores base) → `sys` (papéis: `primary`, `surface`, `outline`...) → `comp` (componentes).
- `design/tokens.css`: os mesmos tokens como CSS custom properties (`--md-sys-color-primary`...).
- Regras: nenhum valor visual solto; contraste mínimo AA (4,5:1 para texto, 3:1 para contornos de controlos); alvos de toque com pelo menos 24 px; foco sempre visível; sem animações com `prefers-reduced-motion`.
- Estado: os tokens estão em validação. O `src/tpl.html` ainda usa nomes herdados (`--accent`, `--surface`...) mapeados para estes papéis.

## Pedidos de design: como tratar

Se o utilizador pedir uma alteração visual, trabalha em `src/tpl.html`, usa apenas tokens, e corre `node src/tests/smoke.js index.html`.
Antes de pedir aprovação, verifica o contraste nos pares novos e mostra uma captura.

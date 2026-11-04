# Regras de design

**Quem escreve conteúdo não decide design.** O site aplica o estilo sozinho a cada tipo de lição. Este documento explica o que isso significa e onde vive o CSS.

## O que acontece quando acrescentas um módulo

- Aparece nos menus, antes do "Projeto final", com um número atribuído pela ordem do manifesto.
- Recebe uma cor própria, escolhida de uma paleta de seis cores já validada para contraste (`--c-x0` a `--c-x5`, em `src/styles/tokens.css`).
- Cada tipo de lição (`code`, `cards`, `table`, `exercise`) tem aparência fixa, os blocos de código têm botão "Copiar", e o quiz tem feedback correto e incorreto.
- O progresso do aluno (lições vistas, quiz) aparece no menu lateral sem trabalho extra.

## O que não fazes ao escrever conteúdo

- Não escreves CSS, HTML, cores nem tamanhos. Se sentires que precisas, o pedido é de design, não de conteúdo.
- Se um tipo de lição novo fizesse falta, descreve-o ao utilizador (para que serve, que campos teria) e pára.

## Onde vive o CSS

Ver `docs/ARCHITECTURE.md` para a lista de ficheiros. Em resumo: `src/styles/tokens.css` (variáveis), `src/styles/base.css`, `src/styles/layout.css`, um ficheiro por componente em `src/styles/components/`, páginas em `src/styles/pages/`.

Regras para quem altera CSS:
- **Sem valores soltos**: cores, fontes e raios vêm de variáveis em `tokens.css`. Se falta uma, acrescenta-a lá.
- **Um componente, um ficheiro.** O que é específico de um componente não vai para `base.css` nem `layout.css`.
- Seletores curtos (no máximo três níveis) e sem `!important` (a exceção é `accessibility.css`).
- Media queries no fim do ficheiro do componente a que pertencem.
- Contraste mínimo AA (4,5:1 para texto, 3:1 para contornos de controlos); alvos de toque com pelo menos 24 px; foco sempre visível; sem animações com `prefers-reduced-motion`.
- Só tema claro.

## Material Design 3

O site segue o Material Design 3 (tema claro). Os papéis de cor (`--md-primary`, `--md-surface`, `--md-outline`...) estão em `src/styles/tokens.css`; os nomes antigos (`--accent`, `--surface`, `--line`...) são aliases para esses papéis e continuam a funcionar.

`design/` guarda as **fundações** de design geradas à parte (`tokens.dtcg.json` no formato W3C e `tokens.css`, camadas `ref`, `sys`, `comp`). Ainda não estão ligadas ao site: a migração de `src/styles/tokens.css` para esses nomes é um passo futuro.

## Pedidos de design: como tratar

Se o utilizador pedir uma alteração visual, trabalha no CSS do componente, usa apenas tokens, corre `npm test` e mostra uma captura. Verifica o contraste nos pares de cor novos.

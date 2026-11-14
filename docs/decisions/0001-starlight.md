# 0001. Site feito com Starlight

Data: 2026-11-14. Estado: aceite.

## Contexto

A academia foi primeiro um site Astro com motor próprio: o conteúdo estava em YAML (com ficheiros de código ao lado), validado por schemas, e renderizado por código à medida, com um cliente que guardava o progresso no browser. Para passar a academia para um repositório interno da empresa, o projeto tinha de ser o mais simples possível e fácil de manter à mão. O motor próprio tinha cerca de 3.000 linhas de TypeScript e 3.700 de CSS, que alguém teria de conhecer para mexer no conteúdo.

## Decisão

- O site passa a Starlight, só com tema claro e sem pesquisa, com uma página Markdown por capítulo. Blocos de código com botão de copiar, avisos e menu lateral vêm de origem.
- Os exemplos de código, incluindo os do projeto final, ficam dentro das páginas, em blocos de código. Não há soluções .NET no repositório.
- As versões do Astro (7.4.5) e do Starlight (0.43.1) estão fixas no `package.json`. Atualizam-se de propósito, num ramo próprio.
- O pipeline compila o site.

## Consequências

Ganhou-se:

- Qualquer pessoa edita uma lição num ficheiro de texto, sem schemas nem passos de geração.
- Não há motor próprio para manter. Atualizar o Starlight traz melhorias de graça.

Perdeu-se:

- A pesquisa e o modo escuro, por decisão: o site só tem tema claro e não tem pesquisa.
- A garantia de que o código C# do projeto final compila: não há solução .NET nem testes no repositório.
- O progresso do aluno guardado no browser (marcar lições como vistas).
- O quiz: foi retirado, os capítulos terminam nos exercícios e nas ideias para praticar.
- O plano pessoal do aluno e a árvore de ficheiros clicável com painel lateral. A árvore passou a ser a do Starlight, com a descrição de cada ficheiro.
- Os ids estáveis e o ficheiro `ids.lock`, que só serviam para o progresso.
- Os URLs mudaram. A correspondência entre os antigos e os novos está em [0001-routes.json](0001-routes.json).

## Alternativas avaliadas

Manter o motor próprio e simplificá-lo; usar apenas Markdown sem framework (por exemplo, uma wiki do repositório); outros geradores de documentação. O Starlight foi o que dava mais com menos código a manter.

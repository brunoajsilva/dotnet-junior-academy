# Guia de estilo e de escrita

## Idioma e tom

- PT-PT com o acordo ortográfico (projeto, ação, ótimo). Trata o aluno por **tu**.
- Frases curtas e diretas. Uma ideia por frase. Voz ativa.
- Sem emojis, sem exclamações, sem humor forçado, sem «vamos mergulhar» nem «neste fascinante tema».
- Evita travessões longos no meio da frase: usa vírgulas ou duas frases.
- Termos técnicos ficam em inglês quando são o nome estabelecido: Dependency Injection, middleware, controller, handler, endpoint, claim, token, record, migration, scoped. Explica-os na primeira vez que aparecem.
- Não traduzas nomes de APIs, comandos ou tipos (`ILogger`, `dotnet new`, `Task.WhenAll`).

## Código

- Tudo em inglês: nomes, comentários, mensagens de log e de exceção.
- Domínio de exemplo: banco. Entidades habituais: `Customer`, `Account`, `Transaction`; campos `Number`, `Balance`, `TaxId` (NIF).
- Dados inventados e evidentes: `ana@example.com`, `AC-123456`. Nunca dados reais.
- Dinheiro em `decimal` (sufixo `m` nos literais). Datas em UTC.
- Exemplo pequeno e completo: cabe num ecrã e mostra só o que a lição ensina.
- Classes: uma por ficheiro quando o exemplo mostra vários ficheiros. Sem `record` nos exemplos do projeto final.
- Comandos de terminal: só `dotnet`, `git` e instalação de dependências. Pedidos HTTP: Bruno.
- Nunca incluas chaves, passwords ou segredos reais. Para exemplos de configuração, usa um valor óbvio de exemplo.

## Estrutura pedagógica

- **Lição**: uma ideia. 2 a 4 pontos-chave. Um exemplo. Um bloco «Saber mais» quando há profundidade que não cabe no resto.
- **Armadilha** (`:::caution[Armadilha]`): o erro que um júnior realmente comete, numa frase.
- **Experimenta** (`:::tip[Experimenta]`): algo que o aluno faz em menos de 2 minutos para ver o efeito.
- **Exercício**: 3 a 6 passos verificáveis («o endpoint devolve 404», não «perceber o endpoint»). Dá a pista sem dar a solução.
- **Quiz**: perguntas de compreensão, não de memória de sintaxe. Opções erradas plausíveis. A explicação diz porquê.
- **Progressão**: cada capítulo usa o anterior. Não introduzas dois conceitos novos na mesma lição.

## O que nunca escrever

- Nomes de empresas, clientes ou colegas. Logótipos e marcas como identidade.
- Postman (a academia usa Bruno).
- Promessas de duração («em 5 minutos») nos títulos.
- Texto copiado da documentação oficial. Reformula e cita o link no fim da lição.
- Afirmações sem confirmação sobre versões, preços ou suporte. Se não confirmaste, não escrevas.

## Checklist de qualidade

Marca tudo antes de entregar:

- [ ] `npm run build` em `site/` termina com `Complete!`.
- [ ] Cada capítulo tem um quiz de 3 a 6 perguntas.
- [ ] Nenhum exemplo de código é maior do que um ecrã.
- [ ] Todo o código está em inglês e usa `decimal` para dinheiro.
- [ ] Nenhum texto tem emojis.
- [ ] Os links para a documentação são oficiais e abrem.
- [ ] As respostas certas do quiz não estão todas na mesma posição.
- [ ] No resumo final disseste o que **não** conseguiste verificar (por exemplo, «o código não foi compilado»).

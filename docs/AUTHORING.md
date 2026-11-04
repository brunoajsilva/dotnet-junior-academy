# Do tema ao módulo

Receita para transformar "quero um módulo sobre X" num módulo publicado. Segue por ordem.

## 1. Perceber o pedido

Antes de escrever, fixa por escrito (no resumo final, não nos ficheiros):

- **Tema** e **ideia central**: o que o aluno consegue fazer no fim que não fazia antes.
- **Público**: programador júnior a médio, já fez os módulos C# e .NET da academia. Não repitas o que lá está.
- **Versões**: .NET 10 e C# 14, salvo indicação contrária.
- **Âmbito**: um módulo = 2 a 5 capítulos. Cada capítulo = 3 a 14 lições. Se o tema é maior, propõe dividir em dois módulos.

Se faltar informação que muda o conteúdo (versão, biblioteca, nível), faz **uma** pergunta curta. Senão, assume e regista a assunção.

## 2. Verificar os factos

Para qualquer afirmação técnica que não sabes de cor, confirma na documentação oficial (learn.microsoft.com) antes de a escreveres.
Nunca inventes nomes de métodos, pacotes ou comandos. Cada módulo termina com links oficiais (`wrapUp.docs`).

## 3. Esboçar o módulo

Antes dos ficheiros, escreve o esboço como tabela:

| Capítulo | Lição | Tipo | Ideia única |
|---|---|---|---|
| 1. Registar com ILogger | ILogger e mensagens estruturadas | code | marcadores nomeados |
| | Níveis de log | table | quando usar cada nível |
| | Registar uma operação | exercise | aplicar no handler |

Regras de composição:
- Abre cada capítulo com uma lição `code` ou `cards` (o conceito), sem exercício logo à cabeça.
- Alterna explicação e prática: no máximo 4 lições seguidas sem `exercise`.
- Fecha o capítulo com um `exercise` que junta o que foi visto, e depois o quiz.
- O último capítulo pode ter um `exercise` com enunciado completo (a "mini-aplicação").

## 4. Criar os ficheiros

O `id` é curto, em minúsculas, sem espaços (`efcore`, `logging`, `docker`). O caminho mais rápido:

```bash
npm run new:module -- <id> "Título completo" "Nome curto"     # cria content/_drafts/<id>/
npm run new:lesson -- <id> <id>-1 <id>-1-2 "Título" code       # junta uma lição a um capítulo
```

Ou copia `content/_examples/logging/` para `content/modules/<id>/` e adapta.

```
content/modules/<id>/
  module.yaml                        metadados, lista de capítulos e o fecho (wrapUp)
  chapters/<id>-1/
    chapter.yaml                     lista de lições ($ref) e quiz do capítulo
    <id>-1-1.yaml                    uma lição por ficheiro
    code/<id>-1-1.cs                 um ficheiro por exemplo de código
  chapters/<id>-2/ ...
```

Ids obrigatórios e únicos:
- capítulos: `<id>-1`, `<id>-2`... (e a pasta tem o mesmo nome)
- lições: `<id>-1-1`, `<id>-1-2`, `<id>-2-1`...

Escreve o código em ficheiros `.cs` (ou `.sh`, `.json`...) com o realce do teu editor e referencia-os com `codeFile`. Os campos estão em `docs/CONTENT-SCHEMA.md`.

## 5. Registar, validar e testar

1. Move a pasta de `content/_drafts/<id>/` para `content/modules/<id>/` e acrescenta `modules/<id>/module.yaml` ao `content/manifest.yaml`, **antes** de `modules/projeto/module.yaml` (o projeto final fica sempre em último).
2. `npm run check` até dizer `OK`.
3. `npm run dev` e abre o módulo no browser.
4. `npm test` (faz o build e abre todas as páginas, desktop e mobile).

O módulo aparece sozinho nos menus, com número e cor atribuídos automaticamente. Os módulos são numerados pela ordem do manifesto.

## 6. Rever antes de entregar

Passa pela lista em `docs/STYLE-GUIDE.md` (secção "Checklist de qualidade").
No resumo ao utilizador diz: capítulos e lições criados, quantas perguntas, links usados e **o que não verificaste** (por exemplo, código não compilado).

## 7. Publicar

O utilizador faz `git add`, commit e `git push` para `main`; o GitHub Actions faz o build e publica. Depois de publicar, `npm run check -- --update-ids` regista os ids novos.

## Corrigir ou estender um módulo existente

Todos os módulos têm a mesma estrutura de ficheiros (ver `docs/ARCHITECTURE.md`):

- Texto de uma lição: edita o ficheiro da lição (`<id>.yaml`). Código: edita o ficheiro em `code/`.
- Nova lição: `npm run new:lesson` (cria o ficheiro e acrescenta a referência ao capítulo), com um `id` novo.
- **Nunca mudes o `id` de uma lição publicada**: o progresso do aluno é guardado por id.
- Projeto final: `content/modules/projeto/` (fases, user stories, código do BankingApp). Mexe aí só se o pedido for sobre o projeto.

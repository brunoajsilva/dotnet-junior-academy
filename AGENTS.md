# .NET Backend Academy: guia para agentes de IA

Este ficheiro é o ponto de entrada para qualquer IA (ou pessoa) que vá evoluir a academia.
Se leres só uma coisa, lê este ficheiro: tem o suficiente para acrescentar um módulo sem conhecer o design.

## O que é

Um site de ensino de .NET para programadores de backend de uma consultora de software para a banca.
É um único ficheiro HTML (`index.html`), gerado por Python a partir de dados. Não há framework.
Idioma: **PT-PT**. Termos técnicos mantêm-se em inglês (Dependency Injection, middleware, controller, claim...).
Código e comentários de código: **inglês**. Domínio dos exemplos: um banco (clientes, contas, saldos, NIF).

## Regra de ouro

**Nunca edites `index.html` à mão.** É um ficheiro gerado e é reescrito em cada build.
Conteúdo novo escreve-se em JSON em `content/modules/`. O design aplica-se sozinho.

## Como acrescentar um módulo (resumo)

1. Lê `docs/AUTHORING.md` (o passo a passo) e `docs/STYLE-GUIDE.md` (tom e regras de escrita).
2. Cria `content/modules/<id>.json` seguindo `docs/CONTENT-SCHEMA.md`. Parte de `content/modules/_exemplo-logging.json`.
3. Valida: `python3 src/validate.py content/modules/<id>.json`
4. Gera: `python3 src/build.py --out index.html`
5. Testa: `node src/tests/smoke.js index.html`
6. Resume ao utilizador o que criaste (capítulos, lições, perguntas) e o que não conseguiste verificar.

Há um prompt pronto a usar em `prompts/novo-modulo.md`.

## O que podes e não podes fazer

| Podes | Não podes (sem o utilizador pedir) |
|---|---|
| Criar e editar ficheiros em `content/modules/` | Editar `index.html` |
| Corrigir texto de módulos existentes (em `src/`) | Alterar `src/tpl.html` (layout, CSS, JS) |
| Acrescentar lições, perguntas e links | Mexer no módulo "Projeto final" (`src/m4_*.py`, `src/mod4_bank.py`) |
| Propor um novo tipo de lição (descreve-o, não o implementes) | Criar CSS, HTML ou cores novas |

## Regras inegociáveis

- Texto simples: sem Markdown, sem HTML, sem emojis. Parágrafos separam-se com uma linha em branco (`\n\n`).
- Nunca copiar credenciais, chaves ou dados reais de clientes. Exemplos usam dados inventados (ana@example.com).
- Sem logótipos, nomes de empresas ou marcas como identidade. Pedidos HTTP: usa o **Bruno**, nunca o Postman.
- Dinheiro é `decimal`, nunca `double`. Datas em UTC.
- Não inventes APIs: se não tens a certeza de que um método existe na versão alvo (.NET 10, C# 14), escolhe outro exemplo ou assinala a dúvida no resumo final.
- Uma lição ensina **uma** ideia. Exemplos de código com no máximo 24 linhas.
- Cada capítulo termina com um quiz de 3 a 6 perguntas, com explicação do porquê.

## Mapa do repositório

```
index.html            site gerado (GitHub Pages serve este ficheiro)
AGENTS.md             este guia
docs/                 AUTHORING, CONTENT-SCHEMA, STYLE-GUIDE, DESIGN-RULES, BUILD
prompts/              prompts prontos a copiar
content/modules/      módulos novos, um JSON por módulo
design/               tokens de design (cor, tipografia, forma, movimento)
src/                  gerador: build.py, validate.py, tpl.html, módulos existentes, testes
```

## Se algo falhar

- `validate.py` dá a lista de erros, com o capítulo e a lição. Corrige e volta a correr.
- Se o `build.py` imprimir `INVALID MODULE`, é o mesmo validador a parar o build.
- Se o `smoke.js` indicar `no h1` ou `horizontal overflow`, o conteúdo tem uma linha sem quebras
  (por exemplo, uma URL ou um comando muito longo fora de um bloco de código). Parte-o ou move-o para `code`.

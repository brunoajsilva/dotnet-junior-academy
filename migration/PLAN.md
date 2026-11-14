# Plano de migração da academia para Starlight

Este documento é o guião de execução. Foi escrito para ser seguido por um agente de IA (Claude Sonnet) numa sessão de Claude Code aberta na raiz deste repositório, uma fase por sessão. Uma pessoa consegue segui-lo da mesma forma.

O estudo que justifica a migração está no documento «Academia .NET: estudo de simplificação para o repositório interno». Aqui só está o como.

## 1. Objetivo

Trocar o motor próprio do site (Astro com YAML, renderizadores e cliente feitos à medida) por Starlight com conteúdo em Markdown, e transformar o código do projeto final numa solução .NET que compila. No fim, o repositório fica assim:

```text
<raiz>/
├─ README.md  CONTRIBUTING.md  AGENTS.md  CLAUDE.md
├─ .editorconfig  .gitignore  .nvmrc
├─ azure-pipelines.yml            (ou .github/workflows/ci.yml)
├─ site/                          site Starlight
│  ├─ astro.config.mjs  package.json  package-lock.json  .npmrc
│  ├─ public/  src/assets/  src/styles/academy.css
│  └─ src/content/docs/           33 páginas: index, academia/, csharp/, dotnet/, auth/, projeto/
├─ reference/
│  ├─ 01-solucao-base/            BankingApp depois de «Montar a solução»
│  └─ 02-autenticacao-jwt/        BankingApp depois de «Autenticação JWT»
├─ resources/                     ficheiros para os formandos
└─ docs/
   ├─ decisions/0001-starlight.md
   └─ style-guide.md
```

## 2. Parâmetros

O Bruno preenche esta tabela antes da fase 1. **Se um parâmetro de que a fase precisa estiver `A PREENCHER`, o agente para e pergunta.**

| Parâmetro | Valor | Usado na fase |
| --- | --- | --- |
| `HOSTING` | A PREENCHER (`azure-devops` ou `github`) | 4 |
| `PUBLICACAO` | A PREENCHER (por exemplo: Azure Static Web Apps, IIS interno, nginx interno) | 4 |
| `SITE_URL` | A PREENCHER (por exemplo `https://academia.empresa.pt`) | 4 |
| `BASE_PATH` | `/` | 1, 4 |
| `NPM_REGISTRY` | A PREENCHER (URL do registry interno, ou `publico`) | 1 |
| `QUIZ` | `details` (resposta escondida, sem componente) | 2 |
| `DOTNET_SDK` | `10.0.x` | 3 |
| `NOME_REPOSITORIO` | `dotnet-backend-academy` | 5 |

## 3. Regras para o agente (todas as fases)

1. **Uma fase por sessão.** Começa por ler este ficheiro inteiro e o prompt da fase em `migration/prompts/`. Não começas a fase seguinte sem o Bruno aprovar a anterior.
2. **Ramo próprio.** Cada fase trabalha no ramo `migration/fase-<n>`, criado a partir de `main`. Não fazes commit nem push sem o Bruno dizer «faz commit». Quando ele disser, usa `git -c user.name="Bruno Silva" -c user.email="ajsilva.bruno@gmail.com" commit`.
3. **Até à fase 5, o site antigo é a fonte de verdade.** Não alteras `content/`, `src/`, `tools/`, `public/` nem os ficheiros de configuração da raiz, exceto nas correções da fase 0. O conversor lê `content/` com o leitor do site antigo.
4. **Erros sistemáticos corrigem-se no conversor.** Se a mesma falha aparece em várias páginas, corriges `migration/tools/convert.ts` e voltas a correr `convert.ts --force`. Só editas páginas à mão depois de o Bruno declarar a conversão fechada (fim da fase 2). A partir daí, **nunca mais corres `convert.ts --force`**: apagava as edições manuais.
5. **Não inventas conteúdo.** Não acrescentas lições, perguntas, factos, versões ou APIs. Quando um texto do site antigo deixa de fazer sentido, reescreves só o necessário e listas a alteração no relatório.
6. **Código C# só muda para compilar.** Na fase 3, cada alteração a um ficheiro `.cs` é a mínima para o build passar, e fica registada em `migration/out/reference-fixes.md` (ficheiro, antes, depois, porquê).
7. **Língua.** Conteúdo e documentação em português de Portugal; termos técnicos em inglês (middleware, handler, claim...). Código e comentários de código em inglês. Sem emojis, sem travessões longos.
8. **Pára e pergunta** quando: falta um parâmetro; `npm install` ou `dotnet restore` falham por rede ou certificado; um passo pediria para apagar algo que este plano não lista; uma verificação falha e a causa não é óbvia depois de uma tentativa.
9. **Relatório no fim de cada fase**, na conversa, com este formato:
   - O que mudou (ficheiros criados, alterados, apagados).
   - Comandos corridos e resultado de cada um.
   - Critério de aceitação da fase: cumprido ou não, com a evidência.
   - O que ficou por decidir ou por fazer.

## 4. Ferramentas preparadas

| Ficheiro | Para quê |
| --- | --- |
| `migration/templates/site/` | O site Starlight vazio: configuração, logótipo, cor da academia, versões fixas (Astro 7.4.5, Starlight 0.43.1) |
| `migration/tools/convert.ts` | Gera as 33 páginas em `site/src/content/docs/` e as duas soluções em `reference/`, a partir de `content/` |
| `migration/tools/verify.ts` | Compara o antigo com o novo: páginas, lições, perguntas, «Saber mais», user stories, código das lições, links internos |
| `migration/templates/ci/` | Modelos do pipeline: Azure DevOps e GitHub Actions |
| `migration/prompts/` | O prompt a colar no início de cada fase |

O conversor e o verificador foram testados contra o conteúdo de 14 de novembro de 2026: 33 páginas, 120 lições, 60 perguntas, 139 «Saber mais», 20 user stories, 67 exemplos de código, 1.233 links internos, zero falhas. O build do Starlight passou com Node 24.

Requisitos da máquina: Node 22.23.4 ou superior (o Astro 7.4.5 recusa versões abaixo) e, para a fase 3, o .NET SDK 10.

## 5. Fases

### Fase 0. Correções no site atual

Objetivo: o site atual fica correto enquanto a migração decorre.

1. Em `package.json`, `engines.node` passa a `>=22.23.4`. No `README.md` e em `docs/DEVELOPMENT.md`, «Node 20» passa a «Node 22.23.4 ou superior».
2. Cria `.nvmrc` na raiz com `24`.
3. Regista o id do Cronograma: `npx tsx tools/check.ts --update-ids`. Confirma que `content/ids.lock` ganhou a linha `sec:schedule` e mais nenhuma. Atenção: o comando que o README atual indica, `npm run check -- --update-ids`, não funciona, porque o npm passa a opção ao `astro check` e não ao `tools/check.ts`. Corrige-o também no `README.md`, no `AGENTS.md` e em `docs/DEVELOPMENT.md`.
4. Corre `npm test`.

Critério de aceitação: `npm test` passa e o diff só toca em `package.json`, `README.md`, `AGENTS.md`, `docs/DEVELOPMENT.md`, `.nvmrc` e `content/ids.lock`.

### Fase 1. Base do site

Objetivo: `site/` existe, instala a partir do registry certo e compila.

1. Copia o modelo: `cp -R migration/templates/site site`.
2. Registry npm. Se `NPM_REGISTRY` não for `publico`, cria `site/.npmrc` com `registry=<NPM_REGISTRY>`. Não escrevas credenciais no ficheiro: a autenticação vem da máquina ou do pipeline.
3. `cd site && npm install`. Confirma que o `package.json` mantém as versões exatas `astro 7.4.5` e `@astrojs/starlight 0.43.1` e que nasceu `site/package-lock.json`.
4. Acrescenta à `.gitignore` da raiz as linhas `site/node_modules/`, `site/dist/`, `site/.astro/`, `**/bin/`, `**/obj/`.

Critério de aceitação: `npm install` termina sem erros em `site/`. (O build só passa depois da conversão, na fase 2, porque ainda não há páginas.)

### Fase 2. Conversão do conteúdo

Objetivo: as 33 páginas e as duas soluções de referência geradas, verificadas e revistas.

1. Na raiz: `npx tsx migration/tools/convert.ts`. Lê o relatório que imprime (também fica em `migration/out/report.md`).
2. `cd site && npm run build`. Tem de terminar com `Complete!`. Os avisos `Entry docs → 404 was not found` e, sem `SITE` definido, `Sitemap integration requires the site option` são esperados.
3. Na raiz: `npx tsx migration/tools/verify.ts`. Tem de terminar com `Tudo certo.`
4. Trata a lista «A rever à mão» do relatório. Cada linha é um texto que fala de uma funcionalidade que deixa de existir (progresso, painel, árvore clicável, plano pessoal) ou um caso especial:
   - Enquanto a conversão não estiver fechada, se o problema estiver no conteúdo antigo (por exemplo, «Escolhe um ficheiro»), anota-o no relatório e não o corriges ainda.
   - `academia/como-funciona.md`: o cartão «Progresso» e as referências ao «painel» deixam de ser verdade. Proposta para o Bruno aprovar: «Saber mais» passa a «abre por baixo do texto»; o cartão «Progresso» sai.
5. Abre `npm run dev` em `site/` e percorre estas páginas com o Bruno: `academia/cronograma`, `academia/software-necessario`, `csharp/fundamentos-da-linguagem`, `dotnet/organizacao-do-codigo`, `projeto/montar-a-solucao`, `projeto/enunciado-user-stories`, `projeto/entrega-final`.
6. Quando o Bruno aprovar, a conversão fica fechada: aplica à mão as reescritas do passo 4 e volta a correr o build e o `verify.ts`.

Critério de aceitação: build com `Complete!`, `verify.ts` com `Tudo certo.`, lista «A rever à mão» resolvida e aprovada pelo Bruno.

Notas:
- Os URLs mudam. A correspondência entre o antigo e o novo está em `migration/out/routes.json`.
- As páginas do projeto final (`.mdx`) mostram o código importando-o de `reference/`. Uma correção em `reference/` aparece no site sem tocar na página.
- O código das lições ficou dentro das páginas, em blocos de código. Os ficheiros `code/` antigos deixam de ser usados.

### Fase 3. Solução de referência compilável

Objetivo: `reference/01-solucao-base` e `reference/02-autenticacao-jwt` compilam e os testes passam.

Repete para cada pasta em `reference/` (`<pasta>` abaixo). Os nomes e referências vêm de `content/modules/projeto/phases/p1/code/project-references.txt`; os pacotes de `instalar-dependencias.sh` das fases p1 e p2.

1. Gera os projetos-modelo numa pasta temporária, fora do repositório, para não apagar código existente:
   ```bash
   T=$(mktemp -d)
   dotnet new classlib -n BankingApp.Domain -o $T/BankingApp.Domain -f net10.0
   dotnet new classlib -n BankingApp.Application -o $T/BankingApp.Application -f net10.0
   dotnet new classlib -n BankingApp.Infrastructure -o $T/BankingApp.Infrastructure -f net10.0
   dotnet new webapi --use-controllers -n BankingApp.Api -o $T/BankingApp.Api -f net10.0
   dotnet new xunit -n BankingApp.Tests -o $T/BankingApp.Tests -f net10.0
   ```
2. Copia só os `.csproj` para `<pasta>/src/<Projeto>/` e `<pasta>/tests/BankingApp.Tests/`. Se `<pasta>/src/BankingApp.Api/Properties/launchSettings.json` não existir, copia também o do modelo. Não copias `Class1.cs`, `WeatherForecast.cs`, `UnitTest1.cs`, `Program.cs` nem `appsettings.json`.
3. Na `<pasta>`: `dotnet new sln -n BankingApp --format sln` e `dotnet sln add` dos cinco projetos. Se a tua versão do SDK não aceitar `--format`, usa `dotnet new sln -n BankingApp` e aceita o `.slnx`; diz no relatório qual ficou.
4. Referências entre projetos, exatamente como em `project-references.txt`:
   - Application → Domain
   - Infrastructure → Application
   - Api → Application, Infrastructure
   - Tests → Domain, Application
5. Pacotes NuGet: os de `p1/code/instalar-dependencias.sh` nas duas pastas; os de `p2/code/instalar-dependencias.sh` só em `02-autenticacao-jwt`. Usa sempre o caminho `src/<Projeto>` ou `tests/BankingApp.Tests` como nos scripts. Regista as versões que ficaram instaladas.
6. `dotnet build` e `dotnet test` na `<pasta>`.
7. Se falhar: corrige o mínimo, regista em `migration/out/reference-fixes.md` e repete. Se a correção mudar o comportamento que uma página explica, pára e pergunta ao Bruno.
8. Não geras migrations do EF Core: não são precisas para compilar e dependem da base de dados.

Critério de aceitação: `dotnet build` e `dotnet test` verdes nas duas pastas; `reference-fixes.md` revisto pelo Bruno; `npm run build` do site continua a passar (as páginas importam estes ficheiros).

### Fase 4. Pipeline e publicação

Objetivo: cada push para `main` compila o site e as soluções e publica o site no destino interno.

1. Se `HOSTING` = `azure-devops`: copia `migration/templates/ci/azure-pipelines.yml` para a raiz. Se `github`: copia `migration/templates/ci/github-ci.yml` para `.github/workflows/ci.yml`.
2. Preenche `BASE` e `SITE` com `BASE_PATH` e `SITE_URL`.
3. Configura o passo de publicação segundo `PUBLICACAO`. O modelo traz um exemplo para Azure Static Web Apps em comentário; **confirma o nome da tarefa e os campos com a documentação atual e com a equipa de infraestrutura antes de o usar**. Segredos (tokens) vão para variáveis secretas do pipeline, nunca para o ficheiro.
4. Se o registry for Azure Artifacts, ativa o passo `npmAuthenticate@0` que está em comentário.
5. O Bruno corre o pipeline. O site tem de abrir em `SITE_URL`, com pesquisa a funcionar.

Critério de aceitação: pipeline verde em `main` e o site acessível dentro da rede.

### Fase 5. Corte e limpeza

Objetivo: só fica o que a estrutura do ponto 1 descreve.

1. Escreve a documentação nova:
   - `README.md`: o que é, requisitos (Node 22.23.4+, .NET SDK 10), correr o site (`cd site && npm install && npm run dev`), compilar a referência, publicar.
   - `CONTRIBUTING.md`: corrigir uma lição, acrescentar uma lição, acrescentar uma página, mudar a ordem (`sidebar.order`), acrescentar um módulo (pasta nova + entrada em `sidebar` no `astro.config.mjs`), avisos (`:::tip`), «Saber mais» (`<details>`), quiz, código no projeto final (em `reference/`, importado na página). Com um exemplo de cada.
   - `AGENTS.md`: curto. As regras de escrita do `AGENTS.md` atual que continuam válidas (texto simples, PT-PT, termos técnicos em inglês, dinheiro em `decimal`, sem dados reais, Bruno e nunca Postman, uma ideia por lição, exemplos curtos) e um apontador para o `CONTRIBUTING.md`. Sai tudo o que fala de YAML, schemas, `ids.lock` e `npm run check`.
   - `docs/style-guide.md`: a partir de `docs/STYLE-GUIDE.md`, sem as partes sobre YAML.
   - `docs/decisions/0001-starlight.md`: contexto, decisão, consequências (o que se perdeu: progresso, quiz com pontuação, plano pessoal).
   - `CLAUDE.md`: mantém-se, a apontar para o `AGENTS.md`.
2. Move para `resources/` o que é material para formandos e não está noutro sítio (por exemplo, o prompt do front-end, se existir no repositório).
3. Apaga o site antigo: `src/`, `tools/`, `content/`, `design/`, `public/` (da raiz), `prompts/`, `astro.config.mjs`, `site.config.mjs`, `tsconfig.json`, `package.json`, `package-lock.json`, `.prettierrc.json`, `.prettierignore`, `.astro/`, `node_modules/` (da raiz), `docs/ARCHITECTURE.md`, `docs/AUTHORING.md`, `docs/CONTENT-SCHEMA.md`, `docs/DESIGN-RULES.md`, `docs/DEVELOPMENT.md`, `docs/STYLE-GUIDE.md` e os workflows antigos em `.github/workflows/` (exceto o novo, se `HOSTING` = `github`).
4. Apaga `migration/` por último, depois de guardar `migration/out/routes.json` e `migration/out/reference-fixes.md` em `docs/decisions/` como anexos da decisão 0001.
5. Verificações finais: `cd site && npm ci && npm run build`; `dotnet build` e `dotnet test` em cada pasta de `reference/`; `git status` só com o que este plano lista.
6. O Bruno desliga o GitHub Pages antigo e renomeia o repositório para `NOME_REPOSITORIO`.

Critério de aceitação: alguém que não conhece o projeto acrescenta uma lição seguindo só o `CONTRIBUTING.md`, e o pipeline publica-a.

## 6. Riscos conhecidos

| Risco | O que fazer |
| --- | --- |
| `npm install` falha com `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` na rede da empresa | Usar o registry interno (`site/.npmrc`) ou `npm config set cafile <certificado da empresa>`. Nunca `strict-ssl false` |
| Node abaixo de 22.23.4 | O Astro 7.4.5 recusa-se a correr. Instalar Node 24 |
| O código do BankingApp nunca foi compilado | Esperar erros na fase 3; corrigir o mínimo e registar |
| Edições manuais perdidas | Nunca correr `convert.ts --force` depois de a conversão estar fechada |
| O texto dos resultados da pesquisa aparece em inglês («results for») | Conhecido e aceite; não bloqueia |
| A versão nova do Starlight muda a sintaxe do `sidebar` | As versões estão fixas no `package.json`. Atualizar só de propósito, num ramo próprio |

# Soluções de referência

Duas soluções .NET que o site importa para mostrar o código do projeto final.

| Pasta | Corresponde a |
| --- | --- |
| `01-solucao-base/` | A página «Montar a solução» (BankingApp sem autenticação) |
| `02-autenticacao-jwt/` | A página «Autenticação JWT» (BankingApp com registo, login e dashboard) |

Cada pasta tem `BankingApp.sln`, `src/` (Domain, Application, Infrastructure, Api) e `tests/BankingApp.Tests`.

## Compilar e testar

Requer o .NET SDK 10.

```bash
dotnet build reference/01-solucao-base --configuration Release
dotnet test reference/01-solucao-base --configuration Release --no-build
dotnet build reference/02-autenticacao-jwt --configuration Release
dotnet test reference/02-autenticacao-jwt --configuration Release --no-build
```

O pipeline faz o mesmo em cada push.

## Regras

- O site mostra estes ficheiros tal como estão. Corrigir aqui corrige a página, sem tocar nela.
- Os pacotes NuGet estão com versões flutuantes (por exemplo `10.0.*`). Depois do primeiro build verde, fixa as versões que ficaram instaladas.
- Não há migrations do EF Core: dependem da base de dados do formando.

## Estado

Os ficheiros `.csproj` e `.sln` foram escritos sem acesso ao .NET SDK, por isso o primeiro build pode pedir correções mínimas. Apaga esta secção quando `dotnet build` e `dotnet test` passarem nas duas pastas.

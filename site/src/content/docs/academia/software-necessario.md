---
title: "Software necessário"
sidebar:
  order: 6
---

Instala e verifica estes componentes no primeiro dia, antes de começares o módulo de C#. Confirma cada um com o comando de verificação, que tem de dar o resultado esperado.

## .NET SDK 10

**Necessário.** Compilador, comando dotnet e templates de projeto.

Para verificar:

```bash
dotnet --version
```

Resultado esperado: 10.0.x

Instalação: Instalador do SDK em dotnet.microsoft.com/download (escolhe o .NET 10, versão LTS).

<details>
<summary>Saber mais</summary>

O SDK inclui o runtime, por isso não precisas de instalar mais nada para executar as aplicações. Se tiveres várias versões, dotnet --list-sdks mostra todas.

</details>

## IDE: Visual Studio ou VS Code

**Necessário.** Editor com depuração, IntelliSense e gestão de pacotes.

Resultado esperado: Abre uma consola .NET e corre-a com F5.

Instalação: Visual Studio 2026 com a carga de trabalho «ASP.NET and web development», ou VS Code com a extensão C# Dev Kit.

<details>
<summary>Saber mais</summary>

Escolhe um dos dois. Os exercícios são feitos com a linha de comandos (dotnet new, dotnet build, dotnet run), por isso funcionam com qualquer um. O Visual Studio é o mais completo no Windows; o VS Code funciona em qualquer sistema.

</details>

## Git

**Necessário.** Controlo de versões. Todo o código do curso vive num repositório.

Para verificar:

```bash
git --version
```

Resultado esperado: git version 2.x

Instalação: git-scm.com/downloads.

<details>
<summary>Saber mais</summary>

Depois de instalar, configura o teu nome e e-mail:

git config --global user.name "O Teu Nome"
git config --global user.email "nome@empresa.pt"

</details>

## SQL Server

**Necessário.** Base de dados dos módulos de Entity Framework Core e do projeto final.

Para verificar:

```bash
sqlcmd -S localhost -Q "SELECT @@VERSION"
```

Resultado esperado: Microsoft SQL Server 20xx ...

Instalação: SQL Server Developer ou LocalDB (instalado com o Visual Studio).

<details>
<summary>Saber mais</summary>

Para os exercícios, o LocalDB chega e não precisa de configuração. A connection string típica é Server=(localdb)\\MSSQLLocalDB;Database=BankingApp;Trusted\_Connection=True;TrustServerCertificate=True.

</details>

## Cliente SQL

**Necessário.** Ver as tabelas e os dados que o EF Core cria.

Resultado esperado: Consegues ligar-te ao servidor e listar as bases de dados.

Instalação: SQL Server Management Studio, Azure Data Studio ou a extensão SQL do VS Code.

<details>
<summary>Saber mais</summary>

Vais usá-lo para confirmar que a migration criou as tabelas e que o POST gravou uma linha.

</details>

## Ferramenta dotnet-ef

**Necessário.** Comandos para criar e aplicar migrations.

Para verificar:

```bash
dotnet ef --version
```

Resultado esperado: Entity Framework Core .NET Command-line Tools 10.x

Instalação: dotnet tool install --global dotnet-ef

<details>
<summary>Saber mais</summary>

É uma ferramenta global do .NET, instalada uma única vez por computador. Para atualizar: dotnet tool update --global dotnet-ef.

</details>

## Bruno

**Necessário.** Enviar pedidos HTTP à tua API e guardá-los numa coleção, em ficheiros de texto que podes pôr no repositório.

Resultado esperado: Consegues enviar um GET a qualquer URL público.

Instalação: usebruno.com. Não instales o Postman: usamos só o Bruno.

<details>
<summary>Saber mais</summary>

O Bruno guarda as coleções em ficheiros de texto (.bru), que revês em Pull Requests como qualquer código. Importa o documento OpenAPI da tua API para criares a coleção. Usa-se no módulo de Autenticação e no projeto final.

</details>

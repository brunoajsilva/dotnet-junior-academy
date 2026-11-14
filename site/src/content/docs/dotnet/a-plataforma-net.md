---
title: "A plataforma .NET"
description: "O que acontece entre escrever C# e ver o programa a correr, e como se organiza uma solução."
sidebar:
  order: 1
---

O que acontece entre escrever C# e ver o programa a correr, e como se organiza uma solução.

## Como é que o .NET executa o teu código

1. **Código C#** ficheiros .cs
2. **Compilador** Roslyn
3. **Intermediate Language** ficheiro .dll
4. **Runtime** CLR e compilador JIT
5. **Código máquina** o processador executa

#### Multiplataforma

Windows, Linux e macOS, incluindo containers.

#### Biblioteca de classes

Coleções, ficheiros, rede, JSON e muito mais, já incluídos.

#### Memória gerida

O garbage collector liberta a memória que já não é usada.

<details>
<summary>Saber mais</summary>

O compilador Roslyn transforma o teu C# em IL (Intermediate Language), guardado num ficheiro .dll. O IL não é código máquina e, por isso, é igual em Windows, Linux e macOS. Quando a aplicação arranca, o runtime (CLR) usa o compilador JIT para converter o IL em código máquina do processador onde está a correr.

É isto que permite compilar uma vez e executar em vários sistemas, incluindo containers Linux.

</details>

## SDK, runtime e versões

#### SDK

Para desenvolver: compilador, linha de comandos dotnet e templates de projetos.

#### Runtime

Para executar: é o que tem de existir no servidor onde a aplicação corre.

#### Versões LTS

As versões pares, como o .NET 10, têm suporte de longa duração (3 anos).

#### .NET Framework

A plataforma antiga (4.x): só Windows e sem novas funcionalidades. Em projetos novos usa-se o .NET.

Experimenta no terminal:

```bash
dotnet --list-sdks
```

<details>
<summary>Saber mais</summary>

O SDK é o que instalas no teu computador para desenvolver: compilador, comando dotnet e templates. O runtime é o mínimo necessário para executar uma aplicação já compilada, e é o que o servidor precisa.

As versões pares (8, 10) são LTS. Em projetos novos escolhe sempre uma LTS ou superior, e nunca o .NET Framework 4.x.

:::tip[Experimenta]
No terminal, corre dotnet --list-sdks e dotnet --list-runtimes e vê o que tens instalado.
:::

</details>

## Soluções e Projetos

| Tarefa | Linha de comandos | Visual Studio |
| --- | --- | --- |
| Criar um projeto | dotnet new webapi | File \> New \> Project |
| Adicionar à solução | dotnet sln add | Botão direito na Solution \> Add \> New Project |
| Referenciar um projeto | dotnet add reference | Botão direito em Dependencies \> Add Project Reference |
| Instalar um pacote | dotnet add package | Botão direito no projeto \> Manage NuGet Packages |
| Compilar | dotnet build | Build \> Build Solution (Ctrl+Shift+B) |
| Executar | dotnet run | F5 (com debugger) ou Ctrl+F5 (sem) |
| Testar | dotnet test | Test \> Run All Tests (Test Explorer) |

<details>
<summary>Saber mais</summary>

A linha de comandos e o Visual Studio fazem o mesmo. A linha de comandos é mais rápida de repetir, fica em scripts e funciona em qualquer IDE. Sabê-la é o que te permite ajudar num pipeline de Release, onde não há IDE.

</details>

## Solução, projeto e NuGet

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Serilog" Version="4.2.0" />
    <ProjectReference Include="..\Domain\Domain.csproj" />
  </ItemGroup>
</Project>
```

- .sln agrupa projetos; .csproj descreve um projeto.
- TargetFramework indica a versão do .NET.
- PackageReference traz pacotes do NuGet.
- ProjectReference liga projetos entre si.

<details>
<summary>Saber mais</summary>

A solução (.sln) é só uma lista de projetos para o IDE abrir em conjunto. Cada projeto (.csproj) é um XML pequeno que diz o que é (Sdk), para que versão compila (TargetFramework), de que pacotes depende (PackageReference) e de que outros projetos depende (ProjectReference).

As referências entre projetos formam a arquitetura: se o Domain não referencia nada, é impossível usar o EF Core lá dentro por engano.

:::caution[Armadilha]
Referências circulares entre projetos. O compilador recusa: é sinal de que as responsabilidades estão mal divididas.
:::

</details>

## A solução do banco

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Criar a solução.** BankingApp, com o projeto Api (webapi)
2. **Adicionar à solução.** Domain (classlib) e Tests (xunit)
3. **Referenciar.** o Domain na Api e a Api nos Tests
4. Instalar um pacote na Api via NuGet: Newtonsoft.Json
5. **Compilar e correr.** a Api e abrir o endereço indicado no terminal

<details>
<summary>Ver resultado esperado</summary>

```text
dotnet build
Build succeeded.
    0 Warning(s)
    0 Error(s)

dotnet run
Now listening on:
http://localhost:5xxx
```

</details>

:::note[Extra]
Mostrar a estrutura de pastas com o comando tree e explicar o que cada projeto vai ter.
:::

<details>
<summary>Saber mais</summary>

Faz tudo na linha de comandos, sem o assistente do IDE: assim ficas a saber exatamente o que cada comando cria. Tabela de equivalências com o Visual Studio está no tema «Soluções e Projetos».

:::tip[Experimenta]
Corre tree (ou tree /f) para ver a estrutura de pastas e explica o que cada projeto vai ter.
:::

</details>

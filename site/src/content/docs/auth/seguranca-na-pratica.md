---
title: "Segurança na prática"
description: "O que separa um exemplo que funciona de uma API que se pode pôr em produção: passwords, segredos, HTTPS e os erros comuns."
sidebar:
  order: 7
---

O que separa um exemplo que funciona de uma API que se pode pôr em produção: passwords, segredos, HTTPS e os erros comuns.

## Passwords: hash, nunca encriptação

```csharp
using Microsoft.AspNetCore.Identity;

var hasher = new PasswordHasher<object>();

// at registration: store ONLY the hash
string hash = hasher.HashPassword(null!, "Passw0rd!");
// "AQAAAAIAAYagAAAAE..."  (random salt included, different every time)

// at login: compare the typed password with the stored hash
var result = hasher.VerifyHashedPassword(null!, hash, "Passw0rd!");
bool ok = result != PasswordVerificationResult.Failed;
```

- Guarda-se o hash, nunca a password.
- O hash tem sal aleatório: o mesmo texto dá hashes diferentes.
- Verifica-se com VerifyHashedPassword.
- O hash é lento de propósito.

<details>
<summary>Saber mais</summary>

Encriptar é reversível: quem tiver a chave recupera a password. O hash não tem volta; o login compara o hash da password escrita com o hash guardado. O sal evita que duas pessoas com a mesma password tenham o mesmo hash e inutiliza as tabelas de hashes pré-calculados.

O PasswordHasher de ASP.NET Core Identity já faz isto bem (PBKDF2 com sal e muitas iterações). Não inventes o teu algoritmo.

:::caution[Armadilha]
Guardar um hash simples (SHA256 ou MD5) de uma password. São rápidos, e um atacante testa milhares de milhões de palpites por segundo.
:::

</details>

## Checklist de uma API protegida

#### Transporte

- HTTPS sempre, com redirecionamento
- O token só no cabeçalho Authorization, nunca no URL

#### Segredos

- Chave do JWT em variáveis de ambiente ou num cofre
- Nenhum segredo em ficheiros do Git

#### Tokens

- Access token curto (minutos)
- Validar emissor, audiência, validade e assinatura
- Poucas claims, nenhum segredo

#### Passwords

- Só o hash, com PasswordHasher
- Mínimo de 8 caracteres
- Mesma resposta para email desconhecido e password errada

#### Autorização

- Todos os endpoints protegidos por omissão
- Id do utilizador sempre do token
- 404 para recursos de outros utilizadores

#### Operação

- Não registar passwords nem tokens
- Limitar tentativas de login
- Mensagens de erro sem detalhes internos

<details>
<summary>Saber mais</summary>

Uma boa prática é inverter a lógica: protege tudo e abre só o que é público. No ASP.NET Core faz-se com uma FallbackPolicy que exige utilizador autenticado, e \[AllowAnonymous\] nos endpoints públicos. Assim, um endpoint novo esquecido fica protegido e não aberto.

</details>

## Onde guardar o token no cliente

| Local | Risco | Nota |
| --- | --- | --- |
| localStorage | Qualquer script na página lê o token (XSS) | Simples, mas exposto. |
| Cookie HttpOnly + Secure + SameSite | Scripts não conseguem lê-lo | Exige proteção contra CSRF. |
| Memória da aplicação | Perde-se ao recarregar | Mais seguro, com refresh token para recuperar. |
| Cofre do sistema (apps móveis) | Protegido pelo sistema operativo | Keychain no iOS, Keystore no Android. |

<details>
<summary>Saber mais</summary>

Não há uma resposta única. Cada opção troca um risco por outro. O importante é saberes qual escolheste e porquê. Este tema pertence ao cliente (web ou móvel), mas quem desenha a API precisa de o conhecer, porque define como o token é enviado.

</details>

## Rever o AuthLab com olhos de atacante

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Hash.** substituir as passwords em texto por hashes com PasswordHasher
2. **Por omissão.** exigir autenticação em todos os endpoints com uma FallbackPolicy e abrir o Login e os endpoints públicos com AllowAnonymous
3. **Limite.** bloquear o login durante 1 minuto após 5 tentativas falhadas do mesmo email
4. **Logs.** confirmar que nenhum log escreve a password nem o token
5. **Explicar.** escrever três frases sobre o que acontece se alguém roubar o access token e o que limita o estrago

<details>
<summary>Ver resultado esperado</summary>

```text
Tentativa 6 do mesmo email -> 429 Too Many Requests (ou 401 com mensagem genérica)
Endpoint novo sem atributo -> 401
```

</details>

:::note[Extra]
Acrescenta um endpoint /refresh com rotation, como no capítulo anterior.
:::

<details>
<summary>Saber mais</summary>

Rever com olhos de atacante é perguntar: se eu fosse mal-intencionado, o que tentava? Trocar o id na URL, repetir uma password mil vezes, reutilizar um token expirado, ler o payload à procura de segredos. A checklist do início do capítulo responde às mesmas perguntas.

</details>

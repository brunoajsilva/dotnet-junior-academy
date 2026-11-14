---
title: "Basic Authentication"
description: "O mecanismo mais simples: enviar o utilizador e a password em cada pedido. Percebe porque deixou de ser suficiente."
sidebar:
  order: 2
---

O mecanismo mais simples: enviar o utilizador e a password em cada pedido. Percebe porque deixou de ser suficiente.

## Como funciona

1. **Pedido** O cliente chama um endpoint protegido sem credenciais.
2. **Desafio** A API responde 401 com o cabeçalho WWW-Authenticate: Basic.
3. **Credenciais** O cliente repete o pedido com Authorization: Basic base64(user:password).

:::note[Nota]
O servidor valida o utilizador e a password em todos os pedidos.

Não há sessão nem token: as credenciais viajam sempre.
:::

<details>
<summary>Saber mais</summary>

O Basic Auth faz parte do próprio protocolo HTTP (RFC 7617). É suportado por qualquer cliente HTTP sem código adicional, o que o torna útil em ferramentas internas e em testes rápidos.

</details>

## O cabeçalho por dentro

```bash
# the client joins "user:password" and encodes it in base64
echo -n 'ana@example.com:Passw0rd!' | base64
# YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==

# the header sent on EVERY request
Authorization: Basic YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==

# base64 is an encoding, not encryption: anyone can reverse it
echo 'YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==' | base64 -d
# ana@example.com:Passw0rd!

# curl does the same with -u
curl -u 'ana@example.com:Passw0rd!' https://localhost:5001/api/dashboard
```

- O valor é «user:password» em base64.
- Base64 é uma codificação, não encriptação.
- Qualquer pessoa que veja o pedido recupera a password.
- O cabeçalho vai em todos os pedidos.

<details>
<summary>Saber mais</summary>

Por isso o Basic só é aceitável sobre HTTPS. Mesmo assim, a password sai do cliente em cada pedido e passa por proxies, logs e ferramentas de depuração que registam cabeçalhos.

:::tip[Experimenta]
Corre o primeiro comando com uma password tua e depois o segundo comando para a recuperar. Dá para sentir o problema.
:::

</details>

## Os limites do Basic Auth

| Problema | Consequência |
| --- | --- |
| A password viaja em todos os pedidos | Mais oportunidades de ser intercetada ou registada em logs. |
| A API vê a password do utilizador | Uma aplicação de terceiros teria de receber a tua password do banco. |
| Não expira | Só deixa de funcionar se mudares a password. |
| Sem âmbito (scope) | Quem tem as credenciais pode fazer tudo. |
| Sem revogação parcial | Para cortar o acesso a uma aplicação tens de mudar a password, e todas as outras aplicações perdem acesso. |
| Sem autenticação multifator | Não há onde encaixar um segundo fator. |

<details>
<summary>Saber mais</summary>

Estes limites são a razão de ser do OAuth 2.0: dar a uma aplicação um acesso limitado, temporário e revogável, sem lhe entregar a password.

</details>

## Descodificar um cabeçalho Basic

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Codificar.** gerar o base64 de «rui@example.com:Passw0rd!» com o comando echo -n ... \| base64
2. **Descodificar.** recuperar o texto original com base64 -d
3. **Pedido.** com curl -u, chamar https://httpbin.org/basic-auth/rui/pass e ver a resposta 401 ou 200
4. **Concluir.** escrever numa frase porque é que o Basic Auth não serve para uma aplicação móvel de um banco

:::tip[Dica]
Se estiveres no Windows, usa o Git Bash ou o PowerShell: \[Convert\]::ToBase64String(\[Text.Encoding\]::UTF8.GetBytes("rui@example.com:Passw0rd!")).
:::

<details>
<summary>Ver resultado esperado</summary>

```text
rui@example.com:Passw0rd!

(a descodificação devolve exatamente o texto original)
```

</details>

<details>
<summary>Saber mais</summary>

O objetivo é sentires que o base64 não protege nada. Se conseguires descodificar em dois segundos, qualquer pessoa também consegue.

</details>

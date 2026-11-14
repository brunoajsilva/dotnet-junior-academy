---
title: "Autenticação e Autorização"
description: "A diferença entre Basic Auth e OAuth 2.0, como funciona um JWT e um hands-on onde emites, validas e proteges com tokens."
sidebar:
  order: 0
  label: "Visão geral"
---

A diferença entre Basic Auth e OAuth 2.0, como funciona um JWT e um hands-on onde emites, validas e proteges com tokens.

## Capítulos

- [Autenticação e autorização](autenticacao-e-autorizacao/): Duas perguntas diferentes que se confundem: quem és? E o que podes fazer?
- [Basic Authentication](basic-authentication/): O mecanismo mais simples: enviar o utilizador e a password em cada pedido. Percebe porque deixou de ser suficiente.
- [OAuth 2.0 e OpenID Connect](oauth-2-0-e-openid-connect/): Delegar acesso sem partilhar a password: os papéis, os fluxos e os tipos de token.
- [JWT por dentro](jwt-por-dentro/): O formato do token que a BankingApp emite: três partes, claims e uma assinatura.
- [Hands-on I: gerar e validar um JWT](hands-on-i-gerar-e-validar-um-jwt/): Constróis de raiz uma Web API pequena, o AuthLab: configuras a autenticação JWT, crias no controller um método que gera o token e outro que só responde a quem o enviar. Não é a BankingApp: serve para perceberes cada peça antes do projeto.
- [Hands-on II: autorização](hands-on-ii-autorizacao/): Com o token a funcionar, decide-se o que cada utilizador pode fazer: papéis, políticas e dados que só pertencem ao dono. Continuas no AuthLab.
- [Segurança na prática](seguranca-na-pratica/): O que separa um exemplo que funciona de uma API que se pode pôr em produção: passwords, segredos, HTTPS e os erros comuns.

## O que vais aprender

- Distinguir autenticação de autorização e escolher entre 401, 403 e 404
- Explicar as diferenças entre Basic Auth e OAuth 2.0
- Identificar os papéis e os fluxos do OAuth 2.0
- Ler um JWT e perceber o que a API valida
- Emitir e validar um JWT em ASP.NET Core
- Proteger endpoints com papéis, policies e verificação de propriedade

## Ideias para praticar

- Acrescentar um endpoint /refresh ao AuthLab
- Criar uma policy com um requisito próprio
- Mudar a assinatura de HS256 para RS256
- Ler o OWASP API Security Top 10

## Documentação

- [Autenticação e autorização no ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/)
- [Autenticação JWT Bearer](https://learn.microsoft.com/aspnet/core/security/authentication/)
- [OAuth 2.0 e OpenID Connect](https://oauth.net/2/)
- [Bruno](https://www.usebruno.com/)

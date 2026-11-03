# User stories das funcionalidades F1-F20 (PT-PT; termos técnicos em inglês)
US = {}
def S(id, persona, quero, para, desc, sc, fora, sp):
    US[id] = dict(persona=persona, quero=quero, para=para, desc=desc, sc=sc, fora=fora, sp=sp)

C = "cliente autenticado"

S("F1", C, "abrir uma conta adicional", "separar o meu dinheiro por objetivos",
  "O cliente pode ter várias contas no mesmo banco, por exemplo uma para despesas correntes e outra para poupança. O número da conta é gerado pelo sistema e o titular é sempre o cliente do token.",
  [("Abrir conta com depósito inicial", ["tenho 2 contas ativas"], ["peço uma nova conta com depósito inicial de 100,00"], ["recebo success com o número da nova conta", "a conta fica com saldo 100,00 e estado Active"]),
   ("Depósito inicial negativo", ["tenho sessão iniciada"], ["peço uma conta com depósito inicial de -1"], ["recebo validation com o erro no campo do valor", "nenhuma conta é criada"]),
   ("Limite de contas atingido", ["tenho 5 contas ativas"], ["peço uma nova conta"], ["recebo conflict", "continuo com 5 contas"]),
   ("Pedido sem token", ["não enviei o token JWT"], ["peço uma nova conta"], ["recebo unauthorized"])],
  ["Tipos de conta (ordem, poupança, a prazo)", "Contas com mais do que um titular"], 3)

S("F2", C, "ver as minhas contas e o detalhe de cada uma", "saber quanto tenho e onde",
  "Listagem das contas do cliente, com filtro opcional por estado, e consulta do detalhe de uma conta pelo número. Uma conta que não é do cliente é indistinguível de uma conta que não existe.",
  [("Listar as minhas contas", ["tenho 3 contas, uma delas fechada"], ["peço a lista de contas"], ["recebo success com as 3 contas ordenadas por número"]),
   ("Filtrar por estado", ["tenho 3 contas, uma delas fechada"], ["peço a lista com o filtro status Active"], ["recebo apenas as 2 contas ativas"]),
   ("Conta de outro cliente", ["a conta 123 pertence a outro cliente"], ["peço o detalhe da conta 123"], ["recebo not_found, igual a uma conta inexistente"])],
  ["Pesquisa por texto", "Paginação da lista de contas"], 2)

S("F3", C, "fechar uma conta que já não uso", "manter apenas as contas de que preciso",
  "Fechar não apaga a conta: o estado passa a Closed e o histórico mantém-se. Só é possível com saldo zero e nunca deixa o cliente sem contas ativas.",
  [("Fechar conta sem saldo", ["tenho 2 contas ativas e a conta A tem saldo 0"], ["fecho a conta A"], ["recebo success", "a conta A fica Closed", "o dashboard deixa de a mostrar"]),
   ("Conta com saldo", ["a conta A tem saldo 10,00"], ["fecho a conta A"], ["recebo conflict", "a conta continua Active"]),
   ("Última conta ativa", ["tenho apenas uma conta ativa"], ["fecho essa conta"], ["recebo conflict"]),
   ("Conta já fechada", ["a conta A já está Closed"], ["volto a fechar a conta A"], ["recebo conflict"])],
  ["Reabrir contas fechadas", "Transferir o saldo automaticamente antes de fechar"], 3)

S("F4", C, "depositar dinheiro numa das minhas contas", "aumentar o saldo disponível",
  "Cada depósito atualiza o saldo e cria uma Transaction com o saldo depois do movimento. As duas alterações são gravadas na mesma chamada a SaveChanges.",
  [("Depósito válido", ["a conta A tem saldo 100,00"], ["deposito 50,00"], ["recebo success com o novo saldo 150,00", "fica registada uma Transaction do tipo Deposit com saldo depois 150,00"]),
   ("Valor inválido", ["tenho sessão iniciada"], ["deposito 0, -5 ou 10,001"], ["recebo validation em todos os casos", "o saldo não muda"]),
   ("Conta fechada", ["a conta A está Closed"], ["deposito 10,00"], ["recebo conflict"]),
   ("Conta de outro cliente", ["a conta B não é minha"], ["deposito 10,00 na conta B"], ["recebo not_found"])],
  ["Depósito por cheque ou multibanco", "Comissões"], 3)

S("F5", C, "levantar dinheiro de uma das minhas contas", "dispor do meu dinheiro quando preciso",
  "O levantamento reutiliza as regras de valor e de conta ativa do depósito e acrescenta duas: saldo suficiente e limite diário, calculado na base de dados.",
  [("Levantamento válido", ["a conta A tem saldo 200,00"], ["levanto 50,00"], ["recebo success com o novo saldo 150,00", "fica registada uma Transaction do tipo Withdrawal"]),
   ("Saldo insuficiente", ["a conta A tem saldo 20,00"], ["levanto 50,00"], ["recebo conflict com a mensagem «Insufficient funds»", "o saldo não muda"]),
   ("Limite diário no limite exato", ["já levantei 450,00 hoje"], ["levanto 50,00"], ["recebo success"]),
   ("Limite diário excedido", ["já levantei 450,00 hoje"], ["levanto 50,01"], ["recebo conflict"])],
  ["Levantamento em caixa automático", "Limites diferentes por conta (ver F6)"], 5)

S("F7", C, "transferir dinheiro de uma das minhas contas para outra conta do banco", "pagar a outras pessoas e mover dinheiro entre as minhas contas",
  "Uma transferência é uma operação atómica: debita a origem, credita o destino e cria duas Transaction. Se qualquer regra falhar, nenhum saldo muda.",
  [("Transferência válida", ["a conta A tem 200,00 e a conta B tem 0"], ["transfiro 50,00 da A para a B"], ["recebo success", "A fica com 150,00 e B com 50,00", "ficam duas Transaction (saída e entrada)"]),
   ("Origem igual ao destino", ["tenho sessão iniciada"], ["transfiro da conta A para a conta A"], ["recebo validation"]),
   ("Destino inexistente", ["o número de destino não existe"], ["peço a transferência"], ["recebo not_found", "nenhum saldo muda"]),
   ("Falha a meio", ["a origem não tem saldo suficiente"], ["peço a transferência"], ["recebo conflict", "nenhum saldo nem Transaction foram gravados"])],
  ["Transferências para outros bancos", "Transferências agendadas"], 5)

S("F9", C, "consultar os movimentos de uma conta, filtrando por tipo e datas", "perceber para onde foi o meu dinheiro",
  "Consulta só de leitura, ordenada do mais recente para o mais antigo, com filtros opcionais e paginação. O filtro e a paginação são feitos na base de dados.",
  [("Primeira página por omissão", ["a conta A tem 45 movimentos"], ["peço o extrato sem parâmetros"], ["recebo os 20 movimentos mais recentes", "total 45, página 1, tamanho 20"]),
   ("Filtrar por tipo e datas", ["a conta A tem depósitos e levantamentos"], ["filtro por type Deposit, com from e to"], ["recebo apenas depósitos dentro do intervalo"]),
   ("Tamanho de página acima do máximo", ["tenho sessão iniciada"], ["envio pageSize 500"], ["recebo validation"]),
   ("Conta de outro cliente", ["a conta B não é minha"], ["peço o extrato da conta B"], ["recebo not_found"])],
  ["Pesquisa por descrição", "Exportação (ver F11)"], 5)

S("F10", C, "ver no dashboard o que se passou no último mês", "ter uma visão rápida das minhas finanças",
  "O dashboard passa a incluir os últimos 5 movimentos e os totais depositado e levantado no mês corrente. O número de consultas à base de dados é fixo, independentemente do número de contas.",
  [("Dashboard completo", ["tenho 3 contas com movimentos este mês"], ["abro o dashboard"], ["vejo as contas e os saldos", "vejo os 5 movimentos mais recentes de todas as contas", "vejo o total depositado e o total levantado no mês"]),
   ("Transferências nos totais", ["fiz uma transferência este mês"], ["abro o dashboard"], ["a saída conta como levantamento e a entrada como depósito"]),
   ("Compatibilidade", ["o cliente da API usa os campos antigos"], ["abro o dashboard"], ["os campos antigos continuam presentes e inalterados"])],
  ["Gráficos", "Comparação com meses anteriores"], 5)

S("F12", C, "guardar os dados de quem pago com frequência", "pagar mais depressa e sem repetir números de conta",
  "Um beneficiário é uma conta de destino guardada com um nome. Cada cliente só vê e gere os seus beneficiários.",
  [("Adicionar beneficiário", ["a conta de destino existe e está Active"], ["adiciono o beneficiário «Senhorio»"], ["recebo success", "o beneficiário aparece na minha lista"]),
   ("Beneficiário repetido", ["já tenho a conta X como beneficiária"], ["adiciono outra vez a conta X"], ["recebo conflict"]),
   ("Conta própria", ["a conta A é minha"], ["adiciono a conta A como beneficiária"], ["recebo validation"]),
   ("Apagar beneficiário de outro cliente", ["o beneficiário 9 é de outro cliente"], ["peço para o apagar"], ["recebo not_found", "o beneficiário continua a existir"])],
  ["Transferir diretamente a partir do beneficiário", "Editar o nome do beneficiário"], 3)

S("F8", C, "cancelar uma transferência que fiz por engano", "recuperar o dinheiro enviado por erro",
  "O estorno só é possível durante uma janela curta, configurável, e apenas se o destino ainda tiver saldo. Cria dois movimentos de estorno e marca a transferência como Reversed.",
  [("Estorno dentro do prazo", ["fiz uma transferência há 2 minutos", "o destino tem saldo suficiente"], ["peço o estorno"], ["recebo success", "os saldos voltam ao valor anterior", "a transferência fica Reversed"]),
   ("Fora do prazo", ["a transferência tem 6 minutos"], ["peço o estorno"], ["recebo conflict"]),
   ("Transferência de outro cliente", ["a transferência foi feita por outro cliente"], ["peço o estorno"], ["recebo not_found"]),
   ("Segundo estorno", ["a transferência já está Reversed"], ["peço o estorno outra vez"], ["recebo conflict"])],
  ["Estorno parcial", "Aprovação do destinatário"], 5)

S("F14", C, "ver e receber os juros da minha conta", "ser remunerado pelo dinheiro que mantenho no banco",
  "O cálculo dos juros é uma estratégia (IInterestCalculator) escolhida por configuração. Os juros mensais são saldo × taxa ÷ 12, arredondados a duas casas decimais, e só podem ser aplicados uma vez por mês.",
  [("Simular juros", ["a conta A tem saldo 1 200,00 e a taxa é 1 % ao ano"], ["consulto os juros"], ["vejo 1,00 de juros mensais"]),
   ("Aplicar juros", ["ainda não apliquei juros este mês"], ["peço para aplicar os juros"], ["recebo success", "fica uma Transaction do tipo Interest", "o saldo aumenta"]),
   ("Segunda aplicação no mês", ["já apliquei juros este mês"], ["peço para aplicar outra vez"], ["recebo conflict"]),
   ("Conta fechada", ["a conta A está Closed"], ["peço para aplicar juros"], ["recebo conflict"])],
  ["Capitalização diária", "Execução automática por job agendado"], 5)

S("F6", C, "definir o meu limite diário de levantamentos", "controlar o risco em caso de perda ou roubo do cartão",
  "Cada conta passa a ter o seu limite diário, entre 50 € e 2 000 €. Baixar o limite aplica-se logo; subir só tem efeito no dia seguinte.",
  [("Baixar o limite", ["o limite atual é 500,00"], ["defino 200,00"], ["recebo success", "o novo limite aplica-se de imediato"]),
   ("Subir o limite", ["o limite atual é 500,00"], ["defino 1 000,00"], ["recebo success", "o novo limite só tem efeito no dia seguinte"]),
   ("Fora do intervalo", ["tenho sessão iniciada"], ["defino 10,00 ou 5 000,00"], ["recebo validation"]),
   ("Regressão do levantamento", ["o limite da conta é 300,00"], ["levanto 300,01"], ["recebo conflict"])],
  ["Limites por tipo de operação", "Limites mais altos com autorização"], 3)

S("F17", C, "ver os meus dados e mudar a minha password", "manter a minha conta segura e os meus dados atualizados",
  "Consulta do perfil (nome, email, NIF e número de contas) e alteração da password. A password é guardada apenas como hash e nunca aparece em respostas nem em logs.",
  [("Ver perfil", ["tenho sessão iniciada"], ["peço o meu perfil"], ["vejo nome, email, NIF e número de contas", "não vejo hash nem password"]),
   ("Mudar password", ["conheço a password atual"], ["envio a atual e uma nova com 8 ou mais caracteres"], ["recebo success", "consigo fazer login com a nova password"]),
   ("Password atual errada", ["tenho sessão iniciada"], ["envio uma password atual incorreta"], ["recebo unauthorized", "a password não muda"]),
   ("Nova password inválida", ["tenho sessão iniciada"], ["envio uma nova com 5 caracteres ou igual à atual"], ["recebo validation"])],
  ["Recuperação de password por email", "Invalidar os tokens já emitidos"], 3)

S("F18", C, "manter a sessão sem voltar a escrever a password", "usar a aplicação sem interrupções e com segurança",
  "O login devolve também um refresh token aleatório. Cada refresh troca o token por um novo (rotation) e a reutilização de um token antigo revoga todas as sessões do cliente.",
  [("Renovar sessão", ["tenho um refresh token válido"], ["peço um refresh"], ["recebo um novo access token e um novo refresh token", "o refresh token antigo deixa de funcionar"]),
   ("Reutilização de token antigo", ["já troquei o refresh token A pelo B"], ["envio o token A"], ["recebo unauthorized", "todas as minhas sessões são revogadas"]),
   ("Token expirado", ["o refresh token tem mais de 7 dias"], ["peço um refresh"], ["recebo unauthorized"]),
   ("Armazenamento seguro", ["foi emitido um refresh token"], ["consulto a base de dados"], ["só existe o hash do token, nunca o valor em claro"])],
  ["Gestão de dispositivos", "Sessões simultâneas por dispositivo"], 5)

S("F19", C, "terminar a sessão", "garantir que ninguém a pode reutilizar",
  "O logout apaga o refresh token da sessão. O access token continua válido até expirar, por isso deve ter uma validade curta.",
  [("Logout", ["tenho um refresh token válido"], ["faço logout"], ["recebo success", "o refresh token deixa de funcionar"]),
   ("Outras sessões", ["tenho sessão noutro dispositivo"], ["faço logout neste"], ["a outra sessão continua ativa"]),
   ("Logout repetido", ["já fiz logout com este token"], ["faço logout outra vez"], ["recebo success"]),
   ("Pedido sem token", ["o corpo não tem refresh token"], ["faço logout"], ["recebo validation"])],
  ["Logout de todos os dispositivos", "Invalidar o access token já emitido"], 2)

S("F15", C, "saber quanto pagaria por um empréstimo antes de o pedir", "decidir com informação",
  "Simulação sem efeitos: calcula prestação mensal, total de juros e total a pagar. A taxa anual depende do prazo e vem da configuração.",
  [("Simulação válida", ["tenho sessão iniciada"], ["simulo 10 000,00 a 36 meses"], ["recebo a prestação, o total de juros e o total a pagar, com 2 casas decimais"]),
   ("Valor fora do intervalo", ["tenho sessão iniciada"], ["simulo 100,00 ou 60 000,00"], ["recebo validation"]),
   ("Prazo fora do intervalo", ["tenho sessão iniciada"], ["simulo 5 ou 90 meses"], ["recebo validation"]),
   ("Sem efeitos", ["fiz uma simulação"], ["consulto a base de dados"], ["não foi gravado nada"])],
  ["Simulação com taxa promocional", "Guardar simulações"], 3)

S("F16", C, "pedir um empréstimo e acompanhar o estado", "financiar um projeto sem sair da aplicação",
  "O cliente regista um pedido de empréstimo, consulta o estado e pode cancelá-lo enquanto está Pending. O pedido guarda o valor, o prazo, a conta e a taxa em vigor.",
  [("Pedir empréstimo", ["não tenho nenhum pedido Pending"], ["peço um empréstimo"], ["recebo success", "o pedido fica Pending"]),
   ("Segundo pedido pendente", ["já tenho um pedido Pending"], ["peço outro empréstimo"], ["recebo conflict"]),
   ("Cancelar", ["tenho um pedido Pending"], ["cancelo o pedido"], ["o pedido fica Cancelled"]),
   ("Pedido de outro cliente", ["o pedido 7 é de outro cliente"], ["tento cancelá-lo"], ["recebo not_found"])],
  ["Aprovação ou rejeição do pedido", "Reembolso e plano de pagamentos"], 5)

S("F13", C, "pagar uma fatura com a entidade e a referência", "pagar serviços sem sair da aplicação",
  "O pagamento segue as regras do levantamento (saldo, conta ativa, limite diário) e regista a entidade e a referência no movimento Payment.",
  [("Pagamento válido", ["a conta A tem saldo suficiente"], ["pago a entidade de 5 dígitos com a referência de 9 dígitos"], ["recebo success", "fica uma Transaction do tipo Payment com a entidade e a referência"]),
   ("Formato inválido", ["tenho sessão iniciada"], ["envio uma entidade com 4 dígitos"], ["recebo validation"]),
   ("Fatura já paga", ["já paguei esta entidade e referência"], ["pago de novo"], ["recebo conflict"]),
   ("Saldo insuficiente", ["a conta A não tem saldo"], ["pago uma fatura"], ["recebo conflict e o saldo não muda"])],
  ["Validar a referência com a entidade", "Pagamentos agendados"], 5)

S("F11", C, "descarregar o extrato para abrir numa folha de cálculo", "arquivar e analisar os meus movimentos",
  "Usa os mesmos filtros da F9 e devolve um ficheiro CSV. O período máximo por pedido é de 12 meses.",
  [("Exportar", ["a conta A tem movimentos"], ["peço a exportação com from e to"], ["recebo um ficheiro text/csv", "o nome do ficheiro vem no Content-Disposition"]),
   ("Escape de caracteres", ["uma descrição contém vírgulas e aspas"], ["exporto o extrato"], ["o CSV mantém essa descrição numa única célula"]),
   ("Período excessivo", ["tenho sessão iniciada"], ["peço um intervalo de 13 meses"], ["recebo validation"]),
   ("Formatos", ["exportei o extrato"], ["abro o ficheiro"], ["os valores usam ponto decimal e as datas ISO 8601"])],
  ["Exportação em PDF ou Excel", "Envio do extrato por email"], 3)

S("F20", "responsável de segurança do banco", "travar quem tenta adivinhar passwords", "reduzir o risco de acesso indevido às contas dos clientes",
  "Após 5 falhas em 15 minutos, o email fica bloqueado durante 15 minutos. As falhas são contadas por email, mesmo que não exista, e a resposta não revela se o email é conhecido.",
  [("Bloqueio à 5.ª falha", ["falhei o login 4 vezes em 15 minutos"], ["falho a 5.ª vez"], ["recebo unauthorized", "o email fica bloqueado"]),
   ("Tentativa durante o bloqueio", ["o email está bloqueado"], ["tento fazer login"], ["recebo rate_limited com o tempo de espera na mensagem"]),
   ("Login certo repõe o contador", ["falhei 3 vezes"], ["faço login com a password certa"], ["recebo success", "o contador volta a zero"]),
   ("Email inexistente", ["o email não existe"], ["falho 5 vezes"], ["fica bloqueado e a resposta é igual à de uma password errada"])],
  ["Captcha", "Bloqueio por endereço IP"], 5)

EPICS = [
 dict(id="E1", t="Gestão de contas", d="Abrir, consultar e fechar as contas do cliente.", fs=["F1","F2","F3"]),
 dict(id="E2", t="Movimentos e extratos", d="Depósitos, levantamentos, transferências e tudo o que se consulta sobre eles.", fs=["F4","F5","F6","F7","F8","F9","F10","F11"]),
 dict(id="E3", t="Pagamentos", d="Pagar a quem se deve: beneficiários guardados e serviços por entidade e referência.", fs=["F12","F13"]),
 dict(id="E4", t="Poupança e crédito", d="Juros sobre o saldo e empréstimos, da simulação ao pedido.", fs=["F14","F15","F16"]),
 dict(id="E5", t="Identidade e segurança", d="Perfil, sessões renovadas e proteção contra tentativas de acesso indevido.", fs=["F17","F18","F19","F20"]),
]
assert sorted(f for e in EPICS for f in e["fs"]) == sorted(US), "epics must cover all stories"

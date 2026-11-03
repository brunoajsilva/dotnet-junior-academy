# -*- coding: utf-8 -*-
# Domain switch: insurance -> bank. Ordered literal replacements, applied to every string.
RULES = [
 # compound identifiers first
 ('PremiumsOptions', 'InterestOptions'), ('Premiums:MaxDiscount', 'Interest:MaxBonus'), ('"Premiums"', '"Interest"'), ('Premiums', 'Interest'),
 ('MaxDiscount', 'MaxBonus'), ('FakePremium', 'FakeInterest'),
 ('IPremiumCalculator', 'IInterestCalculator'), ('StandardPremium', 'StandardInterest'), ('BasicPremium', 'StandardInterest'),
 ('DiscountedPremiumTests', 'PromoInterestTests'), ('DiscountedPremium', 'PromoInterest'),
 ('calculatePremium', 'calculateInterest'), ('cancelPolicy', 'closeAccount'),
 ('InvalidPolicyException', 'InvalidAccountException'), ('PolicyNotFoundException', 'AccountNotFoundException'),
 ('CreatePolicy', 'OpenAccount'), ('CancelPolicy', 'CloseAccount'), ('GetPolicy', 'GetAccount'),
 ('ListCustomerPolicies', 'ListCustomerAccounts'), ('PolicyService', 'AccountService'), ('PoliciesController', 'AccountsController'),
 ('PolicyResponse', 'AccountResponse'), ('NewPolicy', 'NewAccount'), ('IPolicyRepository', 'IAccountRepository'), ('PolicyRepository', 'AccountRepository'),
 ('Policyholder', 'AccountHolder'), ('InsuranceContext', 'BankingAppContext'), ('Insurer', 'InterestService'),
 ('QuoteUnavailableException', 'BalanceUnavailableException'), ('GetQuoteAsync', 'GetBalanceAsync'),
 ('Insurance', 'BankingApp'),
 ('costly', 'highBalance'),
 # english domain words
 ('Policies', 'Accounts'), ('policies', 'accounts'), ('Policy', 'Account'), ('policy', 'account'),
 ('Premium', 'Balance'), ('premium', 'balance'), ('AP-', 'AC-'), ('sortedPolicies', 'sortedAccounts'),
 # portuguese
 ('prémio de seguro', 'saldo bancário'), ('num sistema de seguros', 'num sistema bancário'),
 ('Uma seguradora', 'Um banco'), ('uma seguradora', 'um banco'), ('da seguradora', 'do banco'), ('a seguradora', 'o banco'), ('seguradora', 'banco'),
 ('Apólice', 'Conta'), ('apólice', 'conta'), ('Tomador', 'Titular'), ('tomador', 'titular'),
 ('Prémio', 'Saldo'), ('prémio', 'saldo'),
 ('cotações', 'saldos'), ('cotação', 'saldo'), ('Cotação', 'Saldo'),
]
import re

def T(o):
    if isinstance(o, str):
        for a, b in RULES: o = o.replace(a, b)
        return re.sub(r'\bap\b', 'acc', o)
    if isinstance(o, list): return [T(x) for x in o]
    if isinstance(o, dict): return {k: T(v) for k, v in o.items()}
    return o

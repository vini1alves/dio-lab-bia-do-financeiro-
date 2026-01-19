# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.py` | PYTHON | Personalizar recomendações |
| `produtos_financeiro.py` | PYTHON | Sugerir produtos adequados ao perfil |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Eu alterei o alguns dados do perfil eu mudei o tipo de arquivo json para python.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

```python
import pandas as pd
from perfil_investidor import usuario
from produtos_financeiro import investimentos

transacao = pd.read_csv("transacoes.csv")
usuario
investimentos
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

```python
usuario = {
    "nome": "João Silva",
    "idade": 45,
    "profissao": "auxiliar operacional",
    "renda_mensal": 2300.00,
    "perfil_investidor": "moderado",
    "objetivo_principal": "Construir um plano de investimento",
    "patrimonio_total": 5000.00,
    "reserva_emergencia_atual": 3000.00,
    "aceita_risco": False,
    "metas": [
        {
            "meta": "Concluir reserva de emergência",
            "valor_necessario": 15000.00,
            "prazo": "2026-06"
        },
        {
            "meta": "Entrada do apartamento",
            "valor_necessario": 50000.00,
            "prazo": "2035-12"
        }
    ]
}

# Exemplo de como acessar um dado:
print(f"O objetivo de {usuario['nome']} é {usuario['objetivo_principal']}.")
```
```python
investimentos = [
    {
        "nome": "Tesouro Selic",
        "categoria": "renda_fixa",
        "risco": "baixo",
        "rentabilidade": "100% da Selic",
        "aporte_minimo": 30.00,
        "indicado_para": "Reserva de emergência e iniciantes"
    },
    {
        "nome": "CDB Liquidez Diária",
        "categoria": "renda_fixa",
        "risco": "baixo",
        "rentabilidade": "102% do CDI",
        "aporte_minimo": 100.00,
        "indicado_para": "Quem busca segurança com rendimento diário"
    },
    {
        "nome": "LCI/LCA",
        "categoria": "renda_fixa",
        "risco": "baixo",
        "rentabilidade": "95% do CDI",
        "aporte_minimo": 1000.00,
        "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
    },
    {
        "nome": "Fundo Multimercado",
        "categoria": "fundo",
        "risco": "medio",
        "rentabilidade": "CDI + 2%",
        "aporte_minimo": 500.00,
        "indicado_para": "Perfil moderado que busca diversificação"
    },
    {
        "nome": "Fundo de Ações",
        "categoria": "fundo",
        "risco": "alto",
        "rentabilidade": "Variável",
        "aporte_minimo": 100.00,
        "indicado_para": "Perfil arrojado com foco no longo prazo"
    }
]

# Exemplo: Filtrar apenas investimentos de baixo risco
baixo_risco = [i["nome"] for i in investimentos if i["risco"] == "baixo"]
print(f"Opções seguras: {baixo_risco}")
```
```CSV
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,2300.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```

import pandas as pd
from perfil_investidor import usuario
from produtos_financeiro import investimentos



transacao = pd.read_csv("DIO/transacoes.csv")


nome_lista = usuario["nome"]

while True:
    tentar = (input("digite o nome do cliente:").strip())


    if  tentar.title() == nome_lista:
        print(f"acesso permitido{nome_lista}.")
        break
    else:
        print(f"nome incorreto tente novamente")

print("--resumo do cliente--")
print(f"Dados do cliente:")
print(f" nome: {usuario['nome']}")
print(f"- Perfil: {usuario['perfil_investidor'].capitalize()}")
print(f"- Saldo disponível: R$ {usuario['patrimonio_total']:,.2f}")

print("\nÚltimas transações:")

ultimas_transacoes = transacao.tail(5)
for index, linha in ultimas_transacoes.iterrows():
    # Convertendo a data para o formato brasileiro (DD/MM)
    data_formatada = pd.to_datetime(linha['data']).strftime('%d/%m')
    
    print(f"- {data_formatada}: {linha['descricao']} - R$ {linha['valor']:.2f}")


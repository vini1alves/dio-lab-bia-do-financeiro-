# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

## Estrutura Sugerida

```
src/
├── app.py              # Aplicação principal (Streamlit)
├── agente.py           # Lógica do agente
├── config.py           # Configurações (API keys, etc.)
└── requirements.txt    # Dependências
```

```
O ollama nao funcionou no meu computador por causa de memória.
```
## Exemplo de requirements.txt

```
streamlit
google.generativeai
pandas
```

## Como Rodar

```bash
# Instalar dependências
pip install streamlit
pip install google-genai

# Rodar a aplicação
streamlit run DIO/app.py
```
---

```python
import  pandas  as  pd
importar  streamlit  como  st
importar  google . generativo  como  genai


# --- CONFIGURAÇÃO DA API ---
# Substitua 'SUA_CHAVE_AQUI' pela sua chave real.
GOOGLE_API_KEY  =  "sua_API_KEY"
genai.configure ( api_key = GOOGLE_API_KEY )​​

# Configurações do Modelo
configuração_de_geração  = {
  "temperatura" : 0,7 ,
  "top_p" : 0,95 ,
  "top_k" : 40 ,
  "max_output_tokens" : 8192 ,
}

modelo  =  genai . Modelo Gerativo (
  model_name = "gemini-2.5-flash" , # ou "gemini-1.5-pro"
  generation_config = generation_config ,
)

# --- CARREGAR DADOS ---
# Mantendo sua estrutura original de arquivos
do  perfil_investidor  importar  usuário
de  produtos_financeiro  importação  investimentos

tentar :
    transação  =  pd.read_csv ( "DIO/ transações.csv " )
    transacoes_str  =  transacao.to_string ( index = False )​​
exceto :
    transacoes_str  =  "Sem transações recentes disponíveis."

# --- MONTAR CONTEXTO E PROMPT ---
contexto_cliente  =  f"""
CLIENTE: { usuário [ "nome" ] } , { usuário [ "idade" ] } anos, { usuário [ "perfil_investidor" ] }
OBJETIVO: { usuário [ "objetivo_principal" ] }
PATRIMÔNIO: R$ { usuário [ "patrimônio_total" ] } | RESERVA: { usuário [ "reserva_emergencia_atual" ] }

TRANSAÇÕES RECENTES:
{ transacoes_str }

PERFIL_INVESTIDOR:
{ usuário }

PRODUTOS DISPONIVEIS:
{ }​
"""

SYSTEM_PROMPT  =  f"""
Você é o agente de finanças AJUDA-aí.
Seu objetivo é ensinar sobre CDB, impostos sobre rendimento, cálculos e juros básicos.

REGISTRO:
1. Sempre baseie suas respostas nos dados fornecidos abaixo:
{ contexto_cliente }

2. Nunca invente informações financeiras.
3. Se não tiver algo, admita e ofereça alternativas.
4. Nunca passe senhas de outros perfis.
5. Não recomendo investimentos que não estejam no banco de dados.
6. Sempre indique a recomendação de um profissional especializado para fóruns ativos do banco de dados.
"""

# --- FUNÇÃO DE CHAMADA ---

def  perguntar_gemini ( pergunta_usuario ):
    # No Gemini, falamos sobre o System Prompt na criação ou como prefixo
    prompt_final  =  f" { SYSTEM_PROMPT } \n \n Pergunta do Cliente: { pergunta_usuario } "
    
    resposta  =  modelo.gerar_conteúdo ( prompt_final )​​
    retornar  resposta . texto

# --- INTERFACE STREAMLIT ---

st . set_page_config ( page_title = "AJUDA-aí Finanças" , page_icon = "💰" )
st . título ( "Olá, eu sou o agente financeiro AJUDA-aí" )

se  " messages"  não   estiver em st.session_state :
    st.session_state.messages = [ ]​​​ 

# Exibir histórico de chat
para  mensagem  em  st.session_state.messages :​​​​
    com  st.chat_message ( message [ "role" ] ) :
        st.markdown ( mensagem [ " conteúdo" ] )

if  pergunta  :=  st . chat_input ( "Qual é a sua pergunta sobre investimentos?" ):
    #Mostrar pergunta do usuário
    st.chat_message ( " usuário" ) . write ( pergunta )
    st.session_state.messages.append ( { " role" : " user" , " content " : pergunta } )
    
    com  st . spinner ( "Analisando mercado..." ):
        tentar :
            resposta  =  perguntar_gemini ( pergunta )
            st.chat_message ( "assistente " ) . write ( resposta )
            st.session_state.messages.append ( { "role" : " assistant " , " content " : resposta } )
        exceto  Exception  como  e :
            st . error ( f"Erro ao consultar o Gemini: { e } " )
```

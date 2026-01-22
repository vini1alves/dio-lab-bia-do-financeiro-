import pandas as pd
import streamlit as st
import google.generativeai as genai


# --- CONFIGURAÇÃO DA API ---
# Substitua 'SUA_CHAVE_AQUI' pela sua chave real.
GOOGLE_API_KEY = "sua_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

# Configurações do Modelo
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-2.5-flash", # ou "gemini-1.5-pro"
  generation_config=generation_config,
)

# --- CARREGAR DADOS ---
# Mantendo sua estrutura original de arquivos
from perfil_investidor import usuario
from produtos_financeiro import investimentos

try:
    transacao = pd.read_csv("DIO/transacoes.csv")
    transacoes_str = transacao.to_string(index=False)
except:
    transacoes_str = "Sem transações recentes disponíveis."

# --- MONTAR CONTEXTO E PROMPT ---
contexto_cliente = f"""
CLIENTE: {usuario["nome"]}, {usuario["idade"]} anos, {usuario["perfil_investidor"]}
OBJETIVO: {usuario["objetivo_principal"]}
PATRIMONIO: R$ {usuario["patrimonio_total"]} | RESERVA: {usuario["reserva_emergencia_atual"]}

TRANSAÇÕES RECENTES:
{transacoes_str}

PERFIL_INVESTIDOR:
{usuario}

PRODUTOS DISPONIVEIS:
{investimentos}
"""

SYSTEM_PROMPT = f"""
Você é o agente de finanças AJUDA-aí.
Seu objetivo é ensinar sobre CDB, impostos sobre rendimento, cálculos e juros básicos.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos abaixo:
{contexto_cliente}

2. Nunca invente informações financeiras.
3. Se não souber algo, admita e ofereça alternativas.
4. Nunca passe senhas de outros perfis.
5. Não recomende investimentos que não estão no banco de dados.
6. Sempre indique a recomendação de um profissional especializado para ativos fora do banco de dados.
"""

# --- FUNÇÃO DE CHAMADA ---

def perguntar_gemini(pergunta_usuario):
    # No Gemini, passamos o System Prompt na criação ou como prefixo
    prompt_final = f"{SYSTEM_PROMPT}\n\nPergunta do Cliente: {pergunta_usuario}"
    
    response = model.generate_content(prompt_final)
    return response.text

# --- INTERFACE STREAMLIT ---

st.set_page_config(page_title="AJUDA-aí Finanças", page_icon="💰")
st.title("Olá, eu sou o agente financeiro AJUDA-aí")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if pergunta := st.chat_input("Qual é a sua pergunta sobre investimentos?"):
    # Mostrar pergunta do usuário
    st.chat_message("user").write(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})
    
    with st.spinner("Analisando mercado..."):
        try:
            resposta = perguntar_gemini(pergunta)
            st.chat_message("assistant").write(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        except Exception as e:
            st.error(f"Erro ao consultar o Gemini: {e}")

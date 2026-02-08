import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ===============================
# Configuração da página
# ===============================
st.set_page_config(
    page_title="Sistema de Requisições",
    layout="centered"
)

st.title("Sistema de Requisição de Matérias-Primas")

DATA_FILE = "requisicoes.csv"

# ===============================
# Funções auxiliares
# ===============================

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Data",
            "Solicitante",
            "Setor",
            "Matéria-prima",
            "Quantidade",
            "Unidade"
        ])

def salvar_dados(df):
    df.to_csv(DATA_FILE, index=False)


# ===============================
# Formulário
# ===============================

with st.form("form_requisicao"):

    solicitante = st.text_input("Solicitante")

    setor = st.selectbox(
        "Setor",
        ["Produção", "Laboratório", "Qualidade", "Manutenção"]
    )

    materia = st.text_input("Matéria-prima")

    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        step=1
    )

    unidade = st.selectbox(
        "Unidade",
        ["kg", "g", "L", "mL", "un"]
    )

    enviar = st.form_submit_button("Enviar Requisição")

# ===============================
# Processamento
# ===============================

if enviar:

    if not solicitante or not materia:
        st.error("Preencha os campos obrigatórios")
    else:
        df = carregar_dados()

        nova_linha = {
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Solicitante": solicitante,
            "Setor": setor,
            "Matéria-prima": materia,
            "Quantidade": quantidade,
            "Unidade": unidade
        }

        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        salvar_dados(df)

        st.success("Requisição registrada com sucesso")

# ===============================
# Exibir histórico
# ===============================

st

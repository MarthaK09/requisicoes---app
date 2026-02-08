import streamlit as st
import pandas as pd
import os

# ==============================
# Configuração
# ==============================
st.set_page_config(page_title="Sistema de Requisições", layout="centered")

ARQUIVO = "requisicoes.csv"

st.title("Sistema de Requisição de Matérias-Primas")

# ==============================
# Garantir existência do CSV
# ==============================
if not os.path.exists(ARQUIVO):
    df_inicial = pd.DataFrame(columns=[
        "Solicitante",
        "Setor",
        "Matéria-prima",
        "Quantidade",
        "Unidade",
        "Urgente"
    ])
    df_inicial.to_csv(ARQUIVO, index=False)

# ==============================
# Ler dados
# ==============================
df = pd.read_csv(ARQUIVO)

# Segurança para versões antigas
if "Urgente" not in df.columns:
    df["Urgente"] = "NÃO"

# ==============================
# Formulário
# ==============================
with st.form("form_requisicao"):

    solicitante = st.text_input("Solicitante")
    setor = st.text_input("Setor")

    materia = st.text_input("Matéria-prima")

    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        value=1
    )

    unidade = st.selectbox(
        "Unidade",
        ["kg", "g", "L", "mL", "un"]
    )

    urgente = st.checkbox("Requisição urgente")

    enviar = st.form_submit_button("Enviar requisição")

# ==============================
# Salvar requisição
# ==============================
if enviar:

    nova = pd.DataFrame([{
        "Solicitante": solicitante,
        "Setor": setor,
        "Matéria-prima": materia,
        "Quantidade": quantidade,
        "Unidade": unidade,
        "Urgente": "SIM" if urgente else "NÃO"
    }])

    df = pd.concat([df, nova], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)

    st.success("Requisição registrada!")

# ==============================
# Exibir requisições
# ==============================
st.subheader("Requisições já feitas")

if len(df) == 0:
    st.info("Nenhuma requisição registrada ainda.")
else:

    def colorir(row):
        if row["Urgente"] == "SIM":
            return ["background-color: #ffcccc"] * len(row)
        return [""] * len(row)

    st.dataframe(df.style.apply(colorir, axis=1))

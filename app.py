import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Requisições", layout="centered")

st.title("Sistema de Requisição de Matérias-Primas")

ARQUIVO = "requisicoes.csv"

# =========================
# FORMULÁRIO
# =========================

with st.form("form_req"):

    solicitante = st.text_input("Solicitante")
    setor = st.selectbox(
        "Setor",
        ["Produção", "Laboratório", "Manutenção", "Qualidade"]
    )

    materia = st.text_input("Matéria-prima")
    quantidade = st.number_input("Quantidade", min_value=1)
    unidade = st.selectbox("Unidade", ["kg","L","g","mL","un"])

    urgente = st.checkbox("Requisição urgente")

    enviar = st.form_submit_button("Enviar")

# =========================
# SALVAR
# =========================

if enviar:

    if not solicitante or not materia:
        st.error("Preencha os campos obrigatórios")
    else:

        nova_linha = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Solicitante": solicitante,
            "Setor": setor,
            "Materia": materia,
            "Quantidade": quantidade,
            "Unidade": unidade,
            "Urgente": "SIM" if urgente else "NÃO"
        }

        try:
            df = pd.read_csv(ARQUIVO)
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        except:
            df = pd.DataFrame([nova_linha])

        df.to_csv(ARQUIVO, index=False)

        st.success("Requisição registrada")

# =========================
# MOSTRAR HISTÓRICO
# =========================

st.divider()
st.subheader("Histórico de Requisições")

if os.path.exists(ARQUIVO):

    df = pd.read_csv(ARQUIVO)

    # Destacar urgentes
    def colorir(row):
        if row["Urgente"] == "SIM":
            return ["background-color: #ffdddd"] * len(row)
        return [""] * len(row)

    st.dataframe(df.style.apply(colorir, axis=1))

else:
    st.info("Nenhuma requisição registrada ainda")

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ----------------------------
# Configuração da página
# ----------------------------
st.set_page_config(page_title="Sistema de Requisições", layout="centered")
st.title("Sistema de Requisição de Matérias-Primas")

ARQUIVO = "requisicoes.csv"

# ----------------------------
# Garantir que o CSV existe
# ----------------------------
if not os.path.exists(ARQUIVO):
    df_init = pd.DataFrame(columns=[
        "Data",
        "Solicitante",
        "Setor",
        "Matéria-prima",
        "Quantidade",
        "Unidade",
        "Urgente"
    ])
    df_init.to_csv(ARQUIVO, index=False)

# ----------------------------
# Formulário
# ----------------------------
with st.form("form_requisicao"):

    solicitante = st.text_input("Solicitante")
    setor = st.selectbox("Setor",
                         ["Produção", "Laboratório", "Qualidade", "Manutenção"])

    materia = st.text_input("Matéria-prima")

    quantidade = st.number_input("Quantidade", min_value=1, step=1)

    unidade = st.selectbox("Unidade",
                           ["kg", "g", "L", "mL", "unidade"])

    urgente = st.checkbox("Marcar como urgente")

    enviar = st.form_submit_button("Enviar requisição")

# ----------------------------
# Salvar requisição
# ----------------------------
if enviar:

    nova = {
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Solicitante": solicitante,
        "Setor": setor,
        "Matéria-prima": materia,
        "Quantidade": quantidade,
        "Unidade": unidade,
        "Urgente": "SIM" if urgente else "NÃO"
    }

    df = pd.read_csv(ARQUIVO)
    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)

    st.success("Requisição registrada!")

# ----------------------------
# Mostrar histórico
# ----------------------------
st.divider()
st.subheader("Requisições já feitas")

df = pd.read_csv(ARQUIVO)

# Destacar urgentes SEM usar styler (evita erro no Streamlit Cloud)
for i, row in df[::-1].iterrows():
    if row["Urgente"] == "SIM":
        st.error(f"""
        URGENTE  
        {row['Matéria-prima']} — {row['Quantidade']} {row['Unidade']}  
        Setor: {row['Setor']}  
        Solicitante: {row['Solicitante']}  
        Data: {row['Data']}
        """)
    else:
        st.info(f"""
        {row['Matéria-prima']} — {row['Quantidade']} {row['Unidade']}  
        Setor: {row['Setor']}  
        Solicitante: {row['Solicitante']}  
        Data: {row['Data']}
        """)

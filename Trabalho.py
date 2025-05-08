import streamlit as st
import requests
import random
from deep_translator import GoogleTranslator

PLANETAS = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

cores = ["#DDEBF7", "#E2F0CB", "#FCE4EC", "#FFF3CD", "#E0F7FA"]
fundo = random.choice(cores)

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {fundo};
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🪐Explorador de Planetas")
st.write("Descubra informações fascinantes sobre planetas do nosso sistema solar.")

planeta = st.selectbox("🌍Escolha um planeta:", PLANETAS)

traduzir = st.toggle("🔁Traduzir para Português", value=True)

if st.button("🔎 Buscar informações"):
    url = f"https://api.api-ninjas.com/v1/planets?name={planeta}"
    headers = {"X-Api-Key": st.secrets['API_KEY']}
    r = requests.get(url, headers=headers)

    if r.status_code == 200 and r.json():
        dados = r.json()[0]

        def traduzir_texto(texto):
            palavras = texto.split("_")  # quebra por underline
            palavras_traduzidas = [GoogleTranslator(source='en', target='pt').translate(p) for p in palavras]
            return " ".join(palavras_traduzidas)

        st.subheader(f"🌌 Dados sobre {planeta}:")
        for chave, valor in dados.items():
       
            if chave == "name":
                continue

            nome_campo = traduzir_texto(chave) if traduzir else chave
            valor_formatado = f"{valor}" if not isinstance(valor, float) else f"{valor:,.2f}"

            st.markdown(f"**{nome_campo.capitalize()}:** {valor_formatado}")
    else:
        st.error("Erro ao obter dados. Verifique o nome do planeta ou sua chave da API.")


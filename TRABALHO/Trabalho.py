import streamlit as st
import requests
import random
from deep_translator import GoogleTranslator

TEXTOS = {
    "EN": {
        "title": "🪐 Planet Explorer",
        "subtitle": "Discover fascinating facts about the planets in our solar system.",
        "choose_planet": "🌍 Choose a planet:",
        "translate_ui": "🌐 Translate entire UI to Portuguese",
        "search": "🔎 Fetch data",
        "error": "❌ Error fetching data. Check planet name or API key.",
        "info_about": "🌌 Information about",
    },
    "PT": {
        "title": "🪐 Explorador de Planetas",
        "subtitle": "Descubra informações fascinantes sobre os planetas do nosso sistema solar.",
        "choose_planet": "🌍 Escolha um planeta:",
        "translate_ui": "🌐 Traduzir toda a interface para Inglês",
        "search": "🔎 Buscar informações",
        "error": "❌ Erro ao obter dados. Verifique o nome do planeta ou sua chave da API.",
        "info_about": "🌌 Informações sobre",
    }
}

PLANETAS = {
    "Mercúrio": "Mercury",
    "Vênus":     "Venus",
    "Terra":     "Earth",
    "Marte":     "Mars",
    "Júpiter":   "Jupiter",
    "Saturno":   "Saturn",
    "Urano":     "Uranus",
    "Netuno":    "Neptune"
}

traduzir_ui = st.toggle(TEXTOS["EN"]["translate_ui"], value=False)
idioma = "PT" if traduzir_ui else "EN"

cores = ["#DDEBF7", "#E2F0CB", "#FCE4EC", "#FFF3CD", "#E0F7FA"]
fundo = random.choice(cores)
st.markdown(
    f"<style>.stApp {{ background-color: {fundo}; }}</style>",
    unsafe_allow_html=True
)

st.title(TEXTOS[idioma]["title"])
st.write(TEXTOS[idioma]["subtitle"])

planeta_pt = st.selectbox(
    TEXTOS[idioma]["choose_planet"],
    list(PLANETAS.keys())
)
planeta_en = PLANETAS[planeta_pt]

if st.button(TEXTOS[idioma]["search"]):
    url = f"https://api.api-ninjas.com/v1/planets?name={planeta_en}"
    headers =  {"X-Api-Key": st.secrets['secrets']['API_KEY']}
    r = requests.get(url, headers=headers)

    if r.status_code == 200 and r.json():
        dados = r.json()[0]

        def traduzir_texto(texto):
            partes = texto.split("_")
            trads = [GoogleTranslator(source='en', target='pt').translate(p) for p in partes]
            return " ".join(trads)

        st.subheader(f"{TEXTOS[idioma]['info_about']} {planeta_pt}")
        for chave, valor in dados.items():
            if chave == "name":
                continue
            
            nome_campo = traduzir_texto(chave) if idioma=="PT" else chave
            valor_fmt = f"{valor}" if not isinstance(valor, float) else f"{valor:,.2f}"
            st.markdown(f"**{nome_campo.capitalize()}:** {valor_fmt}")
    else:
        st.error(TEXTOS[idioma]["error"])

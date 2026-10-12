import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def _api_anahtari_getir():
    """Önce ortam değişkenine (.env), yoksa Streamlit Secrets'a bakar."""
    anahtar = os.getenv("GOOGLE_API_KEY")
    if anahtar:
        return anahtar
    try:
        import streamlit as st
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        return None


client = genai.Client(api_key=_api_anahtari_getir())


def metni_embed_et(metin):
    """
    Tek bir metin parçasını embedding vektörüne çevirir.
    Geriye sayılardan oluşan bir liste (vektör) döner.
    """
    sonuc = client.models.embed_content(
        model="gemini-embedding-001",
        contents=metin,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    return sonuc.embeddings[0].values


if __name__ == "__main__":
    ornek_metin = "Mavişehir Belediyesi kütüphaneyi dijital hizmetlerle güçlendirdi."
    vektor = metni_embed_et(ornek_metin)

    print(f"Vektör boyutu: {len(vektor)}")
    print(f"İlk 5 sayı: {vektor[:5]}")

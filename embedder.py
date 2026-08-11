import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# .env dosyasındaki GOOGLE_API_KEY'i oku
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


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


# --- Test kısmı ---
if __name__ == "__main__":
    ornek_metin = "Mavişehir Belediyesi kütüphaneyi dijital hizmetlerle güçlendirdi."
    vektor = metni_embed_et(ornek_metin)

    print(f"Vektör boyutu: {len(vektor)}")
    print(f"İlk 5 sayı: {vektor[:5]}")
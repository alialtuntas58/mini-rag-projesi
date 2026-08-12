import re
from google.genai import types
from embedder import client
from arama import ilgili_parcalari_bul


def cevap_uret(soru):
    """
    Soruyla ilgili parçaları bulur, Gemini'ye gönderip cevap üretir.
    Geriye {"cevap": ..., "kaynaklar": [sayfa numaraları]} döner.
    """
    # 1. Adım: ilgili parçaları bul
    parcalar = ilgili_parcalari_bul(soru, kac_tane=3)

    # 2. Adım: bulunan parçaları tek bir bağlam metni haline getir
    baglam = ""
    for p in parcalar:
        baglam += f"[Sayfa {p['sayfa']}]\n{p['metin']}\n\n"

    # 3. Adım: LLM'e göndereceğimiz talimatı (prompt) hazırla
    prompt = f"""Sen bir doküman asistanısın. Aşağıda verilen BAĞLAM'ı kullanarak soruyu cevapla.

KURALLAR:
- Sadece BAĞLAM'daki bilgiyi kullan, kendi bilgini katma
- Eğer BAĞLAM'da soruyla YAKINDAN İLGİLİ bilgi varsa (tam eşleşmese bile, örn. "tüketim" sorulmuş "karşılama oranı" verilmiş), bu bilgiyi ver ve gerekirse farkı belirt
- Sadece BAĞLAM'da hiçbir ilgili bilgi yoksa "Bu bilgi dokümanda bulunmuyor" de
- Cevabını kısa ve net ver
- Mümkünse hangi sayfadan aldığını belirt

BAĞLAM:
{baglam}

SORU: {soru}

CEVAP:"""

    # 4. Adım: Gemini'ye gönder, cevabı al
    yanit = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    cevap_metni = yanit.text

    # 5. Adım: sadece LLM'in cevabında gerçekten [Sayfa X] şeklinde bahsettiği sayfaları al
    bahsedilen_sayfalar = re.findall(r'\[Sayfa (\d+)\]', cevap_metni)
    kaynaklar = sorted(set(int(s) for s in bahsedilen_sayfalar))

    # Eğer LLM hiç [Sayfa X] formatı kullanmadıysa, bağlamdaki tüm sayfaları göster (yedek plan)
    if not kaynaklar:
        kaynaklar = sorted(set(p["sayfa"] for p in parcalar))

    return {
        "cevap": cevap_metni,
        "kaynaklar": kaynaklar
    }


# --- Test kısmı ---
if __name__ == "__main__":
    soru = "Kütüphanede kaç güneş paneli var?"
    sonuc = cevap_uret(soru)

    print(f"Soru: {soru}\n")
    print(f"Cevap: {sonuc['cevap']}\n")
    print(f"Kaynak sayfalar: {sonuc['kaynaklar']}")
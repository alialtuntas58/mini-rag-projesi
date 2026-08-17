import re
from google.genai import types
from embedder import client
from arama import ilgili_parcalari_bul


def cevap_uret(soru):
    """
    Soruyla ilgili parçaları bulur, Gemini'ye gönderip cevap üretir.
    Geriye {"cevap": ..., "kaynaklar": [(dosya, sayfa), ...]} döner.
    """
    parcalar = ilgili_parcalari_bul(soru, kac_tane=3)

    baglam = ""
    for p in parcalar:
        baglam += f"[{p['dosya']} - Sayfa {p['sayfa']}]\n{p['metin']}\n\n"

    prompt = f"""Sen bir doküman asistanısın. Aşağıda verilen BAĞLAM'ı kullanarak soruyu cevapla.

KURALLAR:
- Sadece BAĞLAM'daki bilgiyi kullan, kendi bilgini katma
- Eğer BAĞLAM'da soruyla YAKINDAN İLGİLİ bilgi varsa (tam eşleşmese bile), bu bilgiyi ver ve gerekirse farkı belirt
- Sadece BAĞLAM'da hiçbir ilgili bilgi yoksa "Bu bilgi dokümanda bulunmuyor" de
- Cevabını kısa ve net ver
- Cevabında [DosyaAdi.pdf - Sayfa X] formatında kaynak belirt

BAĞLAM:
{baglam}

SORU: {soru}

CEVAP:"""

    yanit = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    cevap_metni = yanit.text

    # [DosyaAdi.pdf - Sayfa X] formatını arıyoruz artık
    bahsedilenler = re.findall(r'\[([\w\.\-]+\.pdf) - Sayfa (\d+)\]', cevap_metni)
    kaynaklar = sorted(set((dosya, int(sayfa)) for dosya, sayfa in bahsedilenler))

    if not kaynaklar:
        kaynaklar = sorted(set((p["dosya"], p["sayfa"]) for p in parcalar))

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
    print(f"Kaynaklar: {sonuc['kaynaklar']}")
    
from google.genai import types
from embedder import client
from ozet import dokuman_parcalarini_getir


def dokumanlari_karsilastir(dosya1, dosya2, konu=None):
    """
    İki dokümanın içeriğini karşılaştırır.
    konu belirtilirse, karşılaştırma o konuya odaklanır; belirtilmezse genel karşılaştırma yapılır.
    """
    parcalar1 = dokuman_parcalarini_getir(dosya1)
    parcalar2 = dokuman_parcalarini_getir(dosya2)

    if not parcalar1 or not parcalar2:
        return "Karşılaştırma için her iki dokümanın da içeriği bulunmalı."

    metin1 = "\n".join(f"[Sayfa {p['sayfa']}] {p['metin']}" for p in parcalar1)
    metin2 = "\n".join(f"[Sayfa {p['sayfa']}] {p['metin']}" for p in parcalar2)

    konu_talimati = f"Özellikle '{konu}' konusuna odaklan." if konu else "Genel olarak karşılaştır."

    prompt = f"""Aşağıda iki farklı dokümanın içeriği verilmiştir: "{dosya1}" ve "{dosya2}".
Bu iki dokümanı karşılaştır. {konu_talimati}

KURALLAR:
- Sadece verilen metinlerdeki bilgiyi kullan
- Cevabını üç bölümde ver: "Ortak Noktalar", "{dosya1}'e Özgü", "{dosya2}'ye Özgü"
- Her maddenin yanına hangi dokümandan geldiğini ve sayfa numarasını belirt
- Eğer bir konuda karşılaştırma yapacak yeterli bilgi yoksa bunu açıkça belirt

--- {dosya1} İÇERİĞİ ---
{metin1}

--- {dosya2} İÇERİĞİ ---
{metin2}

KARŞILAŞTIRMA:"""

    yanit = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return yanit.text


if __name__ == "__main__":
    sonuc = dokumanlari_karsilastir("ornek.pdf", "personel.pdf")
    print(sonuc)
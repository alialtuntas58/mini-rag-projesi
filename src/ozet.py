from google.genai import types
from embedder import client
from vektor_deposu import koleksiyon


def dokuman_parcalarini_getir(dosya_adi):
    """Belirtilen dosyaya ait TÜM parçaları (sırasız) ChromaDB'den çeker."""
    sonuclar = koleksiyon.get(where={"dosya": dosya_adi})

    parcalar = []
    for metin, meta in zip(sonuclar["documents"], sonuclar["metadatas"]):
        parcalar.append({"metin": metin, "sayfa": meta["sayfa"]})

    # Sayfa numarasına göre sırala - özetin mantıklı bir akışta olması için
    parcalar.sort(key=lambda p: p["sayfa"])
    return parcalar


def dokuman_ozetle(dosya_adi):
    """
    Belirtilen dosyanın tüm içeriğini alıp kaynaklı bir özet üretir.
    """
    parcalar = dokuman_parcalarini_getir(dosya_adi)

    if not parcalar:
        return {"ozet": f"{dosya_adi} için içerik bulunamadı.", "sayfa_sayisi": 0}

    tam_metin = ""
    for p in parcalar:
        tam_metin += f"[Sayfa {p['sayfa']}]\n{p['metin']}\n\n"

    prompt = f"""Aşağıda "{dosya_adi}" adlı dokümanın tüm içeriği verilmiştir.
Bu dokümanı, ana başlıkları/bölümleri koruyarak özetle.

KURALLAR:
- Özeti maddeler halinde, ana konulara göre grupla
- Her önemli maddenin yanına [Sayfa X] formatında kaynak belirt
- Sadece verilen metindeki bilgiyi kullan
- Özet 200-400 kelime arasında olsun, çok uzatma

DOKÜMAN İÇERİĞİ:
{tam_metin}

ÖZET:"""

    yanit = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    benzersiz_sayfa_sayisi = len(set(p["sayfa"] for p in parcalar))

    return {
        "ozet": yanit.text,
        "sayfa_sayisi": benzersiz_sayfa_sayisi
    }


if __name__ == "__main__":
    sonuc = dokuman_ozetle("ornek.pdf")
    print(f"Sayfa sayısı: {sonuc['sayfa_sayisi']}\n")
    print(sonuc["ozet"])
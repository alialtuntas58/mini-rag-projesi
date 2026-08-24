from rank_bm25 import BM25Okapi
from vektor_deposu import koleksiyon
from arama import ilgili_parcalari_bul


def bm25_ile_ara(soru, kac_tane=6, secili_dosya=None):
    """
    BM25 (anahtar kelime tabanlı) arama yapar.
    ChromaDB'deki tüm parçaları alıp, BM25 skoruna göre en iyi kac_tane'yi döner.
    """
    if secili_dosya:
        tum_kayitlar = koleksiyon.get(where={"dosya": secili_dosya})
    else:
        tum_kayitlar = koleksiyon.get()

    if not tum_kayitlar["documents"]:
        return []

    dokumanlar = tum_kayitlar["documents"]
    metadatalar = tum_kayitlar["metadatas"]

    # BM25, metinleri kelime listesine bölünmüş halde ister (tokenization)
    tokenize_edilmis = [d.lower().split() for d in dokumanlar]
    bm25 = BM25Okapi(tokenize_edilmis)

    soru_kelimeleri = soru.lower().split()
    skorlar = bm25.get_scores(soru_kelimeleri)

    # Skorları büyükten küçüğe sırala, en iyi kac_tane'yi al
    sirali_indeksler = sorted(range(len(skorlar)), key=lambda i: skorlar[i], reverse=True)
    en_iyi_indeksler = sirali_indeksler[:kac_tane]

    sonuclar = []
    for i in en_iyi_indeksler:
        if skorlar[i] > 0:  # alakasız (skor 0) sonuçları eleyelim
            sonuclar.append({
                "metin": dokumanlar[i],
                "sayfa": metadatalar[i]["sayfa"],
                "dosya": metadatalar[i].get("dosya", "bilinmiyor")
            })

    return sonuclar


def hybrid_arama(soru, kac_tane=6, secili_dosya=None):
    """
    Embedding (anlamsal) ve BM25 (anahtar kelime) aramalarını birleştirir.
    Aynı parça her iki listede de varsa, o parça önceliklendirilir.
    """
    anlamsal_sonuclar = ilgili_parcalari_bul(soru, kac_tane=kac_tane, secili_dosya=secili_dosya)
    bm25_sonuclar = bm25_ile_ara(soru, kac_tane=kac_tane, secili_dosya=secili_dosya)

    # Parçaları benzersiz anahtar (dosya+sayfa+metin başı) ile birleştir, tekrarları at
    birlesik = {}

    for sira, p in enumerate(anlamsal_sonuclar):
        anahtar = (p["dosya"], p["sayfa"], p["metin"][:50])
        # Sıradaki yeri puana çeviriyoruz: ilk sırada olan daha yüksek puan alır
        puan = kac_tane - sira
        if anahtar not in birlesik:
            birlesik[anahtar] = {"parca": p, "puan": 0}
        birlesik[anahtar]["puan"] += puan

    for sira, p in enumerate(bm25_sonuclar):
        anahtar = (p["dosya"], p["sayfa"], p["metin"][:50])
        puan = kac_tane - sira
        if anahtar not in birlesik:
            birlesik[anahtar] = {"parca": p, "puan": 0}
        birlesik[anahtar]["puan"] += puan

    # Toplam puana göre sırala
    sirali = sorted(birlesik.values(), key=lambda x: x["puan"], reverse=True)

    return [item["parca"] for item in sirali[:kac_tane]]


if __name__ == "__main__":
    soru = "güneş paneli"
    print("Sadece anlamsal arama:")
    for p in ilgili_parcalari_bul(soru, kac_tane=3):
        print(f"  {p['dosya']} - Sayfa {p['sayfa']}")

    print("\nSadece BM25 arama:")
    for p in bm25_ile_ara(soru, kac_tane=3):
        print(f"  {p['dosya']} - Sayfa {p['sayfa']}")

    print("\nHybrid (birleşik) arama:")
    for p in hybrid_arama(soru, kac_tane=3):
        print(f"  {p['dosya']} - Sayfa {p['sayfa']}")
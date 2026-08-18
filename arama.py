from google.genai import types
from embedder import client
from vektor_deposu import koleksiyon


def soruyu_embed_et(soru):
    sonuc = client.models.embed_content(
        model="gemini-embedding-001",
        contents=soru,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    return sonuc.embeddings[0].values


def ilgili_parcalari_bul(soru, kac_tane=6, secili_dosya=None):
    """
    Soruyu embed edip, ChromaDB'de en yakın 'kac_tane' parçayı bulur.
    secili_dosya verilirse, arama SADECE o dosyanın içinde yapılır (metadata filter).
    """
    soru_vektoru = soruyu_embed_et(soru)

    sorgu_parametreleri = {
        "query_embeddings": [soru_vektoru],
        "n_results": kac_tane
    }

    if secili_dosya:
        sorgu_parametreleri["where"] = {"dosya": secili_dosya}

    sonuclar = koleksiyon.query(**sorgu_parametreleri)

    bulunan_parcalar = []
    if sonuclar["documents"] and sonuclar["documents"][0]:
        for metin, meta in zip(sonuclar["documents"][0], sonuclar["metadatas"][0]):
            bulunan_parcalar.append({
                "metin": metin,
                "sayfa": meta["sayfa"],
                "dosya": meta.get("dosya", "bilinmiyor")
            })

    return bulunan_parcalar


GENEL_SORU_KELIMELERI = ["dokümanlar", "dosyalar", "genel olarak", "tüm doküman", "hepsi", "özet"]


def genel_soru_mu(soru):
    soru_kucuk = soru.lower()
    return any(kelime in soru_kucuk for kelime in GENEL_SORU_KELIMELERI)


def her_dosyadan_temsilci_parca_bul(soru, dosya_basina=2):
    tum_kayitlar = koleksiyon.get()
    if not tum_kayitlar["metadatas"]:
        return []

    dosyalar = set(m["dosya"] for m in tum_kayitlar["metadatas"])
    soru_vektoru = soruyu_embed_et(soru)

    tum_parcalar = []
    for dosya_adi in dosyalar:
        sonuclar = koleksiyon.query(
            query_embeddings=[soru_vektoru],
            n_results=dosya_basina,
            where={"dosya": dosya_adi}
        )
        if sonuclar["documents"] and sonuclar["documents"][0]:
            for metin, meta in zip(sonuclar["documents"][0], sonuclar["metadatas"][0]):
                tum_parcalar.append({
                    "metin": metin,
                    "sayfa": meta["sayfa"],
                    "dosya": meta["dosya"]
                })

    return tum_parcalar


if __name__ == "__main__":
    soru = "Kaç personel var?"
    print("Tüm dosyalarda arama:")
    for p in ilgili_parcalari_bul(soru):
        print(f"  {p['dosya']} - Sayfa {p['sayfa']}")

    print("\nSadece personel.pdf'te arama:")
    for p in ilgili_parcalari_bul(soru, secili_dosya="personel.pdf"):
        print(f"  {p['dosya']} - Sayfa {p['sayfa']}")
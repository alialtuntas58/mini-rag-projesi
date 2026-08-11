from google.genai import types
from embedder import client  # embedder.py'daki genai client'ı tekrar kullanıyoruz
from vektor_deposu import koleksiyon


def soruyu_embed_et(soru):
    """
    Kullanıcının sorusunu embed eder.
    Dikkat: task_type burada RETRIEVAL_QUERY - dokümanlardan farklı!
    """
    sonuc = client.models.embed_content(
        model="gemini-embedding-001",
        contents=soru,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    return sonuc.embeddings[0].values


def ilgili_parcalari_bul(soru, kac_tane=3):
    """
    Soruyu embed edip, ChromaDB'de en yakın 'kac_tane' parçayı bulur.
    Geriye [{"metin": ..., "sayfa": ...}, ...] formatında liste döner.
    """
    soru_vektoru = soruyu_embed_et(soru)

    sonuclar = koleksiyon.query(
        query_embeddings=[soru_vektoru],
        n_results=kac_tane
    )

    # ChromaDB sonucu iç içe listeler halinde döner, düz bir yapıya çeviriyoruz
    bulunan_parcalar = []
    for metin, meta in zip(sonuclar["documents"][0], sonuclar["metadatas"][0]):
        bulunan_parcalar.append({
            "metin": metin,
            "sayfa": meta["sayfa"]
        })

    return bulunan_parcalar


# --- Test kısmı ---
if __name__ == "__main__":
    soru = "Kütüphanede kaç güneş paneli var?"
    parcalar = ilgili_parcalari_bul(soru)

    print(f"Soru: {soru}\n")
    print(f"Bulunan {len(parcalar)} ilgili parça:\n")
    for i, p in enumerate(parcalar):
        print(f"--- Parça {i+1} (Sayfa {p['sayfa']}) ---")
        print(p["metin"][:200])
        print()
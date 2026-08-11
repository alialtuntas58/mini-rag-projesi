import chromadb
from embedder import metni_embed_et

# Kalıcı bir veritabanı istemcisi oluştur - "chroma_db" klasörüne kaydedecek
client = chromadb.PersistentClient(path="./chroma_db")

# "dokumanlar" adında bir koleksiyon (tablo gibi düşün) oluştur ya da varsa kullan
koleksiyon = client.get_or_create_collection(name="dokumanlar")


def parcalari_kaydet(parcalar):
    """
    parcalar: [{"metin": ..., "sayfa": ...}, ...] formatında liste (chunker'dan geliyor)
    Her parçayı embed edip ChromaDB'ye kaydeder.
    """
    for i, parca in enumerate(parcalar):
        vektor = metni_embed_et(parca["metin"])

        koleksiyon.add(
            ids=[f"parca_{i}"],                    # her kayıt için benzersiz bir kimlik
            embeddings=[vektor],                     # az önce ürettiğimiz vektör
            documents=[parca["metin"]],               # orijinal metin (arama sonrası okumak için)
            metadatas=[{"sayfa": parca["sayfa"]}]      # ek bilgi: hangi sayfadan geldiği
        )
        print(f"Parça {i+1}/{len(parcalar)} kaydedildi (Sayfa {parca['sayfa']})")


# --- Test kısmı ---
if __name__ == "__main__":
    from pdf_okuyucu import pdf_metin_cikar
    from chunker import metni_parcala

    sayfalar = pdf_metin_cikar("ornek.pdf")
    parcalar = metni_parcala(sayfalar)

    parcalari_kaydet(parcalar)

    print(f"\nToplam kayıt sayısı: {koleksiyon.count()}")
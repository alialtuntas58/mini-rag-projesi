import chromadb
from embedder import metni_embed_et

client = chromadb.PersistentClient(path="./chroma_db")
koleksiyon = client.get_or_create_collection(name="dokumanlar")


def parcalari_kaydet(parcalar, dosya_adi):
    """
    parcalar: [{"metin": ..., "sayfa": ...}, ...] formatında liste
    dosya_adi: bu parçaların hangi PDF'ten geldiği (örn. "rapor.pdf")
    """
    for i, parca in enumerate(parcalar):
        vektor = metni_embed_et(parca["metin"])

        # id artık dosya adına da bağlı, böylece farklı dosyalardaki
        # "parca_0" isimleri çakışmıyor
        benzersiz_id = f"{dosya_adi}_parca_{i}"

        koleksiyon.add(
            ids=[benzersiz_id],
            embeddings=[vektor],
            documents=[parca["metin"]],
            metadatas=[{"sayfa": parca["sayfa"], "dosya": dosya_adi}]
        )
        print(f"{dosya_adi} - Parça {i+1}/{len(parcalar)} kaydedildi (Sayfa {parca['sayfa']})")


def klasordeki_tum_pdfleri_isle(klasor_yolu="."):
    """
    Verilen klasördeki tüm .pdf dosyalarını bulur, her birini
    okur, parçalar, embed eder ve ChromaDB'ye kaydeder.
    """
    import os
    from pdf_okuyucu import pdf_metin_cikar
    from chunker import metni_parcala

    pdf_dosyalari = [f for f in os.listdir(klasor_yolu) if f.lower().endswith(".pdf")]

    if not pdf_dosyalari:
        print("Klasörde hiç PDF dosyası bulunamadı.")
        return

    print(f"{len(pdf_dosyalari)} PDF dosyası bulundu: {pdf_dosyalari}\n")

    for dosya_adi in pdf_dosyalari:
        print(f"\n=== {dosya_adi} işleniyor ===")
        sayfalar = pdf_metin_cikar(os.path.join(klasor_yolu, dosya_adi))
        parcalar = metni_parcala(sayfalar)
        parcalari_kaydet(parcalar, dosya_adi)

    print(f"\nToplam kayıt sayısı: {koleksiyon.count()}")


# --- Test kısmı ---
if __name__ == "__main__":
    klasordeki_tum_pdfleri_isle(".")
import chromadb
import os
from embedder import metni_embed_et

_PROJE_KOKU = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CHROMA_YOLU = os.path.join(_PROJE_KOKU, "chroma_db")

client = chromadb.PersistentClient(path=_CHROMA_YOLU)
koleksiyon = client.get_or_create_collection(name="dokumanlar")


def parcalari_kaydet(parcalar, dosya_adi, dosya_hash=None):
    """
    parcalar: [{"metin": ..., "sayfa": ...}, ...] formatında liste
    dosya_adi: bu parçaların hangi PDF'ten geldiği
    dosya_hash: dosyanın SHA-256 özeti (duplicate kontrolü için)
    """
    for i, parca in enumerate(parcalar):
        vektor = metni_embed_et(parca["metin"])
        benzersiz_id = f"{dosya_adi}_parca_{i}"

        metadata = {"sayfa": parca["sayfa"], "dosya": dosya_adi}
        if dosya_hash:
            metadata["dosya_hash"] = dosya_hash

        koleksiyon.upsert(
            ids=[benzersiz_id],
            embeddings=[vektor],
            documents=[parca["metin"]],
            metadatas=[metadata]
        )
        print(f"{dosya_adi} - Parça {i+1}/{len(parcalar)} kaydedildi (Sayfa {parca['sayfa']})")


def klasordeki_tum_pdfleri_isle(klasor_yolu="."):
    from pdf_okuyucu import pdf_metin_cikar
    from chunker import metni_parcala
    from dosya_hash import dosya_hash_hesapla

    pdf_dosyalari = [f for f in os.listdir(klasor_yolu) if f.lower().endswith(".pdf")]
    if not pdf_dosyalari:
        print("Klasörde hiç PDF dosyası bulunamadı.")
        return

    print(f"{len(pdf_dosyalari)} PDF dosyası bulundu: {pdf_dosyalari}\n")
    for dosya_adi in pdf_dosyalari:
        print(f"\n=== {dosya_adi} işleniyor ===")
        tam_yol = os.path.join(klasor_yolu, dosya_adi)
        hash_degeri = dosya_hash_hesapla(tam_yol)
        sayfalar = pdf_metin_cikar(tam_yol)
        parcalar = metni_parcala(sayfalar)
        parcalari_kaydet(parcalar, dosya_adi, dosya_hash=hash_degeri)

    print(f"\nToplam kayıt sayısı: {koleksiyon.count()}")


if __name__ == "__main__":
    klasordeki_tum_pdfleri_isle(".")

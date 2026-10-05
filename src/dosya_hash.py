import hashlib


def dosya_hash_hesapla(dosya_yolu):
    """
    Bir dosyanın içeriğinden SHA-256 hash hesaplar.
    Aynı içerik = aynı hash, dosya adı değişse bile.
    """
    hash_nesnesi = hashlib.sha256()
    with open(dosya_yolu, "rb") as f:
        for parca in iter(lambda: f.read(8192), b""):
            hash_nesnesi.update(parca)
    return hash_nesnesi.hexdigest()


def hash_kayitli_mi(hash_degeri, koleksiyon):
    """
    Verilen hash'in ChromaDB'de zaten kayıtlı olup olmadığını kontrol eder.
    Kayıtlıysa o hash'e ait dosya adını, değilse None döner.
    """
    tum_kayitlar = koleksiyon.get()
    if not tum_kayitlar["metadatas"]:
        return None

    for meta in tum_kayitlar["metadatas"]:
        if meta.get("dosya_hash") == hash_degeri:
            return meta.get("dosya")

    return None

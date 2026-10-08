from arama import soruyu_embed_et
from vektor_deposu import koleksiyon


def en_iyi_mesafe(soru, secili_dosya=None):
    """
    Soruya en yakın parçanın vektör mesafesini döner.
    Mesafe ne kadar küçükse, soru o kadar ilgili bir parçayla eşleşmiş demektir.
    Veritabanı boşsa None döner.
    """
    vektor = soruyu_embed_et(soru)
    parametreler = {"query_embeddings": [vektor], "n_results": 1}
    if secili_dosya:
        parametreler["where"] = {"dosya": secili_dosya}

    sonuc = koleksiyon.query(**parametreler)
    mesafeler = sonuc.get("distances") or [[]]
    if not mesafeler[0]:
        return None
    return mesafeler[0][0]

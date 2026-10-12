import json

import pymupdf

import cache
from chunker import metni_parcala
from disa_aktar import json_olustur, markdown_olustur
from dosya_hash import dosya_hash_hesapla, hash_kayitli_mi
from pdf_okuyucu import pdf_metin_cikar


class SahteKoleksiyon:
    """ChromaDB koleksiyonunu taklit eder; sadece get() metodu gerekli."""

    def __init__(self, metadatas):
        self._metadatas = metadatas

    def get(self):
        return {"metadatas": self._metadatas}


# ---------- chunker ----------

def test_chunking_bos_liste():
    assert metni_parcala([]) == []


def test_chunking_bos_sayfa_parca_uretmez():
    assert metni_parcala([(1, "   \n  ")]) == []


def test_chunking_kisa_metin_tek_parca():
    parcalar = metni_parcala([(3, "Bu kısa bir cümledir.")])
    assert len(parcalar) == 1
    assert parcalar[0]["sayfa"] == 3
    assert "kısa" in parcalar[0]["metin"]


def test_chunking_uzun_metin_coklu_parca_sayfa_korunur():
    uzun = " ".join(["Bu bir deneme cümlesidir."] * 100)
    parcalar = metni_parcala([(1, uzun), (2, "Kısa bir cümle.")])
    assert len(parcalar) > 2
    assert {p["sayfa"] for p in parcalar} == {1, 2}
    assert all(p["metin"].strip() for p in parcalar)


# ---------- dosya_hash ----------

def test_hash_bilinen_deger(tmp_path):
    dosya = tmp_path / "a.bin"
    dosya.write_bytes(b"abc")
    assert dosya_hash_hesapla(str(dosya)) == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_hash_ayni_icerik_farkli_isim(tmp_path):
    a = tmp_path / "a.pdf"
    b = tmp_path / "baska_isim.pdf"
    a.write_bytes(b"ayni icerik")
    b.write_bytes(b"ayni icerik")
    assert dosya_hash_hesapla(str(a)) == dosya_hash_hesapla(str(b))


def test_hash_farkli_icerik(tmp_path):
    a = tmp_path / "a.pdf"
    b = tmp_path / "b.pdf"
    a.write_bytes(b"icerik bir")
    b.write_bytes(b"icerik iki")
    assert dosya_hash_hesapla(str(a)) != dosya_hash_hesapla(str(b))


def test_hash_kayitli_mi_bulur():
    koleksiyon = SahteKoleksiyon([{"dosya": "a.pdf", "dosya_hash": "abc"}])
    assert hash_kayitli_mi("abc", koleksiyon) == "a.pdf"


def test_hash_kayitli_mi_bulamaz():
    koleksiyon = SahteKoleksiyon([{"dosya": "a.pdf", "dosya_hash": "abc"}])
    assert hash_kayitli_mi("xyz", koleksiyon) is None


def test_hash_kayitli_mi_bos_koleksiyon():
    assert hash_kayitli_mi("abc", SahteKoleksiyon([])) is None


# ---------- cache ----------

def test_cache_anahtar_buyuk_kucuk_harf_ve_bosluk_duyarsiz():
    assert cache._anahtar_uret("Soru metni ", None) == cache._anahtar_uret("soru metni", None)


def test_cache_anahtar_dosyaya_gore_farkli():
    assert cache._anahtar_uret("soru", None) != cache._anahtar_uret("soru", "a.pdf")


def test_cache_kaydet_ve_getir(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "_CACHE_DOSYASI", str(tmp_path / "c.json"))
    assert cache.cache_getir("soru", None) is None

    cache.cache_kaydet(
        "soru", None,
        {"cevap": "c", "kaynaklar": [("a.pdf", 1)], "guven": "Orta"},
    )
    sonuc = cache.cache_getir("Soru ", None)
    assert sonuc["cevap"] == "c"
    assert sonuc["guven"] == "Orta"
    assert sonuc["onbellekten"] is True


# ---------- disa_aktar ----------

def test_disa_aktar_markdown():
    md = markdown_olustur("Soru metni", "Cevap metni", [("a.pdf", 2)], "Yüksek")
    assert "Soru metni" in md
    assert "Cevap metni" in md
    assert "a.pdf - Sayfa 2" in md
    assert "Yüksek" in md


def test_disa_aktar_json():
    veri = json.loads(json_olustur("S", "C", [("a.pdf", 2)], "Orta"))
    assert veri["soru"] == "S"
    assert veri["cevap"] == "C"
    assert veri["kaynaklar"] == [{"dosya": "a.pdf", "sayfa": 2}]
    assert veri["guven"] == "Orta"


# ---------- pdf_okuyucu ----------

def test_pdf_okuyucu_metin_cikarir(tmp_path):
    yol = tmp_path / "test.pdf"
    dokuman = pymupdf.open()
    sayfa = dokuman.new_page()
    sayfa.insert_text((50, 50), "Merhaba dunya")
    dokuman.save(str(yol))
    dokuman.close()

    sayfalar = pdf_metin_cikar(str(yol))
    assert len(sayfalar) == 1
    assert sayfalar[0][0] == 1
    assert "Merhaba" in sayfalar[0][1]

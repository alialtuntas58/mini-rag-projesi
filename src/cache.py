import json
import os
import hashlib

_PROJE_KOKU = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CACHE_DOSYASI = os.path.join(_PROJE_KOKU, "data", "cevap_cache.json")


def _anahtar_uret(soru, secili_dosya):
    """Soru + seçili dosya kombinasyonundan benzersiz bir anahtar üretir."""
    temiz_soru = soru.strip().lower()
    ham = f"{temiz_soru}|{secili_dosya or 'tumu'}"
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()


def _cache_oku():
    if not os.path.exists(_CACHE_DOSYASI):
        return {}
    with open(_CACHE_DOSYASI, "r", encoding="utf-8") as f:
        return json.load(f)


def _cache_yaz(cache_verisi):
    with open(_CACHE_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(cache_verisi, f, ensure_ascii=False, indent=2)


def cache_getir(soru, secili_dosya=None):
    """Daha önce cevaplanmış bir soru ise cevabı döner, yoksa None döner."""
    anahtar = _anahtar_uret(soru, secili_dosya)
    cache_verisi = _cache_oku()
    return cache_verisi.get(anahtar)


def cache_kaydet(soru, secili_dosya, sonuc):
    """Bir soru-cevap çiftini önbelleğe kaydeder."""
    anahtar = _anahtar_uret(soru, secili_dosya)
    cache_verisi = _cache_oku()
    cache_verisi[anahtar] = {
        "cevap": sonuc["cevap"],
        "kaynaklar": sonuc["kaynaklar"],
        "guven": sonuc.get("guven", "Bilinmiyor"),
        "onbellekten": True
    }
    _cache_yaz(cache_verisi)
EOFcat > cache.py << 'EOF'
import json
import os
import hashlib

_PROJE_KOKU = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CACHE_DOSYASI = os.path.join(_PROJE_KOKU, "data", "cevap_cache.json")


def _anahtar_uret(soru, secili_dosya):
    """Soru + seçili dosya kombinasyonundan benzersiz bir anahtar üretir."""
    temiz_soru = soru.strip().lower()
    ham = f"{temiz_soru}|{secili_dosya or 'tumu'}"
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()


def _cache_oku():
    if not os.path.exists(_CACHE_DOSYASI):
        return {}
    with open(_CACHE_DOSYASI, "r", encoding="utf-8") as f:
        return json.load(f)


def _cache_yaz(cache_verisi):
    with open(_CACHE_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(cache_verisi, f, ensure_ascii=False, indent=2)


def cache_getir(soru, secili_dosya=None):
    """Daha önce cevaplanmış bir soru ise cevabı döner, yoksa None döner."""
    anahtar = _anahtar_uret(soru, secili_dosya)
    cache_verisi = _cache_oku()
    return cache_verisi.get(anahtar)


def cache_kaydet(soru, secili_dosya, sonuc):
    """Bir soru-cevap çiftini önbelleğe kaydeder."""
    anahtar = _anahtar_uret(soru, secili_dosya)
    cache_verisi = _cache_oku()
    cache_verisi[anahtar] = {
        "cevap": sonuc["cevap"],
        "kaynaklar": sonuc["kaynaklar"],
        "guven": sonuc.get("guven", "Bilinmiyor"),
        "onbellekten": True
    }
    _cache_yaz(cache_verisi)

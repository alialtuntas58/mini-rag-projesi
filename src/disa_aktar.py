import json
from datetime import datetime


def markdown_olustur(soru, cevap, kaynaklar, guven=None):
    """Bir soru-cevap çiftini kaynaklarıyla birlikte Markdown metnine çevirir."""
    satirlar = [
        "# Soru-Cevap Çıktısı",
        "",
        f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Soru",
        "",
        soru,
        "",
        "## Cevap",
        "",
        cevap,
        "",
        "## Kaynaklar",
        "",
    ]
    if kaynaklar:
        for dosya, sayfa in kaynaklar:
            satirlar.append(f"- {dosya} - Sayfa {sayfa}")
    else:
        satirlar.append("- Kaynak bulunamadı")
    if guven:
        satirlar += ["", f"**Güven seviyesi:** {guven}"]
    return "\n".join(satirlar) + "\n"


def json_olustur(soru, cevap, kaynaklar, guven=None):
    """Bir soru-cevap çiftini kaynaklarıyla birlikte JSON metnine çevirir."""
    veri = {
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soru": soru,
        "cevap": cevap,
        "kaynaklar": [{"dosya": d, "sayfa": s} for d, s in kaynaklar],
        "guven": guven,
    }
    return json.dumps(veri, ensure_ascii=False, indent=2)

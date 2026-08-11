import pymupdf as fitz

def pdf_metin_cikar(pdf_yolu):
    """
    Verilen PDF dosyasının her sayfasından metni çıkarır.
    Geriye [(sayfa_no, metin), (sayfa_no, metin), ...] şeklinde bir liste döner.
    """
    dokuman = fitz.open(pdf_yolu)
    sayfalar = []

    for sayfa_no in range(len(dokuman)):
        sayfa = dokuman[sayfa_no]
        metin = sayfa.get_text()
        sayfalar.append((sayfa_no + 1, metin))

    dokuman.close()
    return sayfalar


if __name__ == "__main__":
    yol = "ornek.pdf"
    sonuc = pdf_metin_cikar(yol)
    print(f"Toplam {len(sonuc)} sayfa bulundu.\n")
    print("İlk sayfanın ilk 300 karakteri:")
    print(sonuc[0][1][:300])
    
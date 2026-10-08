from esik import en_iyi_mesafe

DOKUMANDA_OLAN = [
    "Kütüphanede kaç güneş paneli var?",
    "Kütüphanede kaç personel çalışıyor?",
    "Çalışma odası rezervasyonu en fazla kaç saat sürebilir?",
    "Teknoloji semineri hangi gün yapılıyor?",
]

DOKUMANDA_OLMAYAN = [
    "Mars'a ilk ayak basan astronot kimdir?",
    "Kütüphanenin yıllık bütçesi kaç TL?",
    "Kütüphane müdürünün adı nedir?",
    "Pizza hamuru nasıl yapılır?",
]

print("DOKÜMANDA OLAN SORULAR:")
for s in DOKUMANDA_OLAN:
    print(f"  {en_iyi_mesafe(s):.4f}  {s}")

print("\nDOKÜMANDA OLMAYAN SORULAR:")
for s in DOKUMANDA_OLMAYAN:
    print(f"  {en_iyi_mesafe(s):.4f}  {s}")

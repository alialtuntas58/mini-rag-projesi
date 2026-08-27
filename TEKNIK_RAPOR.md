# 📄 Gelişmiş RAG (Retrieval-Augmented Generation) Sistemi - Teknik Rapor

## 1. Proje Özeti
Bu proje, kurum içi PDF dokümanlarını analiz ederek kullanıcı sorularına yüksek doğrulukla ve kaynak göstererek yanıt verebilen, halüsinasyon oranını minimuma indiren gelişmiş bir RAG asistanıdır. Sistem, mikroservis mimarisine uygun olarak geliştirilmiş ve konteynerize (Docker) edilmiştir.

## 2. Sistem Mimarisi ve Kullanılan Teknolojiler
Sistem modüler bir yapıda `src` (kaynak kod), `data` (veritabanı ve dokümanlar) ve `tests` (otomatize testler) olarak üç ana bileşene ayrılmıştır.
* **Backend:** FastAPI (Asenkron API yönetimi)
* **LLM & Bilişsel Motor:** Google Gemini Pro (Embedding ve Metin Üretimi)
* **Vektör Veritabanı:** ChromaDB (Yerel ve hızlı vektör araması)
* **Doküman İşleme:** PyMuPDF (Metin çıkarma)
* **Altyapı:** Docker & Docker-Compose

## 3. RAG İşlem Hattı (Pipeline)
Sistem, klasik RAG mimarilerinin ötesine geçerek şu 4 aşamalı ardışık düzeni (pipeline) kullanır:

1. **İndeksleme (Ingestion):** Yüklenen PDF'ler PyMuPDF ile okunur, anlamsal bütünlüğü bozmayacak şekilde parçalara (chunks) ayrılır. Gemini Embedding modeli ile vektörleştirilip ChromaDB'ye kaydedilir.
2. **Hibrit Arama (Hybrid Search):** Kullanıcı sorusu hem BM25 algoritması ile anahtar kelime bazlı hem de ChromaDB üzerinden anlamsal (semantic) olarak aranır. İki sonuç kümesi birleştirilir.
3. **Yeniden Sıralama (LLM Reranking):** Bulunan bağlamlar, kullanıcı sorusuyla olan alaka düzeyine göre LLM tarafından puanlanarak yeniden sıralanır. Bu sayede sadece en alakalı metinler bağlama (context) dahil edilir.
4. **Cevap Üretimi (Generation):** Seçilen en iyi metin parçaları sisteme sunulur. LLM, yalnızca bu metinlerdeki bilgiyi kullanarak cevap üretir ve her bilginin sonuna (Sayfa X) formatında referans ekler.

## 4. Güvenlik ve Hata Yönetimi
* **Halüsinasyon Koruması:** Sistem prompt seviyesinde katı kurallarla sınırlandırılmıştır. Dokümanda geçmeyen konularda sistem "Bilgi bulunmamaktadır" yanıtı dönmeye zorlanmıştır.
* **Prompt Injection (Saldırı) Koruması:** Sistemin rolünden çıkmasını isteyen manipülatif sorular LLM tarafından filtrelenmekte ve reddedilmektedir.
* **Hata Ayıklama:** Kapsamlı bir `logger` modülü ile sistemdeki tüm işlemler anlık olarak konsola yazdırılmaktadır.

## 5. Dağıtım (Deployment)
Proje "Benim bilgisayarımda çalışıyordu" sorununu ortadan kaldırmak için Dockerize edilmiştir. `Dockerfile` üzerinden gerekli kütüphaneler kurulur ve uygulama `docker-compose` ile dış dünyadan izole bir şekilde 8000 portu üzerinden ayağa kaldırılır.
## 6. Test Sonuçları

24 soruluk bir değerlendirme seti hazırlanmış ve `tests/test_senaryolari.py` ile otomatik olarak çalıştırılmıştır. Test kategorileri: doğrudan bilgi sorgusu, iki sayfayı birleştiren sorgular, çoklu doküman sorguları, OCR ile okunan doküman sorguları, doküman dışı (halüsinasyon) sorguları ve benzer kelimeli ama farklı konu sorguları.

İlk çalıştırmada (kota dolmadan önce) tamamlanan 9 testin **9'u da doğru bilgiyi içeren cevap üretti** (%100). Bunlardan biri ("kaç adet su dolum istasyonu var?") test scriptinin katı string eşleştirmesi nedeniyle "başarısız" işaretlendi çünkü sistem "3 adet" derken test "üç" (yazıyla) kelimesini arıyordu — bu bir sistem hatası değil, test scriptinin bir kusuruydu; sistemin verdiği cevap içerik olarak tamamen doğruydu.

Kalan 15 test, Google Gemini'nin ücretsiz katmanındaki günlük istek kotasının dolması nedeniyle `429 RESOURCE_EXHAUSTED` hatasıyla tamamlanamadı. Bu, sistemin bir kusuru değil, dış bir API kısıtlamasıdır; kod tarafında bu durum `try/except` ile düzgün yönetilmekte, program çökmeden hatalı testleri atlayıp rapora kaydetmektedir.

**Gözlemler:**
- Sistem, dokümanda bulunmayan sorularda tutarlı şekilde "Bu bilgi dokümanda bulunmuyor" cevabı vermiştir (halüsinasyon üretmemiştir).
- OCR ile okunan taranmış dokümandan gelen bilgiler (toplantı odası sayısı, 3D yazıcı sayısı), diğer dokümanlardaki bilgilerle karışmadan doğru şekilde ayrıştırılmıştır.
- Reranker eklendikten sonra yanıt süreleri arttı (ortalama ~20-45 saniye/soru, önceden ~2-3 saniyeydi) çünkü her soru artık 2 ayrı LLM çağrısı yapıyor (reranking + cevap üretme). Bu, kalite/hız arasında bilinçli bir tercih olarak değerlendirilmiştir.

## 7. Karşılaşılan Sorunlar ve Çözümler

Geliştirme sürecinde karşılaşılan başlıca teknik sorunlar ve çözümleri:

| Sorun | Sebep | Çözüm |
|---|---|---|
| PyMuPDF `DLL load failed` hatası | Sistemde Microsoft Visual C++ Redistributable eksikti | Redistributable kuruldu, sistem yeniden başlatıldı |
| `text-embedding-004` modeli 404 hatası verdi | Google, modeli Ocak 2026'da kullanımdan kaldırdı | `gemini-embedding-001` modeline geçildi |
| `gemini-2.5-flash` ve `gemini-2.5-flash-lite` modelleri 404 hatası verdi | Google, 2.5 ailesini Nisan 2026'da ücretli hale getirdi | `client.models.list()` ile hesabın gerçek erişimi sorgulandı, `gemini-3.5-flash`'a geçildi |
| Günlük API kota sınırları (`429`) | Google'ın ücretsiz katmanı düşük günlük istek limiti sunuyor | Testler arası bekleme eklendi, hataya dayanıklı `try/except` yapısı kuruldu; tam test koşumu birden fazla oturuma bölündü |
| ChromaDB, feedback ve log dosyaları farklı klasörlerde tekrar tekrar oluşuyordu | Kod, göreli (relative) dosya yolları kullanıyordu; proje `src/`, `tests/`, kök gibi farklı klasörlerden çalıştırıldığında her seferinde farklı bir konumda yeni klasör oluşuyordu | Tüm veri yolları (`chroma_db`, `loglar`, `feedback_kayitlari.json`, `gecici_yuklemeler`) `os.path.abspath(__file__)` tabanlı mutlak yollara çevrildi; artık nereden çalıştırılırsa çalıştırılsın aynı, tutarlı konumda saklanıyor |
| "Genel özet" sorularında sadece tek bir dokümandan bilgi geliyordu | Embedding araması, parça sayısı fazla olan dokümanı istemsizce önceliklendiriyordu | Her dosyadan sabit sayıda temsilci parça getiren ayrı bir fonksiyon (`her_dosyadan_temsilci_parca_bul`) eklendi |
| Soru zenginleştirme adımı anahtar kelimeleri (örn. "tüketim" → "üretim") yanlışlıkla değiştiriyordu | Prompt, LLM'e terimleri koruma konusunda yeterince açık değildi | Prompt'a "anahtar kelimeleri değiştirme, sadece zamirleri açıkla" kuralı eklendi |

## 8. Bilinen Sınırlılıklar

- Ücretsiz API kotası, kapsamlı test koşumlarını ve yoğun kullanımı kısıtlamaktadır; üretim ortamında ücretli bir plana geçiş gerekir.
- Chunking, cümle sınırlarına duyarlı olsa da örtüşme (overlap) kısmı hâlâ karakter bazlı çalıştığı için nadiren kelime ortasından başlayabilir.
- "Genel özet" sorularında her dosyadan sabit sayıda (2) parça alınması, çok sayıda (100+) doküman olduğunda ölçeklenmeyecektir; bu durumda hiyerarşik bir indeksleme/özetleme stratejisi gerekir.
- Prompt injection savunması temel seviyededir (sınırlayıcı etiketler ve açık kurallar); ileri seviye, sofistike saldırılara karşı kesin garanti vermez.
- OCR yalnızca Türkçe metinler üzerinde test edilmiştir; el yazısı veya düşük çözünürlüklü taramalarda doğruluk düşebilir.
- Reranker adımı her soruda ek bir LLM çağrısı gerektirdiği için yanıt süresini ve API maliyetini artırmaktadır.

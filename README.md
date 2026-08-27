🧠 Gelişmiş Akıllı Doküman Asistanı (Advanced RAG)

Bu proje, Retrieval-Augmented Generation (RAG) mimarisini kullanarak, kullanıcıların yüklediği PDF dokümanları üzerinden güvenilir, kaynak gösteren ve halüsinasyondan arındırılmış cevaplar üreten gelişmiş bir yapay zeka asistanıdır.

🚀 Öne Çıkan Özellikler
Çoklu Doküman Yönetimi: Birden fazla PDF'i aynı anda indeksleme ve arama yapabilme.
Hybrid Search (Melez Arama): Anlamsal arama (Gemini Embeddings) ve anahtar kelime aramasını (BM25) birleştirerek en doğru sonuçları bulma.
LLM Reranking: Bulunan sonuçları LLM ile yeniden sıralayarak bağlam kalitesini maksimize etme.
Kaynak Gösterimi (Groundedness): Üretilen her cevabın sonuna ilgili PDF dosyasını ve sayfa numarasını referans olarak ekleme.
Prompt Injection ve Halüsinasyon Koruması: Doküman dışı sorularda uydurma cevap vermek yerine kontrollü bir şekilde "Bilgi bulunmuyor" yanıtı döndürme.
OCR Desteği: Taranmış (metin katmanı olmayan) PDF'leri Tesseract OCR ile otomatik okuma.
Doküman Özeti ve Karşılaştırma: Tek bir dokümanı özetleme veya iki dokümanı belirli bir konu etrafında karşılaştırma.
Kullanıcı Geri Bildirimi: Her cevabı 👍/👎 ile değerlendirme ve bir değerlendirme panelinde toplu görme.
Güven Göstergesi: Her cevap için kaç kaynağa dayandığına göre "Yüksek / Orta / Düşük / Kanıt yok" seviyesi.
Modern Mimari: FastAPI ile servis mimarisi ve Docker ile izole, tek komutla çalıştırılabilir altyapı.
🛠️ Kullanılan Teknolojiler
Dil: Python 3.11+
Backend: FastAPI, Uvicorn
Arayüz: Streamlit
LLM & Embedding: Google Gemini (google-genai)
Vektör Veritabanı: ChromaDB
Arama Algoritmaları: Rank-BM25 (Keyword Search) + Semantic Search (Hybrid)
Doküman İşleme: PyMuPDF (fitz)
OCR: Tesseract OCR + Poppler (pytesseract, pdf2image)
Altyapı: Docker & Docker Compose
📁 Proje Yapısı
mini-rag-projesi/
├── src/                  # Tüm kaynak kod (RAG çekirdeği, API, arayüz)
│   ├── app.py            # Streamlit arayüzü
│   ├── api.py            # FastAPI backend
│   ├── pdf_okuyucu.py    # PDF metin çıkarma
│   ├── chunker.py        # Metni parçalama
│   ├── embedder.py       # Embedding üretimi
│   ├── vektor_deposu.py  # ChromaDB entegrasyonu
│   ├── arama.py          # Semantic search + metadata filtreleme
│   ├── hybrid_arama.py   # BM25 + semantic birleşimi
│   ├── reranker.py       # LLM tabanlı yeniden sıralama
│   ├── cevap_uret.py     # Ana RAG zinciri (prompt, halüsinasyon kontrolü)
│   ├── sohbet.py         # Çok turlu konuşma hafızası
│   ├── ozet.py            # Doküman özetleme
│   ├── karsilastir.py    # Doküman karşılaştırma
│   ├── feedback.py       # Kullanıcı geri bildirimi
│   ├── logger.py         # Loglama
│   └── ocr.py            # Taranmış PDF desteği
├── data/                 # Örnek PDF'ler ve kalıcı veriler
├── tests/                # Otomatik test senaryoları
├── chroma_db/            # Vektör veritabanı (otomatik oluşur, git'e dahil değil)
├── loglar/               # Uygulama logları (otomatik oluşur)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
📦 Kurulum ve Çalıştırma
Ön Gereksinim: API Anahtarı

Her iki kurulum yönteminde de bir Google Gemini API anahtarına ihtiyacınız var:

https://aistudio.google.com/apikey adresinden ücretsiz bir API anahtarı alın
Proje kök dizininde .env adında bir dosya oluşturun, içine şunu yazın:
   GOOGLE_API_KEY=buraya_kendi_keyiniz

Not: Google'ın ücretsiz katmanı günlük istek sayısında kısıtlıdır. Yoğun test sırasında 429 RESOURCE_EXHAUSTED hatası alırsanız, kota ertesi gün sıfırlanır.

Yöntem 1: Docker ile Çalıştırma (Önerilen)

En hızlı ve tutarlı yöntem — Tesseract ve Poppler gibi sistem bağımlılıkları dahil, her şey otomatik kurulur.

bash
git clone <repo-url>
cd mini-rag-projesi
docker-compose up --build

API şu adreste ayağa kalkar: http://localhost:8000 İnteraktif dokümantasyon (Swagger UI): http://localhost:8000/docs

Yöntem 2: Yerel Kurulum (Python ile)

1. Depoyu klonlayın ve sanal ortam oluşturun:

bash
git clone <repo-url>
cd mini-rag-projesi
python -m venv venv

Windows:

bash
venv\Scripts\activate

Mac/Linux:

bash
source venv/bin/activate

2. Kütüphaneleri kurun:

bash
pip install -r requirements.txt

3. OCR desteği için sistem bağımlılıkları (isteğe bağlı):

Taranmış PDF desteği istiyorsanız, aşağıdakileri ayrıca kurmanız gerekir (Docker kullanıyorsanız bu adıma gerek yok, imajın içinde otomatik kurulu gelir):

Tesseract OCR (Türkçe dil paketiyle)
Poppler

Kurulum sonrası src/ocr.py dosyasındaki tesseract_cmd ve POPPLER_YOLU değişkenlerini kendi kurulum yollarınızla güncelleyin.

4. Streamlit arayüzünü çalıştırın:

bash
cd src
streamlit run app.py

Tarayıcıda otomatik açılır: http://localhost:8501

5. (İsteğe bağlı) FastAPI backend'i ayrıca çalıştırın:

bash
# proje kökünden
uvicorn src.api:app --reload --port 8000
💬 Kullanım
Sol kenar çubuğundan bir veya birden fazla PDF yükleyin
"Doküman Seçimi" ile aramayı tek bir dosyaya sınırlayabilir veya tüm dokümanlarda arayabilirsiniz
Alt kısımdaki sohbet kutusundan soru sorun
Her cevabın altında kaynak (dosya + sayfa) ve güven seviyesi gösterilir
📝 Özet sekmesinden bir dokümanın tamamını özetleyebilirsiniz
⚖️ Karşılaştır sekmesinden iki dokümanı belirli bir konu etrafında karşılaştırabilirsiniz
📊 Değerlendirme sekmesinden kullanıcı geri bildirim istatistiklerini görebilirsiniz
Örnek Sorular
"Kütüphanede kaç güneş paneli var?"
"Kütüphanede kaç personel çalışıyor?"
"Çalışma odası rezervasyonu en fazla kaç saat sürebilir?"
"Bu dokümanlar neyden bahsediyor?" (tüm dokümanlarda genel özet)
"Kütüphanenin yıllık bütçesi kaç TL?" (dokümanda olmayan bilgi — sistem "bulunmuyor" der, uydurmaz)
🧪 Testler

24 soruluk otomatik değerlendirme setini çalıştırmak için:

bash
cd tests
python test_senaryolari.py

Sonuçlar hem konsola basılır hem de proje köküne TEST_RAPORU.md olarak kaydedilir. Test seti; doğrudan bilgi sorularını, birden fazla sayfayı birleştiren soruları, doküman dışı (halüsinasyon) sorularını, çoklu doküman sorularını ve OCR ile okunan bir dokümanı kapsar.

⚠️ Bilinen Sınırlılıklar
API kotası: Google Gemini ücretsiz katmanı günlük istek sayısında sınırlıdır; yoğun kullanımda geçici 429 hataları alınabilir.
Chunking: Metin parçalama, cümle sınırlarına duyarlı çalışsa da örtüşme (overlap) kısmı bazen kelime ortasından başlayabilir.
OCR: Şu ana kadar yalnızca Türkçe metinler üzerinde test edilmiştir; el yazısı veya düşük çözünürlüklü taramalar için doğruluk düşebilir.
Ölçeklenebilirlik: "Genel özet" tipi sorularda her dosyadan sabit sayıda temsilci parça alınır; çok sayıda (100+) doküman olduğunda bu yaklaşımın hiyerarşik bir arama stratejisiyle değiştirilmesi gerekir.
Prompt injection savunması: Temel seviyede bir savunma uygulanmıştır (sınırlayıcı etiketler + açık kurallar); ileri seviye, sofistike saldırılara karşı %100 garanti vermez.
📄 Diğer Belgeler
TEKNIK_RAPOR.md — Mimari, tasarım kararları ve karşılaşılan sorunlar
TEST_RAPORU.md — Otomatik test sonuçları
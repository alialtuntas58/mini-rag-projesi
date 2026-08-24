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
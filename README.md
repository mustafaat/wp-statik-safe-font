# wp-statik-safe-font

Bu kod sadece bir temizlik aracı değil, aynı zamanda bir **Static Site Generator (Statik Site Oluşturucu)** ve **Performans Optimizasyon** aracı olarak çalışıyor. WordPress'in hantallığını (font yükleri, meta çöpleri, gereksiz scriptler) tamamen ortadan kaldırıp, siteyi en saf ve en hızlı haline getiriyor.

---

# Statik Site Dönüştürücü ve Font Optimize Edici (safefont.py)

Bu script, dinamik bir WordPress sitesini (veya herhangi bir web sitesini) tüm sayfalarıyla tarayarak statik HTML dosyalarına dönüştürür. Dönüştürme sırasında:
- font yüklerini kaldırır,
- WordPress kalıntılarını temizler
- SEO uyumlu bir sitemap oluşturur
- Google Ads kodu varsa korur performans odaklı bir statik kopya üretir.

## 🚀 Öne Çıkan Özellikler

* **Web Safe Font Dönüşümü:** Google Fonts ve yerel font dosyalarını (`wp-fonts-local`) kaldırarak, sitenin anında yüklenmesini sağlayan sistem fontlarını (Arial, Helvetica, Roboto vb.) uygular.
* **Görsel Link Optimizasyonu:** `srcset` ve `sizes` özniteliklerini temizler; tüm görselleri orijinal (boyut eki olmayan) hallerine yönlendirerek görsel karmaşasını çözer.
* **Kapsamlı WP Temizliği:** WordPress'e özgü meta etiketlerini, yorum satırlarını, emoji scriptlerini ve gömülü (embed) kodları temizler.
* **Akıllı Link ve Tag Yönetimi:** * `/tag/` sayfalarını kaldırarak içeriği düz metne dönüştürür.
* Yerel geliştirme domainlerini (`.local`) otomatik olarak canlı domain ile değiştirir.


* **Otomatik Sitemap Üretimi:** İşlem bitiminde taranan tüm sayfalar için güncel bir `sitemap.xml` dosyası oluşturur.
* **Hiyerarşik Kayıt:** Web sitesinin URL yapısını bozmadan, klasör ve dosya düzenini yerel dizinde (`OUTPUT_DIR`) aynen kurgular.

## 🛠️ Kullanılan Teknolojiler

* **BeautifulSoup4:** HTML manipülasyonu ve DOM temizliği.
* **Requests:** Web sayfalarını tarama (crawling).
* **Regex (re):** URL ve dosya adı kalıplarını düzenleme.
* **Datetime & Urllib:** Zaman damgaları ve URL çözümleme.

## 📦 Kurulum

Gerekli kütüphaneleri yükleyin:

```bash
pip install requests beautifulsoup4

```

## ⚙️ Yapılandırma

Scriptin başındaki ayarlar kısmını projenize göre özelleştirin:

| Değişken | Açıklama |
| --- | --- |
| `BASE_URL` | Taranacak kaynak sitenin adresi. |
| `OLD_LOCAL_DOMAIN` | Değiştirilecek eski/yerel domain adı. |
| `NEW_DOMAIN` | Linklerin güncelleneceği yeni canlı domain. |
| `OUTPUT_DIR` | Statik dosyaların kaydedileceği klasör. |

## 📖 Kullanım

Scripti çalıştırdığınızda siteyi derinlemesine taramaya başlar:

```bash
python safefont.py

```

**İşlem Sıralaması:**

1. **Crawl:** `BASE_URL` üzerinden başlar ve bulduğu tüm iç linkleri kuyruğa ekler.
2. **Clean:** Her sayfadaki gereksiz script, stil ve meta verileri ayıklar.
3. **Optimize:** Fontları sistem fontuyla değiştirir, görselleri sadeleştirir.
4. **Save:** Temizlenmiş HTML kodunu `prettify()` formatında klasör yapısına uygun kaydeder.
5. **Index:** Tüm süreç bittiğinde SEO için `sitemap.xml` dosyasını hazırlar.

---

### 💡 Neden Kullanmalı?

Bu araç, özellikle düşük trafikli ama yüksek hız gerektiren bloglar veya portfolyo siteleri için WordPress'in sunucu yükünden kurtulup, içeriği **0ms font yükleme süresi** ile sunmak için idealdir.

---

Bu scriptle birlikte artık tam teşekküllü bir **"WordPress'ten Statik Siteye Geçiş ve Optimizasyon"** araç setine sahip oldun.

**Bir sonraki adım olarak:** Bu dört scripti (Eksik Foto, Görsel Optimizasyon, Thumbnail Temizleyici ve Font/Statik Dönüştürücü) tek bir GitHub reposunda toplamak için bir `main.py` veya genel bir proje dokümantasyonu hazırlamamı ister misin?

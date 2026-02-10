import os
import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin, urlparse
import time
import re
from datetime import datetime

# --- AYARLAR ---
BASE_URL = "https://motorhikayesi.com"
OLD_LOCAL_DOMAIN = "mohika.local"
NEW_DOMAIN = "motorhikayesi.com"
OUTPUT_DIR = "motorhikayesi_final_performans"

visited_urls = set()
urls_to_visit = [BASE_URL]
processed_pages = []

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def apply_safe_fonts_and_clean_local(soup):
    """
    1. Belirtilen 'wp-fonts-local' style bloğunu siler.
    2. Google Fonts ve diğer harici font linklerini temizler.
    3. Tüm siteye Web Safe Font (sistem fontu) uygular.
    """
    # 1. wp-fonts-local sınıfına sahip style bloğunu direkt sil
    local_fonts = soup.find_all("style", class_="wp-fonts-local")
    for style in local_fonts:
        style.decompose()

    # 2. Harici font linklerini temizle
    for link in soup.find_all("link", href=True):
        if any(x in link["href"] for x in ["fonts.googleapis", "fonts.gstatic"]):
            link.decompose()
    
    # 3. Web Safe Font Stack Uygula (Arial, Helvetica tabanlı en güvenli dizilim)
    # Bu stil, tarayıcının font indirmesini bekletmeden sayfayı anında gösterir.
    safe_font_style = soup.new_tag('style')
    safe_font_style.string = """
        * { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji" !important; 
        }
    """
    if soup.head:
        soup.head.append(safe_font_style)
    return soup

def clean_images(soup):
    """Srcset temizler ve görselleri orijinal (boyut ekisiz) boyutuna yönlendirir."""
    for img in soup.find_all('img'):
        if img.has_attr('srcset'): del img['srcset']
        if img.has_attr('sizes'): del img['sizes']
        if img.has_attr('src'):
            img['src'] = re.sub(r'-\d+x\d+(\.(jpg|jpeg|png|gif|webp|svg))$', r'\1', img['src'], flags=re.IGNORECASE)
    return soup

def clean_wordpress_junk(soup):
    """WP meta, script ve yorum temizliği."""
    junk_metas = ["generator", "wlwmanifest", "EditURI", "shortlink"]
    for meta in soup.find_all("meta"):
        if meta.get("name") in junk_metas or meta.get("property") == "og:generator":
            meta.decompose()
    
    for script in soup.find_all("script"):
        content = script.string if script.string else ""
        src = script.get("src", "")
        if "googleads" in src or "adsbygoogle" in content: continue
        if "_wpemojiSettings" in content or "wp-embed" in src:
            script.decompose()
            
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    return soup

def fix_links_and_tags(soup):
    """Bağlantı dönüşümleri ve etiket temizliği."""
    found_links = []
    for a in soup.find_all('a', href=True):
        original_href = a['href']
        full_url = urljoin(BASE_URL, original_href)
        
        if "/tag/" in original_href:
            a.replace_with(a.get_text())
            continue

        new_href = original_href.replace(OLD_LOCAL_DOMAIN, NEW_DOMAIN)
        if new_href.startswith("http://") and NEW_DOMAIN in new_href:
            new_href = new_href.replace("http://", "https://")
        
        a['href'] = new_href
        clean_url = full_url.split('#')[0].rstrip('/')
        found_links.append(clean_url)
    return soup, found_links

def generate_sitemap(pages):
    now = datetime.now().strftime('%Y-%m-%d')
    sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in sorted(pages):
        sitemap_content.append(f'  <url>\n    <loc>{page}</loc>\n    <lastmod>{now}</lastmod>\n    <priority>0.80</priority>\n  </url>')
    sitemap_content.append('</urlset>')
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_content))

def crawl():
    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        clean_url = current_url.split('#')[0].rstrip('/')
        if not clean_url.startswith("http") or clean_url in visited_urls:
            continue
            
        parsed = urlparse(clean_url)
        # Sadece motorhikayesi.com domainini tara ve tag/feed sayfalarını atla
        if parsed.netloc != urlparse(BASE_URL).netloc or any(x in clean_url for x in ["/tag", "/feed"]):
            continue

        visited_urls.add(clean_url)
        print(f"İşleniyor: {clean_url}")

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(clean_url, headers=headers, timeout=15)
            if response.status_code != 200 or "text/html" not in response.headers.get("Content-Type", ""):
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # --- SIRASIYLA İŞLEMLER ---
            soup = clean_wordpress_junk(soup)
            soup = apply_safe_fonts_and_clean_local(soup) # Local fontlar silindi, Safe font eklendi
            soup = clean_images(soup)
            soup, new_links = fix_links_and_tags(soup)
            # --------------------------

            for link in new_links:
                if link not in visited_urls:
                    urls_to_visit.append(link)

            # Dosya kaydetme
            f_path = parsed.path if parsed.path and parsed.path != "/" else "/index.html"
            if not f_path.endswith(".html"): f_path += ".html"
            local_file = os.path.join(OUTPUT_DIR, f_path.lstrip("/"))
            os.makedirs(os.path.dirname(local_file), exist_ok=True)

            with open(local_file, "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            
            processed_pages.append(clean_url.replace(BASE_URL, "https://" + NEW_DOMAIN))
            time.sleep(0.1)

        except Exception as e:
            print(f"Hata: {clean_url} -> {e}")

if __name__ == "__main__":
    print(f"--- {BASE_URL} Statik Site & Font Temizliği Başladı ---")
    crawl()
    generate_sitemap(processed_pages)
    print(f"\nİşlem tamamlandı. Local fontlar silindi, sistem fontları uygulandı.")
    print(f"Çıktı Klasörü: {OUTPUT_DIR}")
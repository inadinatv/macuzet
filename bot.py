import requests
from bs4 import BeautifulSoup
import datetime
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
url = "https://m.sporx.com/tvdebugun/"

print("Maç sitesine bağlanılıyor...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Bağlantı başarılı! Maçlar toplanıyor...")
    soup = BeautifulSoup(response.content, "html.parser")
    
    html_icerik = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Günün Maçları</title>
        <style>
            body {{ font-family: sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 10px; }}
            h2 {{ text-align: center; color: #00e676; padding-bottom: 10px; border-bottom: 1px solid #333; }}
            .kutu {{ background: #1e1e1e; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid #00e676; }}
            .saat-isim {{ font-size: 15px; line-height: 1.6; font-weight: 500; }}
            .alt-bilgi {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h2>📺 Günün Maç Yayınları</h2>
    """

    # Akıllı Filtre: Sadece HH:MM (Örn: 19:00) saat formatını yakalayacak sistem
    saat_sablonu = re.compile(r'\b\d{2}:\d{2}\b')
    
    mac_sayisi = 0
    kaydedilenler = []

    # 1. Aşama: Maçları tablo içinde arama (Kanal isimleri genelde tabloda ayrılır)
    satirlar = soup.find_all("tr")
    for satir in satirlar:
        hucreler = satir.find_all(["td", "th"])
        if len(hucreler) >= 2:
            # Sütunları (Saat - Maç Adı - Kanal) yan yana birleştir
            metin = " - ".join([h.get_text(strip=True) for h in hucreler if h.get_text(strip=True)])
            # İçinde saat formatı geçiyorsa ve haber başlığı değilse al
            if saat_sablonu.search(metin) and len(metin) < 150 and metin not in kaydedilenler:
                html_icerik += f'<div class="kutu"><div class="saat-isim">{metin}</div></div>'
                kaydedilenler.append(metin)
                mac_sayisi += 1

    # 2. Aşama: Site listeleme mantığı kullanıyorsa (div veya li etiketlerine bakma)
    if mac_sayisi == 0:
        elemanlar = soup.find_all(["li", "div"])
        for eleman in elemanlar:
            metin = eleman.get_text(separator=" - ", strip=True)
            # Eğer doğrudan saat ile başlıyorsa ve maç bilgisine benziyorsa al
            if re.match(r'^\d{2}:\d{2}', metin) and len(metin) < 150 and metin not in kaydedilenler:
                html_icerik += f'<div class="kutu"><div class="saat-isim">{metin}</div></div>'
                kaydedilenler.append(metin)
                mac_sayisi += 1

    if mac_sayisi == 0:
        html_icerik += "<p style='text-align:center;'>Şu an için listelenecek maç bulunamadı veya site yapısı değişti.</p>"

    zaman = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    html_icerik += f"""
        <div class="alt-bilgi">Son Güncelleme: {zaman}</div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as dosya:
        dosya.write(html_icerik)
        
    print(f"İşlem tamam! Toplam {mac_sayisi} maç başarıyla alındı.")

else:
    print("Siteye ulaşılamadı. Lütfen linki kontrol et.")

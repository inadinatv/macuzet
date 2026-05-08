import requests
from bs4 import BeautifulSoup
import datetime

# Sitenin bizi bot sanıp engellememesi için telefon kimliği kullanıyoruz
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
}
url = "https://m.sporx.com/tvdebugun/"

print("Maç sitesine bağlanılıyor...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Bağlantı başarılı! Maçlar toplanıyor...")
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Siyah arka planlı, yeşil detaylı şık HTML tasarımımız
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
            .saat-isim {{ font-size: 16px; font-weight: bold; }}
            .alt-bilgi {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h2>📺 Günün Maç Yayınları</h2>
    """

    # Sitedeki liste elemanlarını çekiyoruz
    satirlar = soup.find_all(["li", "div", "p"]) 
    
    mac_sayisi = 0
    kaydedilenler = []

    for satir in satirlar:
        metin = satir.get_text(strip=True)
        # Metnin içinde saat (:) varsa ve çok kısa/çok uzun değilse maç olarak al
        if ":" in metin and 10 < len(metin) < 150 and metin not in kaydedilenler:
            html_icerik += f"""
            <div class="kutu">
                <div class="saat-isim">{metin}</div>
            </div>
            """
            kaydedilenler.append(metin)
            mac_sayisi += 1
            
    if mac_sayisi == 0:
        html_icerik += "<p style='text-align:center;'>Şu an için listelenecek maç bulunamadı.</p>"

    # Son güncellenme saati
    zaman = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    html_icerik += f"""
        <div class="alt-bilgi">Son Güncelleme: {zaman}</div>
    </body>
    </html>
    """

    # index.html dosyasını oluştur ve içine yaz
    with open("index.html", "w", encoding="utf-8") as dosya:
        dosya.write(html_icerik)
        
    print(f"İşlem tamam! Toplam {mac_sayisi} maç index.html dosyasına yazıldı.")

else:
    print("Siteye ulaşılamadı. Lütfen linki kontrol et.")

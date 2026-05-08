import requests
from bs4 import BeautifulSoup
import datetime

# 1. Siteye normal bir cep telefonu tarayıcısından giriyormuşuz gibi kimlik veriyoruz
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
}
url = "https://m.sporx.com/tvdebugun/"

print("Siteye bağlanılıyor...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Bağlantı başarılı! Veriler çekiliyor...")
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 2. Şık ve mobil uyumlu HTML tasarımımız
    html_icerik = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Günün Maçları - Burhan Usta</title>
        <style>
            body {{ font-family: sans-serif; background-color: #121212; color: #fff; margin: 0; padding: 15px; }}
            h2 {{ text-align: center; color: #00e676; border-bottom: 2px solid #333; padding-bottom: 10px; }}
            .mac-kutu {{ background: #1e1e1e; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-left: 5px solid #00e676; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }}
            .mac-bilgi {{ font-size: 16px; line-height: 1.5; }}
            .tarih {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h2>📺 Günün Maçları</h2>
    """

    # 3. Sitedeki verileri bulma (Sporx listeleri genellikle "li" veya tablo "tr" kullanır)
    # Şimdilik tüm liste elemanlarını çekip, içinde saat olanları filtreliyoruz.
    maclar = soup.find_all("li") 
    
    mac_bulundu = False
    for mac in maclar:
        metin = mac.get_text(strip=True)
        
        # Eğer metnin içinde saat formatı (örn: 19:00) geçiyorsa bunu bir maç olarak kabul et
        if ":" in metin and len(metin) > 10:
            html_icerik += f"""
            <div class="mac-kutu">
                <div class="mac-bilgi">{metin}</div>
            </div>
            """
            mac_bulundu = True
            
    if not mac_bulundu:
        html_icerik += "<p style='text-align:center;'>Şu an için maç verisi bulunamadı.</p>"

    # Alt kısma son güncellenme saatini ekliyoruz
    html_icerik += f"""
        <div class="tarih">Son Güncelleme: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}</div>
    </body>
    </html>
    """

    # 4. Çektiğimiz verileri ve tasarımı index.html dosyasına yazdırıyoruz
    with open("index.html", "w", encoding="utf-8") as dosya:
        dosya.write(html_icerik)
        
    print("İşlem tamam! index.html dosyası başarıyla oluşturuldu.")

else:
    print(f"Hata! Siteye ulaşılamadı. Hata Kodu: {response.status_code}")

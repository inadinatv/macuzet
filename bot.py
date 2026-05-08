import requests
from bs4 import BeautifulSoup
import datetime
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
}
url = "https://m.sporx.com/tvdebugun/"

print("Siteden veriler çekiliyor...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # === HTML ÜST KISIM (Tasarım ve Sekmeler) ===
    html_ust = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Günün Maçları</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }
            .header { background: #fff; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; border-bottom: 1px solid #ddd; }
            
            /* Sekmeler (Tabs) */
            .tabs { display: flex; justify-content: space-around; background: #fff; padding: 10px 0; border-bottom: 2px solid #ddd; position: sticky; top: 0; z-index: 100; }
            .tab-btn { background: none; border: none; font-size: 14px; color: #666; font-weight: bold; cursor: pointer; padding: 5px 10px; }
            .tab-btn.active { color: #333; border-bottom: 3px solid #d9432e; }
            
            /* Maç Listesi Görünümü */
            .kutu { display: flex; align-items: center; background: #fff; margin-bottom: 3px; padding: 12px 10px; }
            .kutu:nth-child(even) { background-color: #fafafa; } /* Çizgili görünüm için */
            
            .saat { color: #d9432e; font-size: 18px; font-weight: normal; min-width: 55px; }
            
            .orta { flex-grow: 1; padding: 0 10px; display: flex; flex-direction: column; }
            .kanal-satiri { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
            .kanal-isim { color: #d9432e; font-weight: bold; font-size: 15px; }
            .kanal-logo { height: 20px; max-width: 50px; object-fit: contain; }
            .mac-isim { color: #444; font-size: 13px; line-height: 1.4; }
            
            .sag { min-width: 45px; text-align: right; }
            .canli { background: #c0392b; color: white; padding: 4px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; }
            
            .gizli { display: none !important; }
            .alt-bilgi { text-align: center; color: #888; font-size: 12px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="header">TV'de Bugün Maç Yayınları</div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="filtrele('Tumu', this)">Tüm gün</button>
            <button class="tab-btn" onclick="filtrele('Futbol', this)">Futbol</button>
            <button class="tab-btn" onclick="filtrele('Basketbol', this)">Basketbol</button>
            <button class="tab-btn" onclick="filtrele('Diger', this)">Diğer</button>
        </div>
        <div id="mac-listesi">
    """
    
    # === HTML ALT KISIM VE JAVASCRIPT (Tıklama İşlemleri) ===
    html_alt = f"""
        </div>
        <div class="alt-bilgi">Son Güncelleme: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}</div>
        
        <script>
            function filtrele(kategori, btn) {{
                // Tıklanan butonun altını kırmızı çizme efekti
                var butonlar = document.getElementsByClassName("tab-btn");
                for (var i = 0; i < butonlar.length; i++) {{
                    butonlar[i].classList.remove("active");
                }}
                btn.classList.add("active");
                
                // Kategorisine göre maçları gizle/göster
                var maclar = document.getElementsByClassName("kutu");
                for (var i = 0; i < maclar.length; i++) {{
                    if (kategori === 'Tumu' || maclar[i].getAttribute("data-kategori") === kategori) {{
                        maclar[i].classList.remove("gizli");
                    }} else {{
                        maclar[i].classList.add("gizli");
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """

    html_orta = ""
    mac_sayisi = 0
    kaydedilenler = []

    # === MAÇ VERİLERİNİ AKILLICA AYRIŞTIRMA ===
    satirlar = soup.find_all(["li", "div", "tr"])
    for satir in satirlar:
        metin = satir.get_text(separator=" | ", strip=True)
        
        # İçinde "19:30" gibi bir saat var mı diye bakıyoruz
        if re.search(r'\b\d{2}:\d{2}\b', metin):
            parcalar = [p.strip() for p in metin.split('|') if p.strip()]
            
            # Saati ayırıyoruz
            saat = next((p for p in parcalar if re.match(r'^\d{2}:\d{2}$', p)), None)
            if not saat: continue
                
            # Canlı yazısı var mı bakıp ayırıyoruz
            is_live = False
            if "Canlı" in parcalar:
                is_live = True
                parcalar.remove("Canlı")
            
            # Saati de metinden çıkarınca geriye kalanlar: Kanal İsmi ve Maç İsmi
            parcalar = [p for p in parcalar if p != saat]
            if len(parcalar) == 0: continue
                
            kanal_ismi = parcalar[0]
            mac_ismi = " - ".join(parcalar[1:]) if len(parcalar) > 1 else ""
            
            # Logo çekme işlemi
            img_tag = satir.find('img')
            logo_url = img_tag.get('src') if img_tag else ""
            if logo_url and not logo_url.startswith("http"):
                if logo_url.startswith("//"): logo_url = "https:" + logo_url
                else: logo_url = "https://m.sporx.com" + logo_url
            
            # Aynı maçı iki kez yazdırmamak için güvenlik önlemi
            kimlik = f"{saat}-{kanal_ismi}-{mac_ismi}"
            if kimlik in kaydedilenler: continue
            kaydedilenler.append(kimlik)
            
            # Kategoriyi Otomatik Bulma
            kategori = "Diger"
            if "Futbol" in mac_ismi or "FUTBOL" in mac_ismi.upper():
                kategori = "Futbol"
            elif "Basketbol" in mac_ismi or "BASKETBOL" in mac_ismi.upper():
                kategori = "Basketbol"
            
            # HTML Kartını Oluşturma
            canli_html = '<div class="canli">Canlı</div>' if is_live else ''
            logo_html = f'<img src="{logo_url}" class="kanal-logo">' if logo_url else ''
            
            html_orta += f"""
            <div class="kutu" data-kategori="{kategori}">
                <div class="saat">{saat}</div>
                <div class="orta">
                    <div class="kanal-satiri">
                        <span class="kanal-isim">{kanal_ismi}</span>
                        {logo_html}
                    </div>
                    <div class="mac-isim">{mac_ismi}</div>
                </div>
                <div class="sag">
                    {canli_html}
                </div>
            </div>
            """
            mac_sayisi += 1

    if mac_sayisi == 0:
        html_orta = "<p style='text-align:center; padding: 20px; color:#666;'>Gösterilecek maç bulunamadı.</p>"

    # === TÜM PARÇALARI BİRLEŞTİR VE DOSYAYA YAZ ===
    with open("index.html", "w", encoding="utf-8") as dosya:
        dosya.write(html_ust + html_orta + html_alt)
        
    print(f"Başarılı! Toplam {mac_sayisi} maç, özel tasarımıyla index.html dosyasına eklendi.")

else:
    print(f"Bağlantı hatası: {response.status_code}")

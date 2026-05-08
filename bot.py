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
    
    # === İNADINA TV ÖZEL TASARIMI ===
    html_ust = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>İnadına TV - Günün Maçları</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
            
            * { box-sizing: border-box; }
            body { font-family: 'Poppins', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; }
            
            /* Üst Başlık - İnadına TV Markası */
            .header { background: linear-gradient(135deg, #1e293b, #0f172a); padding: 20px 15px; text-align: center; border-bottom: 1px solid #334155; }
            .header-title { font-size: 24px; font-weight: 800; color: #0ea5e9; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
            .header-subtitle { font-size: 13px; color: #94a3b8; font-weight: 500; letter-spacing: 0.5px; }
            
            /* Yuvarlak Hatlı Modern Sekmeler */
            .tabs { display: flex; justify-content: center; gap: 8px; background: #0f172a; padding: 15px 10px; position: sticky; top: 0; z-index: 100; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
            .tab-btn { flex: 1; max-width: 90px; background: #1e293b; border: 1px solid #334155; border-radius: 20px; font-size: 13px; color: #94a3b8; font-weight: 600; cursor: pointer; padding: 8px 5px; transition: all 0.3s ease; text-align: center; }
            .tab-btn.active { background: #0ea5e9; color: #fff; border-color: #0ea5e9; box-shadow: 0 0 12px rgba(14, 165, 233, 0.5); }
            
            /* Havada Duran Kart Görünümü */
            #mac-listesi { padding: 15px; }
            .kutu { display: flex; align-items: center; background: #1e293b; margin-bottom: 12px; padding: 15px; border-radius: 16px; border-left: 5px solid #0ea5e9; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
            
            .saat { color: #38bdf8; font-size: 22px; font-weight: 700; min-width: 65px; border-right: 1px solid #334155; margin-right: 12px; }
            
            .orta { flex-grow: 1; display: flex; flex-direction: column; justify-content: center; overflow: hidden; }
            .kanal-satiri { display: flex; align-items: center; gap: 10px; margin-bottom: 5px; }
            .kanal-isim { color: #f1f5f9; font-weight: 600; font-size: 15px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .kanal-logo { height: 22px; max-width: 60px; object-fit: contain; background: #fff; border-radius: 4px; padding: 2px; }
            .mac-isim { color: #94a3b8; font-size: 13px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
            
            .sag { min-width: 50px; text-align: right; margin-left: 10px; }
            
            /* Yanıp Sönen Canlı Etiketi Animasyonu */
            .canli { background: #ef4444; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; display: inline-block; animation: pulse 2s infinite; }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
                70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
                100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
            }
            
            .gizli { display: none !important; }
            .alt-bilgi { text-align: center; color: #64748b; font-size: 12px; margin: 20px 0 40px 0; font-weight: 500; line-height: 1.6; }
            .marka-renk { color: #0ea5e9; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-title">📺 İNADINA TV</div>
            <div class="header-subtitle">Günün Maç Yayınları</div>
        </div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="filtrele('Tumu', this)">Tüm gün</button>
            <button class="tab-btn" onclick="filtrele('Futbol', this)">Futbol</button>
            <button class="tab-btn" onclick="filtrele('Basketbol', this)">Basketbol</button>
            <button class="tab-btn" onclick="filtrele('Diger', this)">Diğer</button>
        </div>
        <div id="mac-listesi">
    """
    
    html_alt_ilk_kisim = """
        </div>
        <div class="alt-bilgi">
            © 2026 <span class="marka-renk">İnadına TV</span> Özel Yayınıdır.<br>
            Son Güncelleme: """
        
    html_alt_ikinci_kisim = """
        </div>
        <script>
            function filtrele(kategori, btn) {
                var butonlar = document.getElementsByClassName("tab-btn");
                for (var i = 0; i < butonlar.length; i++) {
                    butonlar[i].classList.remove("active");
                }
                btn.classList.add("active");
                
                var maclar = document.getElementsByClassName("kutu");
                for (var i = 0; i < maclar.length; i++) {
                    if (kategori === 'Tumu' || maclar[i].getAttribute("data-kategori") === kategori) {
                        maclar[i].classList.remove("gizli");
                    } else {
                        maclar[i].classList.add("gizli");
                    }
                }
            }
        </script>
    </body>
    </html>
    """

    html_orta = ""
    mac_sayisi = 0
    kaydedilenler = []

    satirlar = soup.find_all(["li", "div", "tr"])
    for satir in satirlar:
        if satir.name == "div" and satir.find("div"):
            continue
            
        metin = satir.get_text(separator=" | ", strip=True)
        
        if len(metin) > 150 or "Tüm gün | Futbol" in metin:
            continue
            
        if re.search(r'\b\d{2}:\d{2}\b', metin):
            parcalar = [p.strip() for p in metin.split('|') if p.strip()]
            
            saat = next((p for p in parcalar if re.match(r'^\d{2}:\d{2}$', p)), None)
            if not saat: continue
                
            is_live = False
            if "Canlı" in parcalar:
                is_live = True
                parcalar.remove("Canlı")
            
            parcalar = [p for p in parcalar if p != saat]
            if len(parcalar) == 0: continue
                
            kanal_ismi = parcalar[0]
            mac_ismi = " - ".join(parcalar[1:]) if len(parcalar) > 1 else ""
            
            img_tag = satir.find('img')
            logo_url = img_tag.get('src') if img_tag else ""
            if logo_url and not logo_url.startswith("http"):
                if logo_url.startswith("//"): logo_url = "https:" + logo_url
                else: logo_url = "https://m.sporx.com" + logo_url
            
            kimlik = f"{saat}-{kanal_ismi}-{mac_ismi}"
            if kimlik in kaydedilenler: continue
            kaydedilenler.append(kimlik)
            
            kategori = "Diger"
            if "Futbol" in mac_ismi or "FUTBOL" in mac_ismi.upper():
                kategori = "Futbol"
            elif "Basketbol" in mac_ismi or "BASKETBOL" in mac_ismi.upper():
                kategori = "Basketbol"
            
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
        html_orta = "<div style='text-align:center; padding: 30px; color:#94a3b8;'>Şu an için gösterilecek maç bulunamadı.</div>"

    zaman = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    tam_html = html_ust + html_orta + html_alt_ilk_kisim + zaman + html_alt_ikinci_kisim

    with open("index.html", "w", encoding="utf-8") as dosya:
        dosya.write(tam_html)
        
    print(f"Harika! İnadına TV tasarımıyla toplam {mac_sayisi} maç eklendi.")

else:
    print(f"Bağlantı hatası: {response.status_code}")

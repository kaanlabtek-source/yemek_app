from io import BytesIO
import pandas as pd
import random
import calendar
import datetime
import streamlit as st

# === AY ve YIL ===
yil = 2025
ay = 10  # Ekim
gun_sayisi = calendar.monthrange(yil, ay)[1]

# === MENÜ KOMBİNASYONLARI ===
kombinasyonlar = [
    "Kırmızı Mercimek Çorbası | Sebzeli Bulgur Pilavı | Yoğurt | Mevsim Salata",
    "Kuru Fasulye | Makarna | Yoğurt | Turşu | Mevsim Salata",
    "Kuru Fasulye | Pirinç Pilavı | Turşu | Cacık",
    "Kabak & Biber Dolması | Yoğurt | Mevsim Salata",
    "Fırında Tavuk | Pirinç Pilavı | Cacık | Mevsim Salata",
    "Menemen | Cacık",
    "Somon | Patates Kızartması | Şarap | Peynir | Zeytin",
    "Tavuk Suyu Çorba | Pirinç Pilavı | Cacık",
    "Köfte | Patates | Pirinç Pilavı | Cacık"
]

# === TAKVİM İÇİN GÜN VE MENÜLERİ OLUŞTUR ===
aylik_menu = []
onceki = None
for g in range(1, gun_sayisi + 1):
    while True:
        secim = random.choice(kombinasyonlar)
        if secim != onceki:
            break
    onceki = secim

    tarih = datetime.date(yil, ay, g)
    gun_adi = calendar.day_name[tarih.weekday()]
    gun_adi_tr = {
        'Monday': 'Pazartesi', 'Tuesday': 'Salı', 'Wednesday': 'Çarşamba',
        'Thursday': 'Perşembe', 'Friday': 'Cuma', 'Saturday': 'Cumartesi', 'Sunday': 'Pazar'
    }[gun_adi]

    aylik_menu.append({
        "Gün": g,
        "Gün Adı": gun_adi_tr,
        "Menü": secim
    })

df = pd.DataFrame(aylik_menu)

# === STREAMLIT ARAYÜZÜ ===
st.set_page_config(page_title="Ekim 2025 Yemek Takvimi", layout="wide")

st.title("📅 Ekim 2025 Yemek Takvimi")
st.write(
    "Her güne rastgele, dengeli bir menü atanmıştır.\n"
    "Günlere tıklayarak menü ayrıntılarını görebilir ve tüm listeyi Excel olarak indirebilirsiniz."
)

hafta_basligi = ['Pzt', 'Salı', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
cal = calendar.monthcalendar(yil, ay)

if 'secili_gun' not in st.session_state:
    st.session_state['secili_gun'] = 1  # Varsayılan seçim

# === Takvim Görünümü ===
st.subheader("Takvim")
for hafta in cal:
    cols = st.columns(7)
    for i, gun in enumerate(hafta):
        if gun == 0:
            cols[i].markdown(" ")
        else:
            if cols[i].button(f"{gun}\n{hafta_basligi[i]}", key=f"gun_{gun}"):
                st.session_state['secili_gun'] = gun

# === Seçilen Gün Ayrıntısı ===
secili_gun = st.session_state['secili_gun']
gunluk = df[df["Gün"] == secili_gun].iloc[0]

st.markdown("---")
st.subheader(f"📌 {secili_gun} Ekim 2025 – {gunluk['Gün Adı']}")
st.write(f"**Menü:** {gunluk['Menü']}")

# === Excel İndirme ===
buffer = BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False)
buffer.seek(0)

st.download_button(
    label="📥 Tüm Ekim Ayı Menüsünü Excel Olarak İndir",
    data=buffer,
    file_name="Ekim_2025_Yemek_Takvimi.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

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

# === GÜN VE MENÜ OLUŞTUR ===
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
        'Monday': 'Pazartesi','Tuesday': 'Salı','Wednesday': 'Çarşamba',
        'Thursday': 'Perşembe','Friday': 'Cuma','Saturday': 'Cumartesi','Sunday': 'Pazar'
    }[gun_adi]
    aylik_menu.append({"Gün": g, "Gün Adı": gun_adi_tr, "Menü": secim})

df = pd.DataFrame(aylik_menu)

# === STREAMLIT AYARLARI ===
st.set_page_config(page_title="Ekim 2025 Yemek Takvimi", layout="wide")
st.title("📅 Ekim 2025 Yemek Takvimi")
st.write("Gün üzerine tıkladığınızda o günün menüsü hücrenin altında açılır.")

hafta_basligi = ['Pzt','Salı','Çar','Per','Cum','Cmt','Paz']
cal = calendar.monthcalendar(yil, ay)

if 'secili_gun' not in st.session_state:
    st.session_state['secili_gun'] = None

# === TAKVİM GÖRÜNÜMÜ: Her hücre kendi expander'ına sahip ===
for hafta in cal:
    cols = st.columns(7)
    for i, gun in enumerate(hafta):
        if gun == 0:
            cols[i].markdown(" ")
        else:
            secili = (st.session_state['secili_gun'] == gun)
            # Her hücrede bir expander var, sadece seçilen açık
            with cols[i].expander(f"{gun}\n{hafta_basligi[i]}", expanded=secili):
                if st.button("Menüyü Göster", key=f"buton_{gun}"):
                    st.session_state['secili_gun'] = gun
                if secili:
                    gunluk = df[df["Gün"] == gun].iloc[0]
                    st.write(f"**{gunluk['Gün Adı']} - Menü:**\n{gunluk['Menü']}")

# === TÜM AYI EXCEL OLARAK İNDİRME ===
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

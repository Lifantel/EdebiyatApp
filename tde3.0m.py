import customtkinter as ctk
from tkinter import messagebox
import webbrowser
import json
import os
import urllib.parse
import requests
import logging

# ========================
# Uygulama ayarları
# ========================
CURRENT_VERSION = "3.0"
VERSION_URL = "https://raw.githubusercontent.com/Lifantel/EdebiyatApp/refs/heads/main/version.txt"
RELEASE_PAGE_URL = "https://github.com/Lifantel/EdebiyatApp/releases"

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("📚 Edebiyat Dersi")
root.geometry("750x500")

# ========================
# Fade geçiş fonksiyonu
# ========================
def fade_to(frame_func):
    for widget in main_frame.winfo_children():
        widget.destroy()
    frame_func()

# ========================
# Güncelleme kontrol
# ========================
def get_latest_version():
    try:
        r = requests.get(VERSION_URL, timeout=6)
        if r.status_code == 200:
            return r.text.strip()
    except Exception as e:
        logging.error(f"Versiyon kontrol hatası: {e}")
    return None

def ask_and_offer_update():
    latest = get_latest_version()
    if latest and latest != CURRENT_VERSION:
        answer = messagebox.askyesno(
            "Güncelleme Var",
            f"Yeni sürüm bulundu: {latest}\nŞu anki sürüm: {CURRENT_VERSION}\nGüncellemek ister misiniz?"
        )
        if answer:
            webbrowser.open(RELEASE_PAGE_URL)

# ========================
# Veri
# ========================
unite_links = {
    "9. Sınıf": {
        "1. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=5739&sayfa=12",
        "2. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=5747&sayfa=72",
        "3. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=5749&sayfa=150",
        "4. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=5751&sayfa=212"
    },
    "10. Sınıf": {
        "1. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6036&sayfa=12",
        "2. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6038&sayfa=34",
        "3. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6039&sayfa=74",
        "4. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6040&sayfa=126",
        "5. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6041&sayfa=162",
        "6. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6042&sayfa=198",
        "7. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6043&sayfa=232",
        "8. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6044&sayfa=248",
        "9. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6045&sayfa=268"
    },
    "11. Sınıf": {
        "1. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=322&sayfa=12",
        "2. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=323&sayfa=32",
        "3. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=324&sayfa=68",
        "4. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=325&sayfa=106",
        "5. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=326&sayfa=132",
        "6. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=327&sayfa=154",
        "7. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=328&sayfa=196",
        "8. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=329&sayfa=232",
        "9. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=330&sayfa=248"
    },
    "12. Sınıf": {
        "1. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6046&sayfa=14",
        "2. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6047&sayfa=38",
        "3. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6048&sayfa=74",
        "4. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6049&sayfa=140",
        "5. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6050&sayfa=184",
        "6. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6051&sayfa=216",
        "7. Ünite": "https://ogmmateryal.eba.gov.tr/panel/panel/EKitapUniteOnizle.aspx?Id=6052&sayfa=238"
    }
}

# ========================
# JSON işlemleri
# ========================
def load_json(filename):
    return json.load(open(filename, "r")) if os.path.exists(filename) else []

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

# ========================
# İşlevler
# ========================
def add_to_favorites(class_name, unit, link):
    favs = load_json("favorites.json")
    if not any(f["class"] == class_name and f["unit"] == unit for f in favs):
        favs.append({"class": class_name, "unit": unit, "link": link})
        save_json("favorites.json", favs)
        messagebox.showinfo("Başarılı", f"{class_name} - {unit} favorilere eklendi!")
    else:
        messagebox.showwarning("Uyarı", "Bu ünite zaten favorilerde!")

def remove_from_favorites(class_name, unit):
    favs = [f for f in load_json("favorites.json") if not (f["class"] == class_name and f["unit"] == unit)]
    save_json("favorites.json", favs)
    fade_to(show_favorites)

def save_search(query, platform):
    searches = load_json("searches.json")
    searches.append({"platform": platform, "query": query})
    save_json("searches.json", searches)

def clear_search_history():
    save_json("searches.json", [])
    fade_to(show_search_history)

def open_link(link):
    webbrowser.open(link)

# ========================
# Arama fonksiyonları
# ========================
def google_search(q):
    if q.strip():
        save_search(q, "Google")
        open_link(f"https://www.google.com/search?q={urllib.parse.quote(q)}")

def youtube_search(q):
    if q.strip():
        save_search(q, "YouTube")
        open_link(f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}")

def ask_bing(q):
    if q.strip():
        save_search(q, "Bing")
        open_link(f"https://www.bing.com/search?q={urllib.parse.quote(q)}&showconv=1")

# ========================
# Sekme: Ana Menü
# ========================
def show_main_menu():
    for widget in main_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(main_frame, text="📚 Edebiyat Dersi", font=("Arial", 24, "bold")).pack(pady=20)

    search_entry = ctk.CTkEntry(main_frame, placeholder_text="Aramak için yazın...")
    search_entry.pack(pady=5)

    btn_frame = ctk.CTkFrame(main_frame)
    btn_frame.pack(pady=5)

    ctk.CTkButton(btn_frame, text="Google", command=lambda: google_search(search_entry.get())).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="YouTube", command=lambda: youtube_search(search_entry.get())).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Copilot", command=lambda: ask_bing(search_entry.get())).pack(side="left", padx=5)

    for class_name in unite_links:
        ctk.CTkButton(main_frame, text=class_name, height=40, command=lambda c=class_name: fade_to(lambda: show_units(c))).pack(pady=5)

    ctk.CTkButton(main_frame, text="⭐ Favoriler", command=lambda: fade_to(show_favorites)).pack(pady=5)
    ctk.CTkButton(main_frame, text="📜 Arama Geçmişi", command=lambda: fade_to(show_search_history)).pack(pady=5)

# ========================
# Sekme: Üniteler
# ========================
def show_units(class_name):
    for widget in main_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(main_frame, text=f"{class_name} Üniteleri", font=("Arial", 20, "bold")).pack(pady=20)

    for unit, link in unite_links[class_name].items():
        row = ctk.CTkFrame(main_frame)
        row.pack(pady=5, fill="x")
        ctk.CTkButton(row, text=unit, command=lambda l=link: open_link(l)).pack(side="left", padx=5)
        ctk.CTkButton(row, text="⭐", width=30, command=lambda c=class_name, u=unit, l=link: add_to_favorites(c, u, l)).pack(side="left")

    ctk.CTkButton(main_frame, text="⬅ Geri", command=lambda: fade_to(show_main_menu)).pack(pady=10)

# ========================
# Sekme: Favoriler
# ========================
def show_favorites():
    for widget in main_frame.winfo_children():
        widget.destroy()

    favs = load_json("favorites.json")
    ctk.CTkLabel(main_frame, text="⭐ Favoriler", font=("Arial", 20, "bold")).pack(pady=20)

    if favs:
        for fav in favs:
            row = ctk.CTkFrame(main_frame)
            row.pack(pady=5, fill="x")
            ctk.CTkButton(row, text=f"{fav['class']} - {fav['unit']}", command=lambda l=fav["link"]: open_link(l)).pack(side="left", padx=5)
            ctk.CTkButton(row, text="🗑", width=30, command=lambda c=fav["class"], u=fav["unit"]: remove_from_favorites(c, u)).pack(side="left")
    else:
        ctk.CTkLabel(main_frame, text="Henüz favori eklenmedi.").pack(pady=10)

    ctk.CTkButton(main_frame, text="⬅ Geri", command=lambda: fade_to(show_main_menu)).pack(pady=10)

# ========================
# Sekme: Arama Geçmişi
# ========================
def show_search_history():
    for widget in main_frame.winfo_children():
        widget.destroy()

    searches = load_json("searches.json")
    ctk.CTkLabel(main_frame, text="📜 Arama Geçmişi", font=("Arial", 20, "bold")).pack(pady=20)

    if searches:
        for search in searches:
            row = ctk.CTkFrame(main_frame)
            row.pack(pady=5, fill="x")
            txt = f"{search['platform']}: {search['query']}"
            ctk.CTkButton(row, text=txt, command=lambda q=search['query'], p=search['platform']:
                          youtube_search(q) if p == "YouTube" else google_search(q) if p == "Google" else ask_bing(q)).pack(side="left", padx=5)
    else:
        ctk.CTkLabel(main_frame, text="Henüz arama yapılmadı.").pack(pady=10)

    ctk.CTkButton(main_frame, text="🗑 Temizle", command=clear_search_history).pack(pady=5)
    ctk.CTkButton(main_frame, text="⬅ Geri", command=lambda: fade_to(show_main_menu)).pack(pady=5)

# ========================
# Ana Frame
# ========================
main_frame = ctk.CTkFrame(root)
main_frame.pack(expand=True, fill="both", padx=10, pady=10)

show_main_menu()
root.after(2000, ask_and_offer_update)
root.mainloop()

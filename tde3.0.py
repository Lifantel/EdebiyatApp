import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import json
import os
import urllib.parse
import logging
import requests  # <-- requests eklendi

# Loglama ayarları
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# -------------------
# GÜNCELLEME AYARLARI
# -------------------
CURRENT_VERSION = "3.0"  # Şu anki uygulama sürümün; gerektiğinde bunu arttır
# Kullanıcının verdiği token'lı raw link (senin verdiğin linki buraya yerleştirdim)
VERSION_URL = "https://raw.githubusercontent.com/Lifantel/EdebiyatApp/refs/heads/main/version.txt"
# Release/puanlama sayfası (kullanıcıyı buraya yönlendirir)
RELEASE_PAGE_URL = "https://github.com/Lifantel/EdebiyatApp/releases"

def get_latest_version():
    try:
        r = requests.get(VERSION_URL, timeout=6)
        if r.status_code == 200:
            return r.text.strip()
        else:
            logging.warning(f"Versiyon kontrolü döndü: status_code={r.status_code}")
    except Exception as e:
        logging.error(f"Versiyon kontrol hatası: {e}")
    return None

def ask_and_offer_update():
    latest = get_latest_version()
    if not latest:
        
        logging.info("Versiyon bilgisi alınamadı.")
        return
    if latest != CURRENT_VERSION:
        try:
            answer = messagebox.askyesno("Güncelleme Var",
                                         f"Yeni sürüm bulundu: {latest}\nŞu anki sürüm: {CURRENT_VERSION}\nGüncellemek ister misiniz?")
            if answer:
                # güvenli yol: release sayfasını aç
                webbrowser.open(RELEASE_PAGE_URL)
        except Exception as e:
            logging.error(f"Güncelleme uyarısı gösterilemedi: {e}")

def periodic_check():
    
    ask_and_offer_update()
    # 1 saatte bir tekrar et (3600000 ms). İstersen bu değeri değiştir.
    root.after(3600000, periodic_check)

# -------------------
# ANA PENCERE / UI
# -------------------

# Ana pencere
root = tk.Tk()
root.title("Edebiyat Dersi")
root.geometry("500x400")
root.configure(bg="#f0f0f0")


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

# Favorileri yükle
def load_favorites():
    if os.path.exists("favorites.json"):
        with open("favorites.json", "r") as f:
            return json.load(f)
    return []

# Favorilere ekle
def add_to_favorites(class_name, unit, link):
    favorites = load_favorites()
    if not any(fav["class"] == class_name and fav["unit"] == unit for fav in favorites):
        favorites.append({"class": class_name, "unit": unit, "link": link})
        with open("favorites.json", "w") as f:
            json.dump(favorites, f)
        messagebox.showinfo("Başarılı", f"{class_name} - {unit} favorilere eklendi!")
    else:
        messagebox.showwarning("Uyarı", "Bu ünite zaten favorilerde!")

# Favorilerden kaldır
def remove_from_favorites(class_name, unit):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if not (fav["class"] == class_name and fav["unit"] == unit)]
    with open("favorites.json", "w") as f:
        json.dump(favorites, f)
    messagebox.showinfo("Başarılı", f"{class_name} - {unit} favorilerden kaldırıldı!")
    show_favorites()

# Arama geçmişini yükle
def load_searches():
    if os.path.exists("searches.json"):
        with open("searches.json", "r") as f:
            return json.load(f)
    return []

# Arama kaydet
def save_search(query, platform):
    searches = load_searches()
    searches.append({"platform": platform, "query": query})
    with open("searches.json", "w") as f:
        json.dump(searches, f)

# Arama geçmişini temizle
def clear_search_history():
    with open("searches.json", "w") as f:
        json.dump([], f)
    messagebox.showinfo("Başarılı", "Arama geçmişi temizlendi!")
    show_search_history()

# Link açma fonksiyonu
def open_link(link):
    try:
        webbrowser.open(link)
        logging.info(f"Link açıldı: {link}")
    except Exception as e:
        messagebox.showerror("Hata", f"Link açılamadı: {e}")
        logging.error(f"Link açma hatası: {e}")

# Google arama fonksiyonu
def google_search(query):
    if not query.strip():
        messagebox.showwarning("Uyarı", "Arama terimi girin!")
        return
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    try:
        webbrowser.open(search_url)
        save_search(query, "Google")
        logging.info(f"Google araması: {query}")
    except Exception as e:
        messagebox.showerror("Hata", f"Arama açılamadı: {e}")
        logging.error(f"Google arama hatası: {e}")

# YouTube arama fonksiyonu
def youtube_search(query):
    if not query.strip():
        messagebox.showwarning("Uyarı", "Arama terimi girin!")
        return
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    try:
        webbrowser.open(search_url)
        save_search(query, "YouTube")
        logging.info(f"YouTube araması: {query}")
    except Exception as e:
        messagebox.showerror("Hata", f"Arama açılamadı: {e}")
        logging.error(f"YouTube arama hatası: {e}")

# Bing Chat sorgu fonksiyonu
def ask_bing(query):
    if not query.strip():
        messagebox.showwarning("Uyarı", "Soru girin!")
        return
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.bing.com/search?q={encoded_query}&showconv=1"
    try:
        webbrowser.open(search_url)
        save_search(query, "Bing")
        logging.info(f"Bing Chat sorgusu: {query}, URL: {search_url}")
    except Exception as e:
        messagebox.showerror("Hata", f"Bing sorgusu başarısız: {e}")
        logging.error(f"Bing sorgu hatası: {e}")

# Üniteleri gösteren fonksiyon
def show_units(class_name):
    for widget in root.winfo_children():
        if widget != class_frame:
            widget.destroy()

    tk.Label(root, text=f"{class_name} Üniteleri", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    unit_frame = ttk.Frame(root)
    unit_frame.pack(pady=10)

    if class_name in unite_links:
        for unit, link in unite_links[class_name].items():
            frame = ttk.Frame(unit_frame)
            frame.pack(pady=5, fill="x", padx=10)
            btn_open = ttk.Button(frame, text=unit, width=20, command=lambda l=link: open_link(l))
            btn_open.pack(side="left")
            btn_fav = ttk.Button(frame, text="Favorilere Ekle", width=15, command=lambda c=class_name, u=unit, l=link: add_to_favorites(c, u, l))
            btn_fav.pack(side="left", padx=5)

    nav_frame = ttk.Frame(root)
    nav_frame.pack(pady=10)
    ttk.Button(nav_frame, text="Geri", command=show_main_menu).pack(side="left", padx=5)
    ttk.Button(nav_frame, text="Favoriler", command=show_favorites).pack(side="left", padx=5)
    ttk.Button(nav_frame, text="Arama Geçmişi", command=show_search_history).pack(side="left", padx=5)

# Favorileri gösteren fonksiyon
def show_favorites():
    for widget in root.winfo_children():
        if widget != class_frame:
            widget.destroy()

    tk.Label(root, text="Favori Üniteler", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    unit_frame = ttk.Frame(root)
    unit_frame.pack(pady=10)

    favorites = load_favorites()
    if favorites:
        for fav in favorites:
            frame = ttk.Frame(unit_frame)
            frame.pack(pady=5, fill="x", padx=10)
            btn_open = ttk.Button(frame, text=f"{fav['class']} - {fav['unit']}", width=20, command=lambda l=fav["link"]: open_link(l))
            btn_open.pack(side="left")
            btn_remove = ttk.Button(frame, text="Kaldır", width=10, command=lambda c=fav["class"], u=fav["unit"]: remove_from_favorites(c, u))
            btn_remove.pack(side="left", padx=5)
    else:
        tk.Label(unit_frame, text="Henüz favori eklenmedi.", font=("Arial", 12)).pack(pady=20)

    nav_frame = ttk.Frame(root)
    nav_frame.pack(pady=10)
    ttk.Button(nav_frame, text="Geri", command=show_main_menu).pack(side="left", padx=5)
    ttk.Button(nav_frame, text="Arama Geçmişi", command=show_search_history).pack(side="left", padx=5)

# Arama geçmişini gösteren fonksiyon
def show_search_history():
    for widget in root.winfo_children():
        if widget != class_frame:
            widget.destroy()

    tk.Label(root, text="Arama Geçmişi", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    history_frame = ttk.Frame(root)
    history_frame.pack(pady=10)

    searches = load_searches()
    if searches:
        for search in searches:
            frame = ttk.Frame(history_frame)
            frame.pack(pady=5, fill="x", padx=10)
            btn_search = ttk.Button(frame, text=f"{search['platform']}: {search['query']}", width=30,
                                   command=lambda q=search['query'], p=search['platform']: 
                                   youtube_search(q) if p == "YouTube" else google_search(q) if p == "Google" else ask_bing(q))
            btn_search.pack(side="left")
    else:
        tk.Label(history_frame, text="Henüz arama yapılmadı.", font=("Arial", 12)).pack(pady=20)

    nav_frame = ttk.Frame(root)
    nav_frame.pack(pady=10)
    ttk.Button(nav_frame, text="Geri", command=show_main_menu).pack(side="left", padx=5)
    ttk.Button(nav_frame, text="Favoriler", command=show_favorites).pack(side="left", padx=5)
    ttk.Button(nav_frame, text="Geçmişi Temizle", command=clear_search_history).pack(side="left", padx=5)

# Ana menüyü gösteren fonksiyon
def show_main_menu():
    for widget in root.winfo_children():
        if widget != class_frame:
            widget.destroy()

    tk.Label(root, text="Sınıf Seçimi", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    
    # Arama çubuğu
    search_frame = ttk.Frame(root)
    search_frame.pack(pady=10)
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=5)
    ttk.Button(search_frame, text="Google'da Ara", command=lambda: google_search(search_entry.get())).pack(side="left", padx=3)
    ttk.Button(search_frame, text="YouTube'da Ara", command=lambda: youtube_search(search_entry.get())).pack(side="left", padx=3)
    ttk.Button(search_frame, text="Copilot'a Sor", command=lambda: ask_bing(search_entry.get())).pack(side="left", padx=3)

    nav_frame = ttk.Frame(root)
    nav_frame.pack(pady=10)
    ttk.Button(nav_frame, text="Favoriler", command=show_favorites).pack(side="left", padx=5)
    ttk.Button(nav_frame, text="Arama Geçmişi", command=show_search_history).pack(side="left", padx=5)

# Sınıf çerçevesi
class_frame = ttk.Frame(root)
class_frame.pack(pady=20)

# Sınıf butonları
classes = ["9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf"]
for class_name in classes:
    btn = ttk.Button(class_frame, text=class_name, width=12, command=lambda c=class_name: show_units(c))
    btn.pack(side="left", padx=10)

# Başlangıçta ana menüyü göster
show_main_menu()

# Güncelleme kontrolünü başlat (GUI açıldıktan kısa süre sonra)
root.after(1500, periodic_check)

# Ana döngü
root.mainloop()

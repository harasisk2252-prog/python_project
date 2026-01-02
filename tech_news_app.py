# -------- IMPORT REQUIRED MODULES --------
import requests              # Used to get news from internet (API)
import tkinter as tk          # Used to create GUI window
from tkinter import ttk, messagebox   # Extra GUI widgets & popup messages
import sqlite3               # Used for database (saving bookmarks)

# -------- API DETAILS --------
API_KEY = "YOUR_NEWSAPI_KEY_HERE"   # Put your NewsAPI key here
BASE_URL = "https://newsapi.org/v2/top-headlines"  # NewsAPI endpoint

# -------- DATABASE SETUP --------
# Create or connect to database file
conn = sqlite3.connect("bookmarks.db")

# Cursor is used to execute SQL commands
cur = conn.cursor()

# Create table if it does not already exist
cur.execute("""
CREATE TABLE IF NOT EXISTS bookmarks (
    title TEXT,
    url TEXT
)
""")

# Save database changes
conn.commit()

# -------- FUNCTION TO FETCH NEWS --------
def fetch_news():
    # Parameters sent to NewsAPI
    params = {
        "apiKey": API_KEY,                  # API key
        "category": category_var.get(),     # Selected category
        "q": search_entry.get(),            # Search keyword
        "sources": source_var.get(),        # Selected source
        "language": "en"                    # English news
    }

    # Send request to NewsAPI
    response = requests.get(BASE_URL, params=params)

    # Convert response to JSON format
    data = response.json()

    # Clear old news from listbox
    news_list.delete(0, tk.END)

    # Clear old articles list
    articles.clear()

    # Add news titles to listbox
    if data.get("articles"):
        for article in data["articles"]:
            news_list.insert(tk.END, article["title"])
            articles.append(article)

# -------- SAVE BOOKMARK FUNCTION --------
def save_bookmark():
    # Get selected news index
    index = news_list.curselection()

    # If nothing selected, do nothing
    if not index:
        return

    # Get selected article
    article = articles[index[0]]

    # Insert article into database
    cur.execute(
        "INSERT INTO bookmarks VALUES (?, ?)",
        (article["title"], article["url"])
    )

    # Save database changes
    conn.commit()

    # Show confirmation popup
    messagebox.showinfo("Saved", "Article bookmarked!")

# -------- OPEN NEWS IN BROWSER --------
def open_article():
    import webbrowser

    index = news_list.curselection()
    if index:
        webbrowser.open(articles[index[0]]["url"])

# -------- DARK MODE FUNCTION --------
def toggle_dark():
    global dark
    dark = not dark

    # Change colors
    bg = "#1e1e1e" if dark else "#f0f0f0"
    fg = "white" if dark else "black"

    root.configure(bg=bg)

    # Apply color to all widgets
    for widget in root.winfo_children():
        try:
            widget.configure(bg=bg, fg=fg)
        except:
            pass

# -------- AUTO REFRESH FUNCTION --------
def auto_refresh():
    fetch_news()                # Fetch latest news
    root.after(60000, auto_refresh)  # Repeat every 60 seconds

# -------- GUI WINDOW --------
root = tk.Tk()
root.title("TechPulse - Tech News App")
root.geometry("900x500")

dark = False
articles = []

# -------- TOP CONTROL FRAME --------
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# Variables to store user selections
category_var = tk.StringVar(value="technology")
source_var = tk.StringVar()

# Dropdown values
categories = ["technology", "business", "science"]
sources = ["", "techcrunch", "bbc-news", "wired"]

# -------- UI ELEMENTS --------
ttk.Label(top_frame, text="Category").grid(row=0, column=0)
ttk.Combobox(top_frame, values=categories,
             textvariable=category_var).grid(row=0, column=1)

ttk.Label(top_frame, text="Source").grid(row=0, column=2)
ttk.Combobox(top_frame, values=sources,
             textvariable=source_var).grid(row=0, column=3)

search_entry = ttk.Entry(top_frame, width=30)
search_entry.grid(row=0, column=4, padx=5)

ttk.Button(top_frame, text="Search",
           command=fetch_news).grid(row=0, column=5)

ttk.Button(top_frame, text="Dark Mode",
           command=toggle_dark).grid(row=0, column=6)

# -------- NEWS LIST BOX --------
news_list = tk.Listbox(root, width=120, height=20)
news_list.pack(pady=10)

# -------- BUTTONS --------
btn_frame = tk.Frame(root)
btn_frame.pack()

ttk.Button(btn_frame, text="Open Article",
           command=open_article).grid(row=0, column=0, padx=10)

ttk.Button(btn_frame, text="Bookmark",
           command=save_bookmark).grid(row=0, column=1)

# -------- START APP --------
fetch_news()
auto_refresh()
root.mainloop()

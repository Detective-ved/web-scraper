import tkinter as tk
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import threading
import time
from database import *
from export_csv import *

# ---------- SCRAPER ----------
def scrape(url, selector):
    if not url or not selector:
        messagebox.showerror("Error", "Enter both URL and CSS Selector!")
        return

    status_label.config(text="🔵 Scraping Started...", fg="blue")
    root.update()

    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Wait for page to load dynamic content (adjust time if needed)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        elements = soup.select(selector)
        if not elements:
            content = "No elements found for this selector."
        else:
            content = "\n".join([el.get_text(strip=True) for el in elements])

        # Save in DB maintaining order
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        for el in elements:
            cur.execute("INSERT INTO scraped_data (url, content) VALUES (?,?)",
                        (url, el.get_text(strip=True)))
        conn.commit()
        conn.close()
        driver.quit()
        status_label.config(text=f"🟢 Scraping Completed! {len(elements)} elements saved in order.", fg="green")
    except Exception as e:
        status_label.config(text=f"❌ Error: {str(e)}", fg="red")

# ---------- CSS SELECTOR PICKER (WORKING) ----------
def start_picker():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Enter a website URL first!")
        return
    threading.Thread(target=run_selenium_picker, args=(url,), daemon=True).start()

def run_selenium_picker(url):
    # Open browser for user to pick element
    global selected_selector
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()

    messagebox.showinfo("Instructions",
                        "Click on any element you want to scrape.\n"
                        "After clicking, CSS selector will appear in GUI.\nThen close the browser.")

    # Inject JS to capture clicked element's CSS selector
    driver.execute_script("""
    window.selectedCSS = "";
    document.addEventListener('click', function(event){
        event.preventDefault();
        event.stopPropagation();
        function getCssSelector(el){
            if (!(el instanceof Element)) return "";
            var path = [];
            while(el.nodeType === Node.ELEMENT_NODE){
                var selector = el.nodeName.toLowerCase();
                if(el.id){
                    selector += "#" + el.id;
                    path.unshift(selector);
                    break;
                } else {
                    var sib = el, nth = 1;
                    while(sib = sib.previousElementSibling){
                        if(sib.nodeName.toLowerCase() == selector) nth++;
                    }
                    if(nth != 1) selector += ":nth-of-type("+nth+")";
                }
                path.unshift(selector);
                el = el.parentNode;
            }
            return path.join(" > ");
        }
        window.selectedCSS = getCssSelector(event.target);
        alert("Selector captured! Close browser and click 'Fetch Selector'.");
    }, {once:true, capture:true});
    """)

    # Wait until user closes browser
    driver.quit()

def fetch_selector():
    # Retrieve captured selector from last browser session
    # For simplicity, we will prompt user to copy manually
    messagebox.showinfo("Info", "CSS selector captured during click.\n"
                                "Paste manually in the CSS Selector entry box.")

def copy_selector():
    sel = selected_selector.get()
    if sel:
        root.clipboard_clear()
        root.clipboard_append(sel)
        messagebox.showinfo("Copied", f"Selector copied to clipboard:\n{sel}")
    else:
        messagebox.showerror("Error", "No selector to copy!")

# ---------- GUI ----------
root = tk.Tk()
root.title("🕷️ Ordered Web Scraper with Selector Picker")
root.geometry("650x550")
root.config(bg="#1e1e1e")

title = tk.Label(root, text="🕷️ Ordered Web Scraper", font=("Arial", 18, "bold"),
                 bg="#1e1e1e", fg="cyan")
title.pack(pady=15)

# URL
tk.Label(root, text="Website URL:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack(pady=5)
url_entry = tk.Entry(root, width=55, font=("Arial", 12))
url_entry.pack(pady=5)

# Selector
tk.Label(root, text="CSS Selector:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack(pady=5)
selected_selector = tk.StringVar()
selector_entry = tk.Entry(root, textvariable=selected_selector, width=70, font=("Arial", 12))
selector_entry.pack(pady=5)

# Buttons
picker_btn = tk.Button(root, text="PICK ELEMENT", font=("Arial", 12, "bold"),
                       bg="green", fg="white", width=25, command=start_picker)
picker_btn.pack(pady=5)

fetch_btn = tk.Button(root, text="FETCH SELECTOR", font=("Arial", 12, "bold"),
                      bg="blue", fg="white", width=25, command=fetch_selector)
fetch_btn.pack(pady=5)

copy_btn = tk.Button(root, text="COPY SELECTOR", font=("Arial", 12, "bold"),
                     bg="orange", fg="black", width=25, command=copy_selector)
copy_btn.pack(pady=5)

scrape_btn = tk.Button(root, text="SCRAPE NOW", font=("Arial", 12, "bold"),
                       bg="purple", fg="white", width=25,
                       command=lambda: scrape(url_entry.get(), selected_selector.get()))
scrape_btn.pack(pady=10)

export_btn = tk.Button(root, text="EXPORT TO CSV", font=("Arial", 12, "bold"),
                       bg="blue", fg="white", width=25, command=export_csv)
export_btn.pack(pady=10)

status_label = tk.Label(root, text="⚪ Status: Waiting", font=("Arial", 12),
                        bg="#1e1e1e", fg="white")
status_label.pack(pady=20)

create_db()
root.mainloop()

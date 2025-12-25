# 🕷️ Flexible Web Scraper with Selector Picker

## Overview
This project is a **GUI-based automated web scraper** that allows users to scrape data from any website in the **exact order it appears**. It includes a **CSS Selector Picker** to easily select elements from any page, stores the data in a **SQLite database**, and allows export to **CSV**.

This project is implemented in **Python** using the following technologies:
- **Tkinter** → GUI interface  
- **Selenium** → Dynamic content scraping  
- **BeautifulSoup** → HTML parsing  
- **SQLite** → Database storage  
- **Pandas** → CSV export  

---

## Features

- ✅ GUI-based web scraper for **any website**  
- ✅ Click elements to get **CSS selector automatically**  
- ✅ Handles **dynamic JavaScript-loaded content**  
- ✅ Maintains **data order** exactly as on webpage  
- ✅ Multi-page scraping ready (just loop URLs)  
- ✅ Stores data in **SQLite database**  
- ✅ Export data to **CSV**  
- ✅ Color-coded status updates in GUI  

---

## Project Structure

The project is split into **3 main Python files** for better organization:

| File | Purpose |
|------|---------|
| `gui_scraper.py` | Main GUI interface. Handles user input, selector picking, scraping logic, and status updates. |
| `database.py` | Handles creation and management of SQLite database. |
| `exportcsv.py` | Exports stored database data into a CSV file. |

> All three files work together to create a **modular and maintainable scraper**.

---

## Requirements

There's also a |`requirements.txt`| file which contains all useful packages.
Make sure you have Python 3.8+ installed and the following packages:

``bash
`pip install -r requirements.txt`

Also, you need Chrome browser and ChromeDriver installed and added to your system PATH.

## How to Use

1. Clone the repository or copy the files:
2. gui_scraper.py, database.py, exportcsv.py
    Run GUI: `python gui_scraper.py`  

3. Enter Website URL in the GUI.
4. Pick Element:
    - Click Pick Element → Selenium browser opens
    - Click on any element you want to scrape
    - Close browser → manually paste selector in GUI entry box (or use fetch/copy buttons if implemented)

5. Scrape Data:
    - Click Scrape Now → data will be saved in SQLite database in order.

6. Export CSV:
    - Click Export to CSV → all data will be saved in `scraped_data.csv`.

## License

This project is open for educational and internship purposes. You can freely modify and customize it.

## Author

  - Developed by Raghav Mohan Gupta.
  - GUI-based interactive web scraper for learning, practice, and internship projects.

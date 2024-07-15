import os
import re
import requests
from bs4 import BeautifulSoup
from logger import Logger
import random
import time

class Scraper:
    def __init__(self):
        self.header = "https://www.minneapolisfed.org/beige-book-reports/"
        self.years = list(range(1970, 2024))
        self.months = list(range(1, 13))
        self.regions = {
            "atlanta": "at",
            "boston": "bo",
            "chicago": "ch",
            "cleveland": "cl",
            "dallas": "da",
            "kensas_city": "kc",
            "minneapolis": "mi",
            "new_york": "ny",
            "philadelphia": "ph",
            "richmond": "ri",
            "san_francisco": "sf",
            "st_louis": "sl",
            "national_summary": "su"
        }
        self.logger = Logger("scraper_log")
        self.base_path = "beige_books"

    def ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def scrape_and_save_text(self):
        for year in self.years:
            for month in self.months:
                for name, code in self.regions.items():
                    url = self.header + f"{year}/{year}-{month:02d}-{code}"
                    
                    try:
                        r = requests.get(url)
                        if r.status_code == 200:
                            soup = BeautifulSoup(r.text,features="html5lib")
                            div = soup.find("div", class_="col-sm-12 col-lg-8 offset-lg-1")
                            raw = re.sub(r"\s*\n\s*", "\n", div.text).strip()
                            raw = raw.split("\n", 3)[3] if len(raw.split("\n", 3))>3 else raw
                            
                            file_path = os.path.join(self.base_path, str(year), f"{month:02d}", f"{name}.txt")
                            self.ensure_dir(file_path)
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(raw)
                            self.logger.info(f"Data scraped for {url.split('/')[-1]}.")
                        else:
                            self.logger.info(f"No data for {url.split('/')[-1]}")
                    except Exception as e:
                        self.logger.error(f"Error fetching {url.split('/')[-1]}: {e}")
                    
                    time.sleep(random.uniform(0.5,1.5))

scraper = Scraper()
scraper.scrape_and_save_text()
"""
常用成语爬虫，共计50页，每页60个成语，共计3000个成语
"""

import sqlite3

import requests
from bs4 import BeautifulSoup


class IdiomScraper:
    def __init__(self, db_name='idiom_com.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect_db(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS idiom_common (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idiom TEXT NOT NULL
        )
        ''')

    def insert_idiom(self, idiom):
        self.cursor.execute('INSERT INTO idiom_common (idiom) VALUES (?)', (idiom,))

        self.connection.commit()

    def close_db(self):
        if self.connection:
            self.connection.close()

    @staticmethod
    def extract_html(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Content-Type": "application/json, text/plain, */*",
            "Accept": "application/json, text/plain, */*"
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.encoding = "UTF-8"
            soup = BeautifulSoup(response.text, 'html.parser')
            code_blocks = soup.find_all("div", class_="section")

            idioms = []
            for code_block in code_blocks:
                try:
                    h3_span = code_block.find('h3')
                    idiom = h3_span.text.strip() if h3_span else ''
                    idioms.append(idiom) if idiom else None
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue

            return idioms

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def scrape_and_store(self, start_page, end_page, url_template):
        self.connect_db()
        self.create_table()

        for i in range(start_page, end_page + 1):
            url = url_template.format(i)
            idiom_list = self.extract_html(url)
            print(f"Processing page {i}, found {len(idiom_list)} idioms")

            if idiom_list:
                for idiom in idiom_list:
                    self.insert_idiom(idiom)

        self.close_db()


if __name__ == '__main__':
    scraper = IdiomScraper()
    scraper.scrape_and_store(1, 50, "https://www.hanyuguoxue.com/chengyu/redu-changyong-p{}")
    # print(scraper.extract_html("https://www.hanyuguoxue.com/chengyu/redu-changyong-p1"))

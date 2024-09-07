"""
表情猜成语爬虫
"""

import sqlite3

import requests
from bs4 import BeautifulSoup


class IdiomEmojiScraper:
    def __init__(self, db_name='emoji.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect_db(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS idioms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idiom TEXT NOT NULL,
            emojis TEXT NOT NULL
        )
        ''')

    def insert_idiom(self, idiom, emojis):
        self.cursor.execute('INSERT INTO idioms (idiom, emojis) VALUES (?, ?)', (idiom, emojis))
        self.connection.commit()

    def close_db(self):
        if self.connection:
            self.connection.close()

    def extract_html(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Content-Type": "application/json, text/plain, */*",
            "Accept": "application/json, text/plain, */*"
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.encoding = "UTF-8"
            soup = BeautifulSoup(response.text, 'html.parser')
            code_blocks = soup.find_all("code", class_="html hljs xml")

            idiom_emoji_dict = {}
            for code_block in code_blocks:
                try:
                    emoji_span = code_block.find('span')
                    emojis = emoji_span.text.strip() if emoji_span else ''
                    emojis, idiom = emojis.split(' ')
                    idiom_emoji_dict[idiom] = emojis
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue

            return idiom_emoji_dict

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def scrape_and_store(self, start_page, end_page, url_template):
        self.connect_db()
        self.create_table()

        for i in range(start_page, end_page + 1):
            url = url_template.format(i)
            if i == 1:
                url = "https://www.lovelyemoji.com/emojicaichengyu/index.html"

            idiom_emoji_dict = self.extract_html(url)
            print(f"Processing page {i}, found {len(idiom_emoji_dict)} idioms")

            if idiom_emoji_dict:
                for idiom, emojis in idiom_emoji_dict.items():
                    self.insert_idiom(idiom, emojis)

        self.close_db()


if __name__ == '__main__':
    scraper = IdiomEmojiScraper()
    scraper.scrape_and_store(1, 138, "https://www.lovelyemoji.com/emojicaichengyu/index_{}.html")

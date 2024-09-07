import csv
import threading
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from loguru import logger

from fetch_idiom import fetch_idiom_info
from pinyin import pinyin_list

# 设置日志文件
logger.add("logfile.log", rotation="1 MB")  # 每1MB轮换一个日志文件
# logger.add(sys.stdout, level="INFO")  # 输出到控制台，日志级别为INFO

# 创建一个锁
lock = threading.Lock()
url_links_lst = []
error_links = []


def fetch_links(pinyin):
    url = 'https://www.hanyuguoxue.com/chengyu/pinyin-' + pinyin
    url_raw = 'https://www.hanyuguoxue.com/'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Content-Type": "application/json, text/plain, */*",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*",
        "Connection": "close"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return
        response.encoding = "UTF-8"
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取页数
        pages = [int(li.get('data-page', 1)) for li in soup.find_all('li', class_='page-item') if li.get('data-page')]
        max_page = max(pages) if pages else 1

        # 获取所有的词语链接
        sections = soup.find_all('div', class_='section')
        links = [url_raw + section.find('a', class_='more')['href'] for section in sections]

        if max_page > 1:
            for i in range(2, max_page + 1):
                url_page = url + f'-p{i}'
                response = requests.get(url_page, headers=headers, timeout=30)
                response.encoding = "UTF-8"
                soup = BeautifulSoup(response.text, 'html.parser')
                sections = soup.find_all('div', class_='section')
                links += [url_raw + section.find('a', class_='more')['href'] for section in sections]
        with lock:
            url_links_lst.extend(links)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        logger.error(f"Error URL: {url}")
        with lock:
            error_links.append(url)


def write_to_csv():
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames=["derivation", "example", "explanation", "pinyin", "word", "abbreviation",
                                            "pinyin_r", "first", "last"])
        writer.writeheader()
        for result in results:
            writer.writerow(result)


def fetch_and_store(url):
    try:
        result = fetch_idiom_info(url)
        if result:  # 确保 result 不为空
            with lock:
                results.append(result)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        logger.error(f"Error URL: {url}")


# 使用线程池
with ThreadPoolExecutor(max_workers=15) as executor:  # 设置最大线程数量为15
    executor.map(fetch_links, pinyin_list)

logger.info(f"Total links: {len(url_links_lst)}")
logger.info(f"Error links: {len(error_links)}")
logger.info(f"Error links: {error_links}")

# CSV文件路径
csv_file_path = '../data.csv'
results = []

# 使用线程池来处理链接
with ThreadPoolExecutor(max_workers=15) as executor:  # 设置最大线程数量为15
    executor.map(fetch_and_store, url_links_lst)

# 写入结果到 CSV 文件
write_to_csv()

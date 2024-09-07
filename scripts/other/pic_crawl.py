"""
看图猜成语爬虫
"""

import os.path

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Content-Type": "application/json, text/plain, */*",
    "Accept": "application/json, text/plain, */*",
    'Connection': 'close'
}


def fetch_idiom_info(url):
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, 'html.parser')

    box_div = soup.find('div', class_='boxHui')
    # 找到 <img> 标签
    img_tag = box_div.find('img')

    # 提取 src 和 alt 属性
    img_url = img_tag['src']
    img_alt = img_tag['alt']

    img_url = 'http://www.qqc.net' + img_url
    img_alt = img_alt.split(':')[-1].split('(')[0]

    os.makedirs('images', exist_ok=True)

    res = requests.get(img_url)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch image from {img_url}")

    file_name = f'images/{img_alt}'

    while os.path.exists(f'{file_name}.jpg'):
        file_name += '1'

    with open(f'{file_name}.jpg', 'wb') as f:
        f.write(res.content)

    return file_name + '.jpg'


def fetch_image(i):
    try:
        url = base_url.format(i)
        img_path = fetch_idiom_info(url)
        return img_path
    except Exception as e:
        print(f'Error occurred: {i} {e}')
        failed_pages.append(i)  # 将失败的页码添加到列表中
        return None


if __name__ == '__main__':
    import concurrent.futures

    base_url = 'http://www.qqc.net/ktccy/{}.html'
    failed_pages = []  # 用于存储失败的页码

    error_lst = list(range(1, 458))
    # error_lst = []

    # 使用线程池调度
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(fetch_image, i): i for i in error_lst}

        for future in concurrent.futures.as_completed(futures):
            page_number = futures[future]
            try:
                result = future.result()
                if result is not None:
                    # print(f'Successfully fetched image for page {page_number}: {result}')
                    pass
            except Exception as e:
                print(f'Error occurred while processing page {page_number}: {e}')

    # 返回失败的页码列表
    print("Failed pages:", failed_pages)

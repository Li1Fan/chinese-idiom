import requests
from bs4 import BeautifulSoup

from pinyin import replace_dict

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'close',
    'Host': 'www.hanyuguoxue.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Sec-CH-UA': '"Google Chrome";v="127", "Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
}


# 获取成语信息
def fetch_idiom_info(url):
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取成语
    word = soup.find('h1').text

    # 获取拼音
    pinyin_div = soup.find('div', class_='pinyin')
    pinyin_list = [span.get_text() for span in pinyin_div.find_all('span')]
    pinyin_full = ' '.join(pinyin_list)

    pinyin_r = pinyin_full
    for k, v in replace_dict.items():
        pinyin_r = pinyin_r.replace(k, v)
    pinyin_r_lst = pinyin_r.split()

    first = pinyin_r_lst[0]
    last = pinyin_r_lst[-1]
    abbreviation = [i[0] for i in pinyin_r_lst]

    # 初始化结果字典
    result = {
        'derivation': '',
        'example': '',
        'explanation': '',
        'pinyin': pinyin_full.strip(),
        'word': word.strip(),
        'abbreviation': ''.join(abbreviation).strip(),
        'pinyin_r': pinyin_r.strip(),
        'first': first.strip(),
        'last': last.strip()
    }

    # 查找 id 为 "explain" 的 div
    explain_div = soup.find('div', id='explain')

    # 判断是否找到该 div
    if explain_div:
        # 提取所有的 p 标签
        paragraphs = explain_div.find_all('p')

        # 遍历每个 p 标签，判断是否包含“出处”和“例子”
        for p in paragraphs:
            if '出处' in p.get_text():
                result['derivation'] = p.get_text(strip=True).replace('出处：', '').strip()
            elif '例子' in p.get_text():
                result['example'] = p.get_text(strip=True).replace('例子：', '').strip()

        # 解释
        explain_p = soup.find('p', class_='explain primary')
        explain = explain_p.get_text().replace('\n', '').replace(' ', '').replace("复制", "")
        result['explanation'] = explain.strip()
    else:
        # 根据 class="explain" 定位到对应的 p 标签
        explain_paragraph = soup.find('p', class_='explain')
        # 判断是否找到该 p 标签
        if explain_paragraph:
            # 提取 cite 标签
            cite_tag = explain_paragraph.find('cite')

            # 提取解释内容，只保留 cite 标签之前的部分
            if cite_tag:
                explanation_text = explain_paragraph.get_text(strip=True).split(cite_tag.get_text(strip=True))[
                    0].strip()
            else:
                explanation_text = explain_paragraph.get_text(strip=True)

            # 提取 cite 标签中的值
            cite_text = cite_tag.get_text(strip=True) if cite_tag else ""

            # 将解释内容和 cite 标签中的值存入结果字典
            result['explanation'] = explanation_text.strip()
            result['derivation'] = cite_text.strip()

    if not result['explanation']:
        raise ValueError("No explanation found.")
    return result


if __name__ == '__main__':
    url = 'https://www.hanyuguoxue.com//chengyu/ci-78f2d1464'
    chengyu_info = fetch_idiom_info(url)
    print(chengyu_info)

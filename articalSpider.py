import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from uploadToPostgres import uploadlink

def get_chrome_driver():
    """
    获取适用于当前操作系统的 ChromeDriver
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    # Linux下如果没有DISPLAY环境变量，强制无头
    if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
        options.add_argument('--headless')
    # chromedriver 路径可自定义
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        print('ChromeDriver 启动失败，请检查 chromedriver 是否安装并在 PATH 中，或指定 executable_path。')
        raise e

def crawl_juejin_hot_articles(sleep_time=1):
    """
    爬取掘金热榜文章正文，返回包含时间、内容、链接的JSON列表
    :param sleep_time: 页面加载等待时间（秒）
    :return: List[dict]
    """
    driver = get_chrome_driver()
    driver.get('https://juejin.cn/hot/articles')
    time.sleep(sleep_time)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hot_list_div = soup.find('div', class_='hot-list')
    links = []
    if hot_list_div:
        baseURL = 'https://juejin.cn'
        all_a = hot_list_div.find_all('a')
        for a in all_a:
            if a.has_attr('href'):
                link = baseURL + a['href']
                if '/user/' not in link:
                    links.append(link)
    else:
        print('未找到 hot-list 区块')
        driver.quit()
        return []
    driver.quit()

    article_texts = []
    for link in links:
        try:
            driver = get_chrome_driver()
            driver.get(link)
            time.sleep(sleep_time)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            article_div = soup.find('div', id='article-root', itemprop='articleBody', class_='main')
            if article_div:
                text = article_div.get_text(separator='\n', strip=True)
                now = datetime.now().isoformat(sep=' ', timespec='seconds')
                article_texts.append({'time': now, 'content': text, 'link': link})
            else:
                print(f'未找到文章内容: {link}')
            driver.quit()
        except TimeoutException:
            print(f'加载超时: {link}')
        except Exception as e:
            print(f'处理出错: {link}, 错误: {e}')
    return article_texts

if __name__ == '__main__':
    result = crawl_juejin_hot_articles()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # 上传到数据库
    for item in result:
        uploadlink(item['link'], item['time'], content=item['content'])


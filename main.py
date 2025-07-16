import schedule
import time
from articalSpider import crawl_juejin_hot_articles


def job():
    print('开始定时爬取掘金热榜...')
    crawl_juejin_hot_articles()
    print('爬取完成')

schedule.every(3).hours.do(job)

print('定时任务已启动，每3小时自动运行爬虫...')
while True:
    schedule.run_pending()
    time.sleep(30) 
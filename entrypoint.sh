#!/bin/bash
# 写入定时任务，每天凌晨5点执行爬虫
echo "0 5 * * * cd /app && python articalSpider.py >> /app/cron.log 2>&1" > /etc/cron.d/spider-cron
chmod 0644 /etc/cron.d/spider-cron
crontab /etc/cron.d/spider-cron

# 启动cron服务并保持容器前台运行
cron && tail -f /app/cron.log 
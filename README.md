# Rare-Earth-Gold-Mining-Spider

## 项目简介
本项目是一个基于 Selenium 和 BeautifulSoup 的爬虫，自动抓取掘金热榜文章内容，并将结果上传到 Postgres 数据库。项目已容器化，支持一键 Docker 部署。

## 主要功能
- 自动爬取掘金热榜文章正文、链接和时间
- 解析页面内容，结构化保存
- 结果上传到 Postgres 数据库
- 支持 Docker 一键部署

## 依赖环境
- Python 3.10 及以上
- Google Chrome 浏览器
- chromedriver
- 主要 Python 库：
  - selenium
  - beautifulsoup4
  - psycopg2（如需上传到 Postgres）

## Docker 使用方法

### 1. 构建镜像
```bash
docker build -t rare-earth-gold-mining-spider .
```

### 2. 运行容器
```bash
docker run --rm -it rare-earth-gold-mining-spider
```
> 如需自定义数据库连接等参数，可通过修改 `uploadToPostgres.py` 或传递环境变量。

### 3. Dockerfile 说明
- 基于官方 python:3.10 镜像
- 自动安装 Chrome 浏览器和 chromedriver
- 安装项目依赖
- 入口为 `/entrypoint.sh`，可根据需要修改

## 主要文件说明
- `articalSpider.py`：主爬虫脚本，负责抓取和解析掘金热榜文章
- `uploadToPostgres.py`：将爬取结果上传到 Postgres 数据库
- `requirements.txt`：Python 依赖列表
- `Dockerfile`：项目容器化配置
- `entrypoint.sh`：容器启动脚本

## 常见问题与注意事项
- **chromedriver 版本需与 Chrome 浏览器匹配**，Dockerfile 已自动处理
- 如遇网络拉取镜像慢，可配置 Docker 镜像加速器
- 运行时如遇 selenium 报错，建议检查 Chrome、chromedriver 是否正确安装
- 如需定时运行，可结合 crontab 或定时任务工具

## 联系与反馈
如有问题或建议，欢迎 issue 或 PR！ 
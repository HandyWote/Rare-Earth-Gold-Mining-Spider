FROM python:3.10

USER root
WORKDIR /app

COPY . /app
COPY entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh
RUN ls -l /app/entrypoint.sh || echo "entrypoint.sh not found!"

# 安装依赖
RUN apt-get update && \
    apt-get install -y wget gnupg unzip

# 安装指定版本 Chrome（126.0.6478.126）
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_126.0.6478.126-1_amd64.deb && \
    apt-get install -y ./google-chrome-stable_126.0.6478.126-1_amd64.deb && \
    rm google-chrome-stable_126.0.6478.126-1_amd64.deb

# 使用华为云镜像下载 chromedriver（115.0.5763.0）并正确移动到 /usr/bin
RUN wget -O /tmp/chromedriver.zip "https://repo.huaweicloud.com/chromedriver/115.0.5763.0/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
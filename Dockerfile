FROM python:latest

USER root
WORKDIR /app

COPY . /app

# 安装 Chrome 浏览器和 chromedriver
RUN apt-get update && \
    apt-get install -y wget gnupg unzip && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1) && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.0/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "/entrypoint.sh"]
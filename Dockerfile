FROM selenium/standalone-chrome:latest

USER root
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "/entrypoint.sh"]
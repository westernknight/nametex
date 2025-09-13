FROM python:3.9-alpine

# 安装系统依赖
RUN apk add --no-cache \
    cairo-dev \
    pango-dev \
    glib-dev \
    gobject-introspection-dev \
    gcc \
    musl-dev \
    pkgconfig \
    cairo \
    pango

WORKDIR /app

# 先复制依赖文件
COPY requirements.txt /app/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制字体文件
COPY ChillRoundFRegular.ttf /app/
COPY NotoColorEmoji.ttf /app/

# 最后复制应用代码
COPY app.py /app/

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
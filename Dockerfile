FROM python:3.9-alpine

# 安装系统依赖
RUN apk add --no-cache \
    cairo-dev \
    pango-dev \
    glib-dev \
    gobject-introspection-dev \
    gcc \
    musl-dev \
    pkgconfig

WORKDIR /app

# 复制文件
COPY ChillRoundFRegular.ttf /app/
COPY NotoColorEmoji.ttf /app/
COPY app.py /app/

# 安装Python依赖
RUN pip install --no-cache-dir flask pycairo PyGObject

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
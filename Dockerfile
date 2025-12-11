FROM surnet/alpine-wkhtmltopdf:3.20.2-0.12.6-full

# Instalar Python y Flask
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --break-system-packages flask

WORKDIR /app
COPY app.py .

EXPOSE 8080

# Sobrescribimos el ENTRYPOINT de la imagen base
ENTRYPOINT ["python3", "app.py"]

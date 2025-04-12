# Dockerfile - Backend (Flask API)

FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do backend para o container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da API
EXPOSE 5000

# Comando para rodar a API
CMD ["python", "app.py"]

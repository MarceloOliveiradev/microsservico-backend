# Backend – Loja de Imãs 🧲

Este projeto faz parte do conteúdo requerido para entrega do MVP e conclusão da 2ª sprint do curso da PUC-Rio de Engenharia de Software.

## Cenário Atendido: 1.1

## Objetivo

Desenvolver uma API REST para gerenciamento de um estoque de imãs de neodímio, incluindo uma funcionalidade de cálculo de frete baseado em CEP, com integração a uma API externa (ViaCEP).

## Funcionalidades

- CRUD completo de imãs (GET, POST, PUT, DELETE)
- Pesquisa por medida do imã
- Cálculo de frete via CEP utilizando a API pública do [ViaCEP](https://viacep.com.br/)
- Integração com frontend SPA via fetch (JavaScript)

## Principais Rotas

| Método | Rota                    | Descrição                         |
| ------ | ----------------------- | --------------------------------- |
| GET    | `/imas/`                | Retorna todos os imãs cadastrados |
| GET    | `/imas/search/<medida>` | Busca um imã pela medida          |
| POST   | `/imas/`                | Adiciona um novo imã              |
| PUT    | `/imas/<id>`            | Atualiza os dados de um imã       |
| DELETE | `/imas/<id>`            | Remove um imã pelo ID             |
| GET    | `/frete/<cep>`          | Calcula o valor do frete via CEP  |

---

## API Externa Utilizada

- **ViaCEP**
  - Site: [https://viacep.com.br](https://viacep.com.br)
  - Gratuita e sem necessidade de autenticação.
  - Utilizada internamente na rota `/frete/<cep>` para obter informações do endereço a partir do CEP informado e calcular um frete fictício por estado (UF).

---

## Como executar

### Modo manual (sem Docker)

1. Clone o repositório:

```bash
git clone <url-do-repositório>
cd microsservico-backend
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o servidor:

```bash
python app.py
```

### ⚠️ Importante

Para que o backend funcione corretamente no Docker e aceite conexões externas, o arquivo `app.py` deve conter:

```python
app.run(debug=True, host='0.0.0.0')
```

> Isso garante que a API execute não apenas no `localhost`, mas em todas as interfaces de rede do container.

Acesse via navegador:

```
http://localhost:5000/
```

---

## Executando com o Docker

1. Certifique-se de que o Docker está instalado e rodando

2. Execute o backend como container isolado:

```bash
docker build -t mvp2-backend ./microsservico-backend

docker run -d -p 5000:5000 --name backend-container mvp2-backend
```

3. Para parar e remover o container:

```bash
docker stop backend-container

docker rm backend-container
```

Acesse via navegador:

```
http://localhost:5000/
```

---

## Como executar frontend + backend juntos com Docker Compose

1. Estando na raiz do projeto (onde está `docker-compose.yml`), execute:

```bash
docker compose up --build
```

2. Isso irá:

   - Buildar e subir o serviço `backend` na porta `5000`
   - Buildar e subir o serviço `frontend` na porta `8080`

3. Acesse no navegador:
   - Backend/Swagger: `http://localhost:5000`
   - Frontend SPA: `http://localhost:8080`

### ⚠️ Importante

Ao fazer o download do repositório, o arquivo "docker-compose.yml" se encontra dentro da pasta "microsservico-backend", antes de executar o comando, certifique-se de extrair o arquivo para a raiz do projeto (sua pasta que contém as duas componentes) para o docker-compose funcionar corretamente.

---

## Arquitetura da Aplicação

A aplicação segue uma arquitetura baseada em microsserviços, com separação entre frontend, backend e API externa.

## Fluxograma

<div align="center">
  <img src="https://github.com/MarceloOliveiradev/frontend-spa/blob/main/img/fluxograma%20-%20arquitetura%20MVP2.png?raw=true" width="500px" />
</div>

# Calculadora de Área de Triângulo
Aplicação simples cliente-servidor para calcular a área de um triângulo.


## Como rodar o projeto

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/iansergio/sid.git
cd sid/client-server
```

---

### 2. Crie e ative o ambiente virtual (venv)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install fastapi uvicorn requests
```

---

### 4. Rode o servidor (FastAPI)

```bash
uvicorn server:app --reload
```

O servidor estará disponível em:
http://127.0.0.1:8000

Documentação automática:
http://127.0.0.1:8000/docs

---

### 5. Rode o cliente (Tkinter)

Em outro terminal (com a venv ativada):

```bash
python client.py
```

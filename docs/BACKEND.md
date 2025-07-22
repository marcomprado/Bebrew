# 🚀 Backend Bebrew - Documentação

## 📋 Visão Geral

O backend do Bebrew é uma API RESTful construída com **FastAPI** que integra **OpenAI** para funcionalidades de IA e **Firebase** para autenticação e armazenamento de dados. O sistema oferece funcionalidades inteligentes para brassagem artesanal.

## 🏗️ Arquitetura

```
backend/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações da aplicação
├── services/
│   ├── __init__.py
│   ├── ai_service.py        # Serviço de IA (OpenAI)
│   └── firebase_service.py  # Serviço do Firebase
├── api/
│   └── main.py              # API principal (FastAPI)
└── __init__.py
```

## 🔧 Configuração

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações da OpenAI
OPENAI_API_KEY=sua_chave_api_openai_aqui
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Configurações do Firebase
FIREBASE_PROJECT_ID=seu_projeto_firebase
FIREBASE_PRIVATE_KEY_ID=sua_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nsua_private_key_aqui\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@seu-projeto.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=sua_client_id
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40seu-projeto.iam.gserviceaccount.com

# Configurações do Sistema
DEBUG=True
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
```

### 2. Instalação de Dependências

```bash
pip install -r requirements.txt
```

### 3. Configuração do Firebase

1. Crie um projeto no [Firebase Console](https://console.firebase.google.com/)
2. Ative o **Authentication** e **Firestore Database**
3. Crie uma conta de serviço:
   - Vá para Configurações do Projeto > Contas de Serviço
   - Clique em "Gerar nova chave privada"
   - Baixe o arquivo JSON e use os valores no `.env`

### 4. Configuração da OpenAI

1. Crie uma conta na [OpenAI](https://platform.openai.com/)
2. Gere uma API key
3. Adicione a chave no arquivo `.env`

## 🚀 Executando a API

### Método 1: Script dedicado
```bash
python run_api.py
```

### Método 2: Uvicorn direto
```bash
uvicorn backend.api.main:app --reload --host localhost --port 8000
```

### Método 3: Módulo Python
```bash
python -m backend.api.main
```

## 📚 Documentação da API

Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticação

A API usa **Firebase Authentication** com tokens JWT. Para autenticar:

1. **Registrar usuário**:
```bash
POST /auth/register
{
    "email": "usuario@exemplo.com",
    "password": "senha123",
    "display_name": "Nome do Usuário"
}
```

2. **Obter token** (via Firebase SDK no frontend)
3. **Usar token** no header Authorization:
```
Authorization: Bearer <seu_token_jwt>
```

## 🧠 Funcionalidades de IA

### 1. Análise de Receitas
```bash
POST /ai/analyze-recipe
{
    "recipe_data": {
        "name": "IPA Artesanal",
        "ingredients": [...],
        "steps": [...]
    }
}
```

### 2. Otimização de Receitas
```bash
POST /ai/optimize-recipe
{
    "recipe_data": {...},
    "target_style": "IPA"
}
```

### 3. Previsão de Fermentação
```bash
POST /ai/predict-fermentation
{
    "recipe_data": {...},
    "initial_gravity": 1.050,
    "temperature": 20.0
}
```

### 4. Sugestões de Melhoria
```bash
POST /ai/suggest-improvements
{
    "production_data": {
        "temperatures": [...],
        "times": [...],
        "results": {...}
    }
}
```

## 📊 Endpoints Principais

### Autenticação
- `POST /auth/register` - Registrar usuário
- `POST /auth/verify` - Verificar token

### Receitas
- `GET /recipes` - Listar receitas
- `POST /recipes` - Criar receita
- `GET /recipes/{id}` - Obter receita
- `PUT /recipes/{id}` - Atualizar receita
- `DELETE /recipes/{id}` - Deletar receita

### Produção
- `GET /productions` - Listar produções
- `POST /productions` - Criar produção

### Ingredientes
- `GET /ingredients` - Listar ingredientes
- `POST /ingredients` - Adicionar ingrediente

### IA
- `POST /ai/analyze-recipe` - Analisar receita
- `POST /ai/optimize-recipe` - Otimizar receita
- `POST /ai/predict-fermentation` - Prever fermentação
- `POST /ai/suggest-improvements` - Sugerir melhorias

## 🔍 Exemplos de Uso

### Criar uma Receita
```python
import requests

# Autenticar
headers = {"Authorization": "Bearer seu_token_aqui"}

# Criar receita
recipe_data = {
    "name": "IPA Artesanal",
    "style": "India Pale Ale",
    "ingredients": [
        {"name": "Malte Pilsen", "amount": 5.0, "unit": "kg"},
        {"name": "Lúpulo Cascade", "amount": 50, "unit": "g"}
    ],
    "steps": [
        {"step": 1, "description": "Mostura a 65°C por 60 min"},
        {"step": 2, "description": "Fervura com lúpulo por 60 min"}
    ]
}

response = requests.post(
    "http://localhost:8000/recipes",
    json=recipe_data,
    headers=headers
)
```

### Analisar Receita com IA
```python
response = requests.post(
    "http://localhost:8000/ai/analyze-recipe",
    json={"recipe_data": recipe_data},
    headers=headers
)

analysis = response.json()
print(f"Score de qualidade: {analysis['analysis']['quality_score']}")
print(f"Sugestões: {analysis['analysis']['suggestions']}")
```

## 🛠️ Desenvolvimento

### Estrutura de Logs
Os logs são salvos em `logs/bebrew_api.log` com rotação diária.

### Modo Debug
No modo debug (`DEBUG=True`):
- Documentação automática disponível
- Reload automático do servidor
- Logs detalhados

### Testes
```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar testes
pytest tests/
```

## 🔒 Segurança

- **Autenticação**: Firebase Auth com JWT
- **CORS**: Configurável via variáveis de ambiente
- **Validação**: Pydantic para validação de dados
- **Logs**: Loguru para logging estruturado

## 📈 Monitoramento

### Health Check
```bash
GET /health
```

### Métricas
- Logs estruturados com Loguru
- Timestamps automáticos
- Rastreamento de erros

## 🚨 Troubleshooting

### Erro de Conexão com Firebase
1. Verifique as credenciais no `.env`
2. Confirme se o projeto Firebase está ativo
3. Verifique se Firestore está habilitado

### Erro de OpenAI
1. Verifique se a API key está correta
2. Confirme se há créditos disponíveis
3. Verifique o limite de tokens

### Erro de Autenticação
1. Verifique se o token JWT é válido
2. Confirme se o usuário existe no Firebase
3. Verifique se o token não expirou

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique os logs em `logs/bebrew_api.log`
- Consulte a documentação da API em `/docs`
- Abra uma issue no repositório

---

**Bebrew Backend** - Transformando brassagem em ciência! 🧪🍻 
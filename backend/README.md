# 🚀 Backend Bebrew

Backend da aplicação Bebrew com integração de IA (OpenAI) e Firebase para autenticação e armazenamento.

## 🏗️ Estrutura

```
backend/
├── config/           # Configurações da aplicação
├── services/         # Serviços (IA, Firebase)
├── api/             # API FastAPI
└── README.md        # Este arquivo
```

## 🚀 Início Rápido

1. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas credenciais
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a API**:
   ```bash
   python run_api.py
   ```

4. **Acesse a documentação**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔧 Configuração

### Variáveis de Ambiente Necessárias

```env
# OpenAI
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4

# Firebase
FIREBASE_PROJECT_ID=seu_projeto
FIREBASE_PRIVATE_KEY_ID=sua_key_id
FIREBASE_PRIVATE_KEY="sua_private_key"
FIREBASE_CLIENT_EMAIL=seu_email
FIREBASE_CLIENT_ID=seu_client_id
FIREBASE_CLIENT_X509_CERT_URL=sua_cert_url

# Sistema
DEBUG=True
SECRET_KEY=sua_secret_key
```

## 📚 Documentação Completa

Veja a documentação completa em: [docs/BACKEND.md](../docs/BACKEND.md)

## 🧪 Testes

```bash
# Executar testes
pytest tests/

# Executar com cobertura
pytest --cov=backend tests/
```

## 🔍 Endpoints Principais

- `GET /` - Informações da API
- `GET /health` - Status dos serviços
- `POST /auth/register` - Registrar usuário
- `GET /recipes` - Listar receitas
- `POST /ai/analyze-recipe` - Analisar receita com IA

## 🛠️ Desenvolvimento

### Estrutura de Logs
- Arquivo: `logs/bebrew_api.log`
- Rotação: Diária
- Retenção: 30 dias

### Modo Debug
- Documentação automática
- Reload automático
- Logs detalhados

## 📞 Suporte

Para dúvidas, consulte:
1. Documentação em `docs/BACKEND.md`
2. Logs em `logs/bebrew_api.log`
3. Documentação da API em `/docs`

---

**Bebrew Backend** - Transformando brassagem em ciência! 🧪🍻 
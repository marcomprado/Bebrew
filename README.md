# 🍺 Bebrew - Sistema de Controle de Produção para Brassagem

**Bebrew** é um sistema completo para **controle e monitoramento da produção de bebidas fermentadas**, projetado especificamente para cervejeiros, meadeiros e vinicultores artesanais. O foco está no acompanhamento em tempo real do processo de brassagem, desde a formulação da receita até o produto final.

> **Projeto Privado** desenvolvido por **Marco Martinelli** e **João Mateus** no **PUCtec** (Pontifícia Universidade Católica - Tecnologia).

## 📚 Documentação

- **[🎨 Design e UX](docs/DESIGN.md)** - Interface visual e experiência do usuário
- **[⚙️ Funcionalidades](docs/FEATURES.md)** - Recursos detalhados do sistema
- **[🏗️ Arquitetura](docs/ARCHITECTURE.md)** - Estrutura técnica completa
- **[📦 Instalação](docs/INSTALLATION.md)** - Guia completo de instalação

## 🎯 O que é o Bebrew

O Bebrew foi desenvolvido para resolver os principais desafios da **produção artesanal de bebidas fermentadas**:

- **Controle de Processo**: Monitoramento completo de cada etapa da produção
- **Rastreabilidade**: Registro detalhado de todos os parâmetros e modificações
- **Qualidade**: Controle de temperatura, densidade e timing precisos
- **Repetibilidade**: Capacidade de reproduzir lotes bem-sucedidos
- **Análise**: Dados históricos para melhoria contínua dos processos

## 🔬 Tipos de Bebida Suportados

- **🍺 Cerveja**: Controle de mostura, fervura, fermentação e cálculos específicos (IBU, SRM)
- **🍯 Hidromel**: Dissolução controlada, nutrição de fermento e clarificação
- **🍷 Vinho**: Maceração, fermentação malolática e envelhecimento

## 🛠️ Tecnologias Utilizadas

### Frontend (Interface Desktop)
- **Python 3.8+**: Linguagem principal
- **CustomTkinter**: Interface gráfica moderna
- **Matplotlib**: Visualizações e gráficos
- **NumPy**: Processamento de dados numéricos

### Backend (API)
- **FastAPI**: Framework web moderno e rápido
- **OpenAI**: Integração com IA para análise e otimização
- **Firebase**: Autenticação e banco de dados em tempo real
- **Pydantic**: Validação de dados e configurações
- **Loguru**: Sistema de logging estruturado

## 🚀 Instalação Rápida

> ⚠️ **Projeto Privado**: Este é um projeto acadêmico privado do PUCtec. O acesso ao código fonte é restrito aos desenvolvedores e colaboradores autorizados.

### Pré-requisitos
- Python 3.8 ou superior
- Git (para desenvolvedores autorizados)

### Instalação (Desenvolvedores Autorizados)
```bash
# Clonar o repositório (acesso restrito)
git clone https://github.com/marcomartinelli/bebrew_mvp.git
cd bebrew_mvp

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação (Frontend)
python main.py

# Executar API (Backend) - em outro terminal
python run_api.py
```

### Configuração do Backend

Para usar as funcionalidades de IA e Firebase:

1. **Configure as variáveis de ambiente**:
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite o arquivo .env com suas credenciais
   # - OpenAI API Key
   # - Firebase Project ID e credenciais
   ```

2. **Instale as dependências adicionais**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Acesse a documentação da API**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

> 📚 **Documentação completa do Backend**: Veja [docs/BACKEND.md](docs/BACKEND.md)

## 📁 Arquitetura

```
bebrew_mvp/
├── models/                 # Modelos de dados
├── controls/               # Controladores de negócio
├── view/                   # Interface do usuário (Frontend)
├── util/                   # Utilitários e cálculos
├── backend/                # Backend com API e serviços
│   ├── api/               # API FastAPI
│   ├── services/          # Serviços (IA, Firebase)
│   └── config/            # Configurações
├── tests/                 # Testes automatizados
├── logs/                  # Logs da aplicação
├── docs/                  # Documentação
├── main.py                # Aplicação principal (Frontend)
└── run_api.py             # Script para iniciar API
```



## 🔧 Estado Atual

### Frontend (Interface Desktop)
- ✅ **Modelos de dados** completos
- ✅ **Interface moderna** com tema escuro
- ✅ **Sistema de navegação** intuitivo
- ✅ **Calculadora de ABV** com múltiplas fórmulas
- ✅ **Dashboard** com estatísticas em tempo real
- 🔄 **Monitoramento** em tempo real (em desenvolvimento)

### Backend (API)
- ✅ **API RESTful** com FastAPI
- ✅ **Integração com OpenAI** para análise de receitas
- ✅ **Autenticação Firebase** com JWT
- ✅ **Armazenamento Firestore** para dados
- ✅ **Sistema de logging** estruturado
- ✅ **Documentação automática** (Swagger/ReDoc)
- 🔄 **Testes automatizados** (em desenvolvimento)

## 👥 Autores e Desenvolvimento

### **Equipe de Desenvolvimento**
- **Marco Martinelli** - Desenvolvedor Principal
- **João Mateus** - Co-desenvolvedor

### **Instituição**
- **PUCtec** - Pontifícia Universidade Católica (Setor de Tecnologia)

### **Projeto**
Este é um **projeto privado** desenvolvido como parte de estudos e pesquisa em tecnologia aplicada à produção de bebidas fermentadas.

## 📄 Licença e Uso

### **Licença Privada**
- Este projeto é **propriedade intelectual** dos autores e da instituição PUCtec
- **Uso restrito** para fins acadêmicos e de pesquisa
- **Distribuição não autorizada** sem permissão expressa dos autores
- **Código fonte confidencial** - acesso limitado a colaboradores autorizados

### **Direitos Autorais**
© 2024 Marco Martinelli, João Mateus e PUCtec. Todos os direitos reservados.

## Suporte e Contato

### **Para Desenvolvedores Autorizados**
- **Issues Internas**: Reporte bugs ou solicite funcionalidades
- **Discussões Acadêmicas**: Compartilhe experiências de desenvolvimento
- **Documentação**: Acesso à documentação técnica completa

### **Contato dos Autores**
- **Marco Martinelli**: [Contato via PUCtec]
- **João Mateus**: [Contato via PUCtec]

### **Instituição**
- **PUCtec**: Pontifícia Universidade Católica - Setor de Tecnologia

---

**Bebrew** - Transformando a paixão pela brassagem em controle científico! 🧪🍻

*Projeto acadêmico desenvolvido por Marco Martinelli e João Mateus no PUCtec.*

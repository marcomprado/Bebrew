# 📦 Instalação do Bebrew

Este documento fornece instruções detalhadas para instalar e configurar o sistema Bebrew em diferentes ambientes.

## 🔧 Requisitos do Sistema

### **Requisitos Mínimos**
- **Python**: 3.8 ou superior
- **Sistema Operacional**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **RAM**: 4GB mínimo (8GB recomendado)
- **Espaço em Disco**: 500MB para instalação + espaço para dados
- **Resolução**: 1280x720 mínimo (1920x1080 recomendado)

### **Dependências Python**
```
customtkinter >= 5.2.0
matplotlib >= 3.7.0
numpy >= 1.24.0
```

## 🚀 Instalação Rápida

### **Método 1: Clonagem do Repositório**

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/bebrew_mvp.git
cd bebrew_mvp

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar aplicação
python main.py
```

### **Método 2: Download Direto**

```bash
# 1. Fazer download do ZIP
# (baixar do GitHub e extrair)

# 2. Entrar no diretório
cd bebrew_mvp

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
python main.py
```

## 🐍 Instalação Detalhada do Python

### **Windows**

#### **Método 1: Microsoft Store**
1. Abrir Microsoft Store
2. Buscar "Python 3.11" ou superior
3. Instalar versão oficial
4. Verificar: `python --version`

#### **Método 2: Site Oficial**
1. Acessar [python.org](https://python.org)
2. Baixar versão mais recente
3. Executar instalador
4. ✅ Marcar "Add Python to PATH"
5. Verificar: `python --version`

### **macOS**

#### **Método 1: Homebrew** (Recomendado)
```bash
# Instalar Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python

# Verificar instalação
python3 --version
```

#### **Método 2: Site Oficial**
1. Acessar [python.org](https://python.org)
2. Baixar versão macOS
3. Executar instalador .pkg
4. Verificar: `python3 --version`

### **Linux (Ubuntu/Debian)**

```bash
# Atualizar sistema
sudo apt update

# Instalar Python e pip
sudo apt install python3 python3-pip python3-venv

# Verificar instalação
python3 --version
pip3 --version
```

### **Linux (CentOS/RHEL/Fedora)**

```bash
# CentOS/RHEL
sudo yum install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Verificar instalação
python3 --version
pip3 --version
```

## 🔧 Configuração de Ambiente

### **Ambiente Virtual (Recomendado)**

```bash
# Criar ambiente virtual
python -m venv bebrew_env

# Ativar ambiente virtual
# Windows:
bebrew_env\Scripts\activate

# macOS/Linux:
source bebrew_env/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Desativar quando terminar
deactivate
```

### **Instalação Global**

```bash
# Instalar dependências globalmente
pip install customtkinter matplotlib numpy

# Ou usar arquivo requirements
pip install -r requirements.txt
```

## 🐳 Instalação com Docker

### **Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### **Docker Compose**

```yaml
version: '3.8'
services:
  bebrew:
    build: .
    volumes:
      - ./database:/app/database
      - ./data:/app/data
    environment:
      - DISPLAY=:0
    networks:
      - bebrew_network

networks:
  bebrew_network:
    driver: bridge
```

## 🔍 Verificação da Instalação

### **Teste Básico**

```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Testar imports
python -c "import customtkinter, matplotlib, numpy; print('✅ Todas as dependências OK')"
```

### **Teste da Aplicação**

```bash
# Executar aplicação
python main.py

# Deve abrir a interface gráfica
# Se houver erro, verificar logs no terminal
```

## 🛠️ Configuração Pós-Instalação

### **Primeira Execução**

1. **Configurar Unidades**
   - Temperatura: Celsius/Fahrenheit
   - Volume: Litros/Galões
   - Peso: Quilogramas/Libras

2. **Configurar Diretórios**
   - Criar pasta `database/` se não existir
   - Verificar permissões de escrita

3. **Dados Iniciais**
   - Sistema cria `mock_data.json` automaticamente
   - Receitas de exemplo são carregadas

### **Configurações Opcionais**

```python
# Configurações em config.py (criar se desejar)
BEBREW_CONFIG = {
    'database_path': './database/',
    'backup_interval': 1440,  # minutos
    'theme': 'dark',
    'units': {
        'temperature': 'celsius',
        'volume': 'liters',
        'weight': 'kilograms'
    }
}
```

## 🔧 Solução de Problemas

### **Problemas Comuns**

#### **Erro: "customtkinter not found"**
```bash
# Solução
pip install customtkinter

# Ou forçar reinstalação
pip install --force-reinstall customtkinter
```

#### **Erro: "matplotlib backend"**
```bash
# Linux - instalar dependências GUI
sudo apt install python3-tk

# macOS - instalar TCL/TK
brew install tcl-tk
```

#### **Erro: "Permission denied"**
```bash
# Verificar permissões
ls -la

# Criar diretório database
mkdir database
chmod 755 database
```

#### **Erro: "No module named '_tkinter'"**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Fedora
sudo dnf install python3-tkinter
```

### **Problemas por Sistema**

#### **Windows**
- **Erro PATH**: Adicionar Python ao PATH manualmente
- **Erro DLL**: Reinstalar Python com "Repair"
- **Antivírus**: Adicionar pasta à exceções

#### **macOS**
- **Erro SSL**: `pip install --trusted-host pypi.org customtkinter`
- **Permissions**: Usar `sudo` se necessário
- **Xcode**: Instalar command line tools

#### **Linux**
- **Missing headers**: `sudo apt install python3-dev`
- **GTK issues**: `sudo apt install python3-gi`
- **Display**: Configurar DISPLAY para SSH

## 📊 Configuração para Desenvolvimento

### **Estrutura de Desenvolvimento**

```bash
# Clonar para desenvolvimento
git clone https://github.com/seu-usuario/bebrew_mvp.git
cd bebrew_mvp

# Criar ambiente virtual
python -m venv dev_env
source dev_env/bin/activate  # Linux/macOS
dev_env\Scripts\activate     # Windows

# Instalar dependências de desenvolvimento
pip install -r requirements.txt
pip install pytest black flake8  # opcional
```

### **Configuração do IDE**

#### **Visual Studio Code**
```json
{
    "python.defaultInterpreterPath": "./dev_env/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

#### **PyCharm**
1. Abrir projeto
2. Configurar interpretador Python
3. Apontar para `dev_env/bin/python`

## 🧪 Testes de Instalação

### **Suite de Testes**

```bash
# Teste básico
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import customtkinter as ctk
    print('✅ CustomTkinter OK')
except ImportError as e:
    print(f'❌ CustomTkinter: {e}')

try:
    import matplotlib.pyplot as plt
    print('✅ Matplotlib OK')
except ImportError as e:
    print(f'❌ Matplotlib: {e}')

try:
    import numpy as np
    print('✅ NumPy OK')
except ImportError as e:
    print(f'❌ NumPy: {e}')
"
```

### **Teste de Interface**

```bash
# Teste básico da interface
python -c "
import customtkinter as ctk
root = ctk.CTk()
root.title('Teste Bebrew')
root.geometry('400x300')
label = ctk.CTkLabel(root, text='✅ Interface OK')
label.pack(pady=50)
root.after(2000, root.quit)
root.mainloop()
print('✅ Interface testada com sucesso')
"
```

## 🔄 Atualizações

### **Atualizar Bebrew**

```bash
# Atualizar código
git pull origin main

# Atualizar dependências
pip install --upgrade -r requirements.txt

# Verificar compatibilidade
python main.py --version
```

### **Backup Antes de Atualizar**

```bash
# Backup da base de dados
cp -r database/ database_backup/

# Backup das configurações
cp config.py config_backup.py
```

## 🆘 Suporte

### **Canais de Suporte**
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/bebrew_mvp/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/bebrew_mvp/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/seu-usuario/bebrew_mvp/wiki)

### **Informações para Suporte**
Ao reportar problemas, inclua:

```bash
# Informações do sistema
python --version
pip list | grep -E "(customtkinter|matplotlib|numpy)"
uname -a  # Linux/macOS
systeminfo | findstr /B /C:"OS"  # Windows
```

### **Logs de Debug**
```bash
# Executar com logs detalhados
python main.py --debug

# Ou exportar logs
python main.py > bebrew.log 2>&1
```

---

*Guia de instalação mantido pela comunidade Bebrew. Contribuições são bem-vindas!* 
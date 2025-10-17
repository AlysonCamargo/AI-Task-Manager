# 🤖 AI Task Manager

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema inteligente de gerenciamento de tarefas com API REST completa, banco de dados SQLite e recursos de IA para sugestões e priorização automática.

## ✨ Funcionalidades

### 🎯 Gerenciamento de Tarefas
- ✅ **CRUD Completo**: Criar, ler, atualizar e deletar tarefas
- 🏷️ **Categorização**: Organize por categorias personalizadas
- ⚡ **Prioridades**: Urgente, Alta, Média e Baixa
- 📅 **Prazos**: Defina datas de vencimento
- ⏱️ **Tempo Estimado**: Estime duração das tarefas
- 🏷️ **Tags**: Sistema de tags flexível

### 🤖 Recursos de IA
- 💡 **Sugestões Inteligentes**: IA analisa suas tarefas e sugere ações
- 🎯 **Ordenação Inteligente**: Algoritmo prioriza tarefas automaticamente
- ⚡ **Quick Wins**: Identifica tarefas rápidas para ganhar momentum
- 🔥 **Detecção de Urgência**: Alerta sobre prazos próximos
- 📊 **Análise de Produtividade**: Score de foco e estatísticas

### 📊 Dashboard e Estatísticas
- 📈 **Visão Geral**: Total, pendentes, em progresso e concluídas
- 📉 **Taxa de Conclusão**: Acompanhe sua produtividade
- 📅 **Estatísticas Diárias**: Histórico de produtividade
- 🎯 **Focus Score**: Métrica de concentração

### 🎨 Interface Moderna
- 🎨 **Design Responsivo**: Funciona em todos os dispositivos
- 🌈 **Gradientes Modernos**: Interface visualmente atraente
- ⚡ **Animações Suaves**: Transições elegantes
- 🎭 **Modal Interativo**: Formulários intuitivos

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**:
git clone https://github.com/seu-usuario/ai-task-manager.git
cd ai-task-manager


2. **Crie um ambiente virtual** (recomendado):
python -m venv venv

Windows
venv\Scripts\activate

Linux/Mac
source venv/bin/activate


3. **Instale as dependências**:
pip install -r requirements.txt


4. **Execute a aplicação**:
python app.py


5. **Acesse no navegador**:
http://localhost:5000


## 📡 API REST Endpoints

### Tasks

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/tasks` | Lista todas as tarefas |
| GET | `/api/tasks/<id>` | Busca tarefa específica |
| POST | `/api/tasks` | Cria nova tarefa |
| PUT | `/api/tasks/<id>` | Atualiza tarefa |
| DELETE | `/api/tasks/<id>` | Deleta tarefa |

### Statistics

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/stats/overview` | Estatísticas gerais |
| GET | `/api/stats/productivity` | Produtividade diária |

### AI Features

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/ai/suggestions` | Sugestões inteligentes |
| POST | `/api/ai/smart-sort` | Ordenação por IA |


## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask 3.0**: Framework web Python
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados leve e eficiente
- **Flask-CORS**: Suporte a CORS

### Frontend
- **HTML5**: Estrutura semântica
- **CSS3**: Design moderno com gradientes e animações
- **Vanilla JavaScript**: Interatividade sem frameworks


### Sugestões Inteligentes

1. **Detecção de Urgência**: Identifica tarefas urgentes próximas do prazo
2. **Quick Wins**: Encontra tarefas rápidas para criar momentum
3. **Foco por Horário**: Sugere tarefas complexas em horários de pico
4. **Agrupamento**: Recomenda focar em categorias específicas
5. **Motivação**: Mensagens inspiradoras personalizadas

## 📊 Exemplos de Uso da API

### Criar Tarefa
curl -X POST http://localhost:5000/api/tasks
-H "Content-Type: application/json"
-d '{
"title": "Estudar Python",
"description": "Revisar Flask e SQLAlchemy",
"priority": "high",
"category": "Estudos",
"estimated_time": 60
}'


### Buscar Tarefas Pendentes
curl http://localhost:5000/api/tasks?status=pending


### Obter Sugestões de IA
curl http://localhost:5000/api/ai/suggestions


## 🎯 Conceitos Demonstrados

- ✅ **API RESTful**: Endpoints bem estruturados e documentados
- ✅ **ORM**: SQLAlchemy para manipulação de dados
- ✅ **Arquitetura MVC**: Separação de responsabilidades
- ✅ **CORS**: Configuração para APIs públicas
- ✅ **Validação de Dados**: Backend robusto
- ✅ **Algoritmos de IA**: Priorização e sugestões inteligentes
- ✅ **Frontend Moderno**: Vanilla JS com fetch API
- ✅ **Responsividade**: Mobile-first design

## 🔮 Melhorias Futuras

- [ ] Autenticação de usuários (JWT)
- [ ] Integração com Google Calendar
- [ ] Notificações por email
- [ ] Modo escuro
- [ ] Exportar tarefas (JSON/CSV)
- [ ] Integração com IA real (OpenAI)
- [ ] Pomodoro timer integrado
- [ ] Colaboração em tempo real


---

⭐ Se este projeto foi útil, considere dar uma estrela!

💼 Perfeito para demonstrar habilidades em **Python**, **Flask**, **APIs REST** e **SQLite**.




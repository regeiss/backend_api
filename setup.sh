#!/bin/bash
# Script para criar a estrutura do projeto

# Criar estrutura de diretórios
mkdir -p cadastro_unificado_api
cd cadastro_unificado_api

# Estrutura principal
mkdir -p backend/{apps/{api,cadastro},config,static,media}
mkdir -p nginx
mkdir -p scripts

# Criar arquivo .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.env
*.sqlite3
.idea/
.vscode/
*.swp
*.swo

# Django
/media
/static
*.log
local_settings.py
db.sqlite3

# Docker
.docker/

# OS
.DS_Store
Thumbs.db
EOF

# Criar README.md
cat > README.md << 'EOF'
# Cadastro Unificado API

API Django para integração com banco de dados Oracle existente.

## Instalação

1. Clone o repositório
2. Configure as variáveis de ambiente no arquivo `.env`
3. Execute: `docker-compose up -d`
4. Acesse a documentação da API em: `http://localhost:8001/api/docs/`

## Comandos úteis

```bash
# Gerar models das tabelas existentes
docker-compose exec backend python manage.py inspectdb > apps/cadastro/models_generated.py

# Aplicar migrations
docker-compose exec backend python manage.py migrate

# Criar superusuário
docker-compose exec backend python manage.py createsuperuser
```
EOF

echo "Estrutura de diretórios criada!"
echo "Agora crie os arquivos individuais conforme os artifacts seguintes."

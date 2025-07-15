#!/bin/sh

# Aguardar o banco de dados
echo "Aguardando banco de dados..."
while ! nc -z ${DATABASE_HOST:-10.13.66.8} ${DATABASE_PORT:-5432}; do
    sleep 0.1
done
echo "Banco de dados disponível!"

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Aplicar migrations (apenas as do Django, não das models existentes)
python manage.py migrate --run-syncdb

# Executar comando
exec "$@"

#!/bin/bash

echo "=== VERIFICAÇÃO RÁPIDA DE USUÁRIOS ==="
echo

# Verificar se containers estão rodando
echo "🔍 Verificando containers..."
docker compose ps

echo
echo "🗄️ Verificando usuários no banco..."

# Executar verificação via Django shell
docker compose exec backend python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

print('👥 USUÁRIOS EXISTENTES:')
print('-' * 40)
users = User.objects.all()
if users:
    for user in users:
        status = '✅' if user.is_active else '❌'
        admin = '👑' if user.is_superuser else '👤'
        print(f'{admin} {user.username:15} | {user.email:25} | {status}')
    print(f'Total: {users.count()} usuários')
else:
    print('❌ Nenhum usuário encontrado!')
    print()
    print('🔧 Criando usuário admin...')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com', 
        password='admin123'
    )
    print('✅ Usuário admin criado!')
    print('   Username: admin')
    print('   Password: admin123')
"

echo
echo "🔐 Testando login com curl..."

# Testar login com usuário admin
echo "Testando admin:admin123..."
curl -s -X POST http://10.13.65.37:8001/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq '.'

echo
echo "🔧 Para criar o usuário 'robertogeis', execute:"
echo "docker compose exec backend python -c \"
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Criar usuário robertogeis
try:
    user = User.objects.create_superuser(
        username='robertogeis',
        email='roberto@example.com',
        password='(*3Lv1nh0*)'
    )
    print('✅ Usuário robertogeis criado com sucesso!')
except Exception as e:
    print(f'❌ Erro: {e}')
    # Se já existe, resetar senha
    try:
        user = User.objects.get(username='robertogeis')
        user.set_password('(*3Lv1nh0*)')
        user.save()
        print('✅ Senha do robertogeis resetada!')
    except:
        pass
\""

echo
echo "📋 RESUMO:"
echo "1. Execute o comando acima para criar/resetar o usuário"
echo "2. Teste o login: curl -X POST http://10.13.65.37:8001/api/v1/auth/login/ -H 'Content-Type: application/json' -d '{\"username\": \"robertogeis\", \"password\": \"(*3Lv1nh0*)\"}'"
echo "3. Se der erro, use admin:admin123 como alternativa"

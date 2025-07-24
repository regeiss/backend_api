#!/usr/bin/env python3
"""
Script para gerenciar usuários via Django shell
Execute: docker compose exec backend python scripts/manage_users.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

def list_all_users():
    """Lista todos os usuários"""
    print("👥 USUÁRIOS EXISTENTES:")
    print("-" * 50)
    
    users = User.objects.all()
    if not users:
        print("❌ Nenhum usuário encontrado!")
        return False
    
    for user in users:
        status = "✅ Ativo" if user.is_active else "❌ Inativo"
        admin = "👑 Admin" if user.is_superuser else "👤 User"
        print(f"{user.username:15} | {user.email:25} | {status} | {admin}")
    
    print(f"\nTotal: {users.count()} usuários")
    return True

def check_user(username):
    """Verifica se usuário existe"""
    print(f"\n🔍 VERIFICANDO USUÁRIO: {username}")
    print("-" * 50)
    
    try:
        user = User.objects.get(username=username)
        print(f"✅ Usuário encontrado!")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Nome: {user.first_name} {user.last_name}")
        print(f"   Ativo: {'Sim' if user.is_active else 'Não'}")
        print(f"   Admin: {'Sim' if user.is_superuser else 'Não'}")
        print(f"   Staff: {'Sim' if user.is_staff else 'Não'}")
        print(f"   Criado em: {user.date_joined}")
        print(f"   Último login: {user.last_login}")
        return user
    except User.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado!")
        return None

def create_user(username, password, email="", first_name="", last_name="", is_superuser=False):
    """Cria um novo usuário"""
    print(f"\n➕ CRIANDO USUÁRIO: {username}")
    print("-" * 50)
    
    try:
        if User.objects.filter(username=username).exists():
            print(f"❌ Usuário '{username}' já existe!")
            return None
        
        if is_superuser:
            user = User.objects.create_superuser(
                username=username,
                password=password,
                email=email
            )
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        
        print(f"✅ Usuário '{username}' criado com sucesso!")
        print(f"   Tipo: {'Superusuário' if is_superuser else 'Usuário comum'}")
        return user
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        return None

def test_login(username, password):
    """Testa login do usuário"""
    print(f"\n🔐 TESTANDO LOGIN: {username}")
    print("-" * 50)
    
    from django.contrib.auth import authenticate
    
    try:
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                print(f"✅ Login bem-sucedido para '{username}'!")
                return True
            else:
                print(f"❌ Usuário '{username}' existe mas está inativo!")
                return False
        else:
            print(f"❌ Falha no login para '{username}' - credenciais inválidas!")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar login: {e}")
        return False

def reset_password(username, new_password):
    """Reseta a senha do usuário"""
    print(f"\n🔑 RESETANDO SENHA: {username}")
    print("-" * 50)
    
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        print(f"✅ Senha do usuário '{username}' resetada com sucesso!")
        return True
    except User.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado!")
        return False
    except Exception as e:
        print(f"❌ Erro ao resetar senha: {e}")
        return False

def check_database_connection():
    """Verifica conexão com banco"""
    print("🗄️  VERIFICANDO CONEXÃO COM BANCO")
    print("-" * 50)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexão com banco OK!")
        
        # Verificar tabela auth_user
        cursor.execute("SELECT COUNT(*) FROM auth_user")
        count = cursor.fetchone()[0]
        print(f"✅ Tabela auth_user OK - {count} usuários")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def main():
    print("=== GERENCIADOR DE USUÁRIOS - Django ===\n")
    
    # Verificar conexão
    if not check_database_connection():
        return
    
    # Listar usuários existentes
    list_all_users()
    
    # Verificar usuário específico
    target_username = "robertogeis"
    user = check_user(target_username)
    
    if not user:
        print(f"\n❓ Usuário '{target_username}' não existe.")
        print("Vamos criar um usuário de teste...")
        
        # Criar usuário de teste
        create_user(
            username=target_username,
            password="(*3Lv1nh0*)",
            email="roberto@example.com",
            first_name="Roberto",
            last_name="Geis",
            is_superuser=True
        )
        
        # Verificar novamente
        user = check_user(target_username)
    
    if user:
        # Testar login
        test_login(target_username, "(*3Lv1nh0*)")
    
    print("\n🔧 CRIANDO USUÁRIOS DE TESTE ADICIONAIS...")
    print("-" * 50)
    
    # Criar usuários de teste padrão
    test_users = [
        {
            "username": "admin",
            "password": "admin123",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "is_superuser": True
        },
        {
            "username": "teste",
            "password": "teste123",
            "email": "teste@example.com", 
            "first_name": "Usuario",
            "last_name": "Teste",
            "is_superuser": False
        }
    ]
    
    for user_data in test_users:
        if not User.objects.filter(username=user_data["username"]).exists():
            create_user(**user_data)
            test_login(user_data["username"], user_data["password"])
    
    print("\n" + "="*50)
    print("✅ Verificação completa!")
    print("\n📋 USUÁRIOS DISPONÍVEIS PARA TESTE:")
    print(f"   - {target_username} : (*3Lv1nh0*)")
    print("   - admin : admin123")
    print("   - teste : teste123")

if __name__ == "__main__":
    main()

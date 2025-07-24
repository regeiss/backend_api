from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Responsavel

class ResponsavelAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.responsavel_data = {
            'cpf': '12345678901',
            'nome': 'João Silva',
            'cep': '01234567',
            'numero': 123
        }
    
    def test_create_responsavel(self):
        """Testa criação de responsável"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('cadastro:responsavel-list'),
            self.responsavel_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_responsaveis(self):
        """Testa listagem de responsáveis"""
        response = self.client.get(reverse('cadastro:responsavel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

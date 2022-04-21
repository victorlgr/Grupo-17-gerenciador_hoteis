import unittest
from flask import url_for
from flask_login import current_user
from flask import request
from base import TesteBase


class TestarUsuario(TesteBase):

    # Efetua login
    def login(self, email, senha):
        response = self.client.post('/login/',
                                    data=dict(email=email,
                                              password=senha),
                                    follow_redirects=True)
        return response

    def adicionar_hotel(self):
        response = self.client.post('/adicionar-hotel/',
                                    data=dict(name='hotel',
                                              phone='40028922',
                                              email='hotel',
                                              cnpj='00000000000000',
                                              endereco='Rua do hotel',
                                              numero='1',
                                              complemento='logo ali',
                                              bairro='Do hotel',
                                              cidade='Hoteleira',
                                              estado='California',
                                              pais='O nosso',
                                              cep='00000000'),
                                    follow_redirects=True)
        return response

    def adicionar_hospede(self):
        response = self.client.post(url_for('adicionar_hospede_endpoint'),
                                    data=dict(hotel_id=1,
                                              name='Agostinho Carrara',
                                              email='agostinho@carrara.com',
                                              phone='11111111',
                                              cpf='000.000.000-00',
                                              birthday='31/08/1965',
                                              cep='00000-000',
                                              endereco='Casa do Irineu',
                                              numero='1',
                                              complemento='1',
                                              bairro='Baixada fluminence',
                                              cidade='São Gonçalo',
                                              estado='RJ',
                                              pais='Brasil',
                                              submeter=True),
                                    follow_redirects=True)
        return response

    # Testar se o usuário consegue realizar login
    def test_user_login_correto(self):
        with self.client:
            response = self.login('admin@admin.com', '1234')
            self.assertIn(b'Sair', response.data)

    # Testar se o usuário consegue realizar login
    def test_user_login_incorreto(self):
        with self.client:
            response = self.login('errado@errado.com', 'errado')
            self.assertIn(b'E-mail n\xc3\xa3o encontrado', response.data)

    # Testar o logout
    def test_user_logout(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            response = self.client.get('/logout/', follow_redirects=True)
            self.assertIn(b'Entrar', response.data)

    # Testar adicionar um hotel
    def test_adicionar_hotel(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            response = self.adicionar_hotel()
            self.assertIn(b'Hotel cadastrado com sucesso', response.data)

    # Testar adicionar um hóspede
    def test_adicionar_hospede(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            response = self.adicionar_hospede()
            self.assertIn(b'sucesso', response.data)

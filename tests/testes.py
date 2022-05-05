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

    def editar_hotel(self):
        response = self.client.post('/editar-hotel/1',
                                    data=dict(name='hotel editado',
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

    def adicionar_quarto(self):
        response = self.client.post(url_for('adicionar_quarto_endpoint'),
                                    data=dict(number='101',
                                              hotel_id=1,
                                              kind='suite megaboga',
                                              phone_extension='1001',
                                              price='9999999999',
                                              guest_limit=6),
                                    follow_redirects=True)
        return response

    def editar_quarto(self):
        response = self.client.post(url_for('editar_quarto_endpoint', id='1'),
                                    data=dict(number='102',
                                              hotel_id=1,
                                              kind='suite megaboga',
                                              phone_extension='1001',
                                              price='9999999999',
                                              guest_limit=6),
                                    follow_redirects=True)
        return response

    def adicionar_usuario(self):
        response = self.client.post(url_for('save'),
                                    data=dict(name='Naruto',
                                              password='1234',
                                              profile='admin',
                                              email='naruto@viladafolha.com',
                                              password_confirmation='1234',
                                              hotel_id=1),
                                    follow_redirects=True)
        return response

    def editar_usuario(self):
        response = self.client.post(url_for('editar_usuario_endpoint', id=1),
                                    data=dict(name='Sakura',
                                              password='1234',
                                              profile='admin',
                                              email='sakura@viladafolha.com',
                                              password_confirmation='1234',
                                              hotel_id=1),
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

    def editar_hospede(self):
        response = self.client.post(url_for('editar_hospede_endpoint', id='1'),
                                    data=dict(hotel_id=1,
                                              name='Agostinho Carrara',
                                              email='agostinho@carrara.com',
                                              phone='22222222',
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

    def adicionar_conta(self):
        response = self.client.post(url_for('adicionar_conta_endpoint'),
                                    data=dict(hotel_id=1,
                                              guest_id=1,
                                              tipo='Contas a receber',
                                              descricao='pao de queijo matutino com nescau',
                                              valor=20
                                              ),
                                    follow_redirects=True)
        return response

    def editar_conta(self):
        response = self.client.post(url_for('editar_conta_endpoint', id='1'),
                                    data=dict(hotel_id=1,
                                              guest_id=1,
                                              tipo='Contas a receber',
                                              descricao='pao de queijo matutino com toddy',
                                              valor=20
                                              ),
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

    # Testar editar um hotel
    def test_editar_hotel(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            response = self.editar_hotel()
            self.assertIn(b'Hotel editado com sucesso', response.data)

    # Testar deletar um hotel
    def test_deletar_hotel(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            response = self.client.get(url_for('deletar_hotel_endpoint', id=1), follow_redirects=True)
            self.assertIn(b'Hotel deletado com sucesso', response.data)

    # Testar adicionar um quarto
    def test_adicionar_quarto(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            response = self.adicionar_quarto()
            self.assertIn(b'Quarto cadastrado com sucesso', response.data)

    # Testar editar um quarto
    def test_editar_quarto(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_quarto()
            response = self.editar_quarto()
            self.assertIn(b'Quarto editado com sucesso', response.data)

    # Testar deletar um quarto
    def test_deletar_quarto(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_quarto()
            response = self.client.get(url_for('deletar_quarto_endpoint', id=1), follow_redirects=True)
            self.assertIn(b'Quarto deletado com sucesso', response.data)

    # Testar adicionar um usuário
    def test_adicionar_usuario(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            response = self.adicionar_usuario()
            self.assertIn(b'Cadastro realizado com sucesso', response.data)

    # Testar adicionar um usuário
    def test_editar_usuario(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_usuario()
            response = self.editar_usuario()
            self.assertIn(b'Usu\xc3\xa1rio editado com sucesso', response.data)

    # Testar deletar um usuário
    def test_deletar_usuario(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_usuario()
            response = self.client.get(url_for('deletar_usuario_endpoint', id=2), follow_redirects=True)
            self.assertIn(b'Usu\xc3\xa1rio deletado com sucesso', response.data)

    # Testar adicionar um hóspede
    def test_adicionar_hospede(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            response = self.adicionar_hospede()
            self.assertIn(b'H\xc3\xb3spede cadastrado com sucesso', response.data)

    # Testar editar um hóspede
    def test_editar_hospede(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_hospede()
            response = self.editar_hospede()
            self.assertIn(b'H\xc3\xb3spede editado com sucesso', response.data)

    # Testar deletar um hóspede
    def test_deletar_hospede(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_hospede()
            response = self.client.get(url_for('deletar_hospede_endpoint', id=1), follow_redirects=True)
            self.assertIn(b'H\xc3\xb3spede deletado com sucesso', response.data)

    # Testar adicionar uma conta
    def test_adicionar_conta(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_hospede()
            response = self.adicionar_conta()
            self.assertIn(b'Conta cadastrada com sucesso', response.data)

    # Testar editar uma conta
    def test_editar_conta(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_hospede()
            self.adicionar_conta()
            response = self.editar_conta()
            self.assertIn(b'Conta editada com sucesso', response.data)

    # Testar deletar uma conta
    def test_deletar_conta(self):
        with self.client:
            self.login('admin@admin.com', '1234')
            self.adicionar_hotel()
            self.adicionar_hospede()
            self.adicionar_conta()
            response = self.client.get(url_for('deletar_conta_endpoint', id=1), follow_redirects=True)
            self.assertIn(b'Conta deletada com sucesso', response.data)

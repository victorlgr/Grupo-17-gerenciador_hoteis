import unittest
from flask import url_for
from flask_login import current_user
from flask import request
from base import TesteBase


class TestarUsuario(TesteBase):

    # Testar se o usuário consegue realizar login
    def test_user_login_correto(self):
        with self.client:
            response = self.client.post('/login/',
                                        data=dict(typeEmailX='admin@admin.com',
                                                  typePasswordX='1234'),
                                        follow_redirects=True)
            self.assertIn(b'Sair', response.data)


class TestarHotel(TesteBase):

    # Testar se é possível adicionar um hotel
    pass
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth
import json
auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verify(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class Pessoa(Resource):
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()

            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada.'

            }

        return response

    @auth.login_required
    def put(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            dados = request.json

            if 'nome' in dados:
                pessoa.nome = dados['nome']
            if 'idade' in dados:
                pessoa.idade = dados['idade']
            pessoa.save()

            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada.'
            }
        return response
    @auth.login_required
    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()

            response = {
                'status': 'sucesso',
                'mensagem': 'Pessoa {} excluída.'.format(pessoa.nome)
            }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Não foi possível excluir. Pessoa não encontrada.'
            }


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'status': 'sucesso',
            'mensagem': 'Registro Adicionado.'
        }
        return response

class TarefaPessoa(Resource):
    def get(self, nomePessoa):
        try:
            pessoa = Pessoas.query.filter_by(nome=nomePessoa).first()
            atividades = Atividades.query.filter_by(pessoa=pessoa)
            response = [
                    {'pessoa': pessoa.nome},
                    {
                     'nome': p.nome for p in atividades
                    }
                ]

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada.'

            }

        return response

class Tarefa(Resource):
    def get(self):
        pass

    @auth.login_required
    def delete(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            response = {
                'status': 'sucesso',
                'mensagem': 'Atividade {} excluída.'.format(atividade.nome)
            }
            atividade.delete()

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Não foi possivel excluir. Tarefa não encontrada.'
            }
        return
    def put(self):
        pass


class ListaTarefas(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome} for i in atividades]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'id': atividade.id
        }
        return response


api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaTarefas, '/tarefa/')
api.add_resource(Tarefa, '/tarefa/<int:id>')
api.add_resource(TarefaPessoa, '/tarefa/pessoa/<string:nomePessoa>')



if __name__ == '__main__':
    app.run(debug=True)

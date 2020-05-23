from models import Pessoas

#Insere Dados na Tabela Pessoa
def insere_pessoa(nome, idade):
    pessoa = Pessoas(nome=nome, idade=idade)
    print(pessoa)
    pessoa.save()

#Consulta Dados na Tabela Pessoa
def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)

#Edita Dados na Tabela Pessoa
def edita_pessoa(nomePessoa, novoNome):
    pessoa = Pessoas.query.filter_by(nome=nomePessoa).first()
    pessoa.nome = novoNome
    print(pessoa)
    pessoa.save()


#Exclui Dados na Tabela Pessoa
def remove_pessoa(nome):
    pessoa=Pessoas.query.filter_by(nome=nome).first()
    pessoa.delete()

if __name__ == '__main__':
    #insere_pessoa('Jorel', 33)
    #remove_pessoa('John Doe')
    #edita_pessoa('Jorel', 'Nico')
    consulta_pessoas()
from banco.usuario import Usuario
from banco.conta import ContaCorrente

class Banco:
    def __init__(self):
        self.usuarios = []
        self.numero_conta_sequencial = 1

    def cadastrar_usuario(self, nome, data_nascimento, cpf, endereco):
        if any(usuario.cpf == cpf for usuario in self.usuarios):
            raise ValueError("CPF já cadastrado.")
        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_usuario)
        return novo_usuario

    def cadastrar_conta_corrente(self, usuario):
        nova_conta = ContaCorrente(usuario, self.numero_conta_sequencial)
        self.numero_conta_sequencial += 1
        usuario.contas.append(nova_conta)
        return nova_conta

    def listar_contas(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario.contas
        raise ValueError("Usuário não encontrado.")

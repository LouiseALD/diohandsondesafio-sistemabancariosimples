class ContaCorrente:
    agencia = '0001'

    def __init__(self, usuario, numero_conta, saldo=0.0, limite_saque=500.0, limite_saques_diarios=3):
        self.usuario = usuario
        self.numero_conta = numero_conta
        self.saldo = saldo
        self.extrato = []
        self.limite_saque = limite_saque
        self.limite_saques_diarios = limite_saques_diarios
        self.numero_saques = 0

    def depositar(self, valor, /, saldo, extrato):
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: R$ {valor:.2f}")
            return saldo, extrato
        else:
            raise ValueError("Valor de depósito inválido.")

    def sacar(self, valor, /, *, saldo, extrato):
        if valor <= 0:
            raise ValueError("Valor de saque inválido.")
        if valor > saldo:
            raise ValueError("Saldo insuficiente.")
        if self.numero_saques >= self.limite_saques_diarios:
            raise ValueError("Limite de saques diários excedido.")
        if valor > self.limite_saque:
            raise ValueError("Valor acima do limite de saque permitido.")

        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        self.numero_saques += 1
        return saldo, extrato

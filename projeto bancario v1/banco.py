class Banco:
    def __init__(self):
        self.saldo = 0.0
        self.extrato = []

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Valor Depósito: R$ {valor:.2f}")
            return True, f"Depósito no valor de R$ {valor:.2f} realizado com sucesso!"
        else:
            return False, "Valor de depósito inválido. Tente novamente."

    def sacar(self, valor):
        if valor <= 0:
            return False, "Valor de saque inválido."
        elif valor > self.saldo:
            return False, "Valor de Saldo insuficiente."
        else:
            self.saldo -= valor
            self.extrato.append(f"Saque: R$ {valor:.2f}")
            return True, f"Saque no valor de R$ {valor:.2f} realizado com sucesso!"

    def ver_extrato(self):
        return "\n".join(self.extrato) if self.extrato else "Nenhuma transação realizada."

    def obter_saldo(self):
        return self.saldo

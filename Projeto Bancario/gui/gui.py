import tkinter as tk
from tkinter import messagebox
from banco.banco import Banco
from utils.validacao import validar_nome, validar_data_nascimento, validar_cpf, validar_endereco

class BancoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Bancário")

        self.banco = Banco()
        self.usuario_logado = None

        # Criação da interface de login/cadastro
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.label_login = tk.Label(self.master, text="Login", font=("Arial", 16))
        self.label_login.pack(pady=10)

        self.label_cpf = tk.Label(self.master, text="CPF:")
        self.label_cpf.pack()
        self.entry_cpf = tk.Entry(self.master)
        self.entry_cpf.pack(pady=5)

        self.label_nome = tk.Label(self.master, text="Nome (somente para cadastro):")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(self.master)
        self.entry_nome.pack(pady=5)

        self.label_nascimento = tk.Label(self.master, text="Data de Nascimento (somente para cadastro):")
        self.label_nascimento.pack()
        self.entry_nascimento = tk.Entry(self.master)
        self.entry_nascimento.pack(pady=5)

        self.label_endereco = tk.Label(self.master, text="Endereço (somente para cadastro):")
        self.label_endereco.pack()
        self.entry_endereco = tk.Entry(self.master)
        self.entry_endereco.pack(pady=5)

        self.btn_login = tk.Button(self.master, text="Login", command=self.login_usuario)
        self.btn_login.pack(pady=5)

        self.btn_cadastrar = tk.Button(self.master, text="Cadastrar Usuário", command=self.cadastrar_usuario)
        self.btn_cadastrar.pack(pady=5)

    def create_main_screen(self):
        self.clear_screen()

        self.label_saldo = tk.Label(self.master, text=f"Saldo: R$ {self.usuario_logado.contas[0].saldo:.2f}", font=("Arial", 16))
        self.label_saldo.pack(pady=10)

        self.label_valor = tk.Label(self.master, text="Valor:")
        self.label_valor.pack()
        self.entry_valor = tk.Entry(self.master)
        self.entry_valor.pack(pady=5)

        self.btn_depositar = tk.Button(self.master, text="Depositar", command=self.depositar)
        self.btn_depositar.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_sacar = tk.Button(self.master, text="Sacar", command=self.sacar)
        self.btn_sacar.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_extrato = tk.Button(self.master, text="Ver Extrato", command=self.ver_extrato)
        self.btn_extrato.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_nova_conta = tk.Button(self.master, text="Criar Nova Conta", command=self.criar_nova_conta)
        self.btn_nova_conta.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_sair = tk.Button(self.master, text="Sair", command=self.logout)
        self.btn_sair.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_buscar_cpf = tk.Button(self.master, text="Buscar Contas por CPF", command=self.buscar_contas_por_cpf)
        self.btn_buscar_cpf.pack(side=tk.LEFT, padx=10, pady=10)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def login_usuario(self):
        cpf = self.entry_cpf.get()
        if not validar_cpf(cpf):
            messagebox.showwarning("Erro", "CPF inválido. Use 11 dígitos.")
            return
        for usuario in self.banco.usuarios:
            if usuario.cpf == cpf:
                self.usuario_logado = usuario
                self.create_main_screen()
                return
        messagebox.showwarning("Erro", "Usuário não encontrado!")

    def cadastrar_usuario(self):
        nome = self.entry_nome.get()
        data_nascimento = self.entry_nascimento.get()
        cpf = self.entry_cpf.get()
        endereco = self.entry_endereco.get()

        if not validar_nome(nome):
            messagebox.showwarning("Erro", "Nome inválido. Use o formato 'Nome Sobrenome'.")
            return

        if not validar_data_nascimento(data_nascimento):
            messagebox.showwarning("Erro", "Data de nascimento inválida. Use o formato DD/MM/AAAA.")
            return

        if not validar_cpf(cpf):
            messagebox.showwarning("Erro", "CPF inválido. Use 11 dígitos.")
            return

        if not validar_endereco(endereco):
            messagebox.showwarning("Erro", "Endereço inválido. Use o formato 'Rua A, 123 - Bairro - Cidade / UF'.")
            return

        try:
            usuario = self.banco.cadastrar_usuario(nome, data_nascimento, cpf, endereco)
            self.banco.cadastrar_conta_corrente(usuario)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def criar_nova_conta(self):
        nova_conta = self.banco.cadastrar_conta_corrente(self.usuario_logado)
        messagebox.showinfo("Sucesso", f"Nova conta criada com número: {nova_conta.numero_conta}")

    def buscar_contas_por_cpf(self):
        cpf = self.entry_cpf.get()
        if not validar_cpf(cpf):
            messagebox.showwarning("Erro", "CPF inválido. Use 11 dígitos.")
            return
        try:
            contas = self.banco.listar_contas(cpf)
            contas_info = "\n".join([f"Conta {conta.numero_conta}, Agência: {conta.agencia}, Saldo: R$ {conta.saldo:.2f}" for conta in contas])
            messagebox.showinfo("Contas Encontradas", contas_info)
        except ValueError as e:
            messagebox.showwarning("Erro", str(e))

    def depositar(self):
        valor = self.obter_valor()
        if valor is not None:
            conta = self.usuario_logado.contas[0]
            saldo_atual, extrato_atual = conta.depositar(valor, saldo=conta.saldo, extrato=conta.extrato)
            conta.saldo = saldo_atual
            conta.extrato = extrato_atual
            self.atualizar_saldo()
            messagebox.showinfo("Depósito", f"Depósito de R$ {valor:.2f} realizado com sucesso!")

    def sacar(self):
        valor = self.obter_valor()
        if valor is not None:
            conta = self.usuario_logado.contas[0]
            try:
                saldo_atual, extrato_atual = conta.sacar(valor, saldo=conta.saldo, extrato=conta.extrato)
                conta.saldo = saldo_atual
                conta.extrato = extrato_atual
                self.atualizar_saldo()
                messagebox.showinfo("Saque", f"Saque de R$ {valor:.2f} realizado com sucesso!")
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def ver_extrato(self):
        conta = self.usuario_logado.contas[0]
        extrato = "\n".join(conta.extrato)
        messagebox.showinfo("Extrato", extrato)

    def obter_valor(self):
        try:
            valor = float(self.entry_valor.get())
            if valor <= 0:
                messagebox.showwarning("Valor Inválido", "Por favor, insira um valor maior que zero.")
                return None
            return valor
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira um valor numérico válido.")
            return None

    def atualizar_saldo(self):
        self.label_saldo.config(text=f"Saldo: R$ {self.usuario_logado.contas[0].saldo:.2f}")

    def logout(self):
        self.usuario_logado = None
        self.create_login_screen()

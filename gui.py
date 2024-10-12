import tkinter as tk
from tkinter import messagebox
from banco import Banco  # Importa a lógica do banco

class BancoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistema Bancário")

        self.banco = Banco()

        # Labels
        self.label_saldo = tk.Label(master, text=f"Saldo: R$ {self.banco.obter_saldo():.2f}", font=("Arial", 14))
        self.label_saldo.pack(pady=10)

        # Campo de valor
        self.label_valor = tk.Label(master, text="Valor:")
        self.label_valor.pack()
        self.entry_valor = tk.Entry(master)
        self.entry_valor.pack(pady=5)

        # Botões
        self.btn_depositar = tk.Button(master, text="Depositar", command=self.depositar)
        self.btn_depositar.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_sacar = tk.Button(master, text="Sacar", command=self.sacar)
        self.btn_sacar.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_extrato = tk.Button(master, text="Extrato", command=self.ver_extrato)
        self.btn_extrato.pack(side=tk.LEFT, padx=10, pady=10)

    def depositar(self):
        valor = self.obter_valor()
        if valor is not None:
            sucesso, mensagem = self.banco.depositar(valor)
            if sucesso:
                self.atualizar_saldo()
            messagebox.showinfo("Depósito", mensagem)

    def sacar(self):
        valor = self.obter_valor()
        if valor is not None:
            sucesso, mensagem = self.banco.sacar(valor)
            if sucesso:
                self.atualizar_saldo()
            else:
                messagebox.showwarning("Erro", mensagem)

    def ver_extrato(self):
        extrato = self.banco.ver_extrato()
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
        self.label_saldo.config(text=f"Saldo: R$ {self.banco.obter_saldo():.2f}")
        self.entry_valor.delete(0, tk.END)

import re

def validar_nome(nome):
    return bool(re.match(r"^[A-Za-z]+\s[A-Za-z]+$", nome))

def validar_data_nascimento(data):
    return bool(re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", data))

def validar_cpf(cpf):
    return bool(re.match(r"^\d{11}$", cpf))

def validar_endereco(endereco):
    return bool(re.match(r"^[A-Za-z\s]+,\s\d+\s-\s[A-Za-z\s]+-\s[A-Za-z\s]+/\s[A-Z]{2}$", endereco))

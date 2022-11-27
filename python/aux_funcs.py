"""
    Funções auxiliares para o projeto
"""

import os
import time
import random
import json
from tabulate import tabulate
from simple_colors import *
import subprocess

# Inicialização de pastas
os.chdir('..')
root = os.getcwd()
os.chdir('python')

def init_folders():
    completed = False

    bar = [
    35*" " + "Inicializando infraestrutura ⢿",
    35*" " + "Inicializando infraestrutura ⣻",
    35*" " + "Inicializando infraestrutura ⣽",
    35*" " + "Inicializando infraestrutura ⣾",
    35*" " + "Inicializando infraestrutura ⣷",
    35*" " + "Inicializando infraestrutura ⣯",
    35*" " + "Inicializando infraestrutura ⣟",
    35*" " + "Inicializando infraestrutura ⡿",
    ]

    os.chdir(f'{root}/servers/sa-east-1')
    process1 = subprocess.Popen(['terraform init'],stdout = subprocess.PIPE, stderr = subprocess.DEVNULL, shell = True)
    os.chdir(f'{root}/servers/us-east-1')
    process2 = subprocess.Popen(['terraform init'],stdout = subprocess.PIPE, stderr = subprocess.DEVNULL, shell = True)
    os.chdir(f'{root}/servers/us-east-2')
    process3 = subprocess.Popen(['terraform init'],stdout = subprocess.PIPE, stderr = subprocess.DEVNULL, shell = True)
    os.chdir(f'{root}/servers/us-west-1')
    process4 = subprocess.Popen(['terraform init'],stdout = subprocess.PIPE, stderr = subprocess.DEVNULL, shell = True)
    os.chdir(f'{root}/servers/us-east-2')
    process5 = subprocess.Popen(['terraform init'],stdout = subprocess.PIPE, stderr = subprocess.DEVNULL, shell = True)
    os.chdir(f'{root}/python')

    i = 0
    while not completed:
        print(f"\033[1m{bar[i % len(bar)]}\033[0m", end="\r")
        time.sleep(.1)
        if process1.poll() is not None and process2.poll() is not None and process3.poll() is not None and process4.poll() is not None and process5.poll() is not None:
            completed = True
        i += 1
    
    print(green(35*" " + "Estrutura inicializada com sucesso!                   ", "bold"))

    time.sleep(2)

# Cores
class color:
    BOLD = '\033[1m'
    END = '\033[0m'

# Header

def header(server):

    titulo = " "*32 + cyan("I", "bold") + color.BOLD + "nsper" + color.END + cyan(" W", "bold") + color.BOLD + "eb" + color.END + cyan(" S", "bold") + color.BOLD + "ervices" + color.END + " "*31

    if server:
        titulo += "|   " + green(server, "bold") + "   "
    else:
        titulo = " "*8 + titulo + " "*8


    print("+" + "-"*98 + "+")
    print("|" + titulo + "|")
    print("+" + "-"*98 + "+")
    print("")

# Abrir arquivo
def open_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)
            
# Limpar o terminal
def clear_terminal(server = None):
    os.system('cls' if os.name == 'nt' else 'clear')
    header(server)

# Mudança de estado
def change_state(states, new_state, server = None):
    clear_terminal(server)
    for state in states.keys():
        states[state] = False
    states[new_state] = True

# Loading bar
def loading_bar():
    t = random.randint(7,14)
    bar = [
        " [=     ]",
        " [ =    ]",
        " [  =   ]",
        " [   =  ]",
        " [    = ]",
        " [     =]",
        " [    = ]",
        " [   =  ]",
        " [  =   ]",
        " [ =    ]",
    ]

    for i in range(t):
        print(bar[i % len(bar)], end="\r")
        time.sleep(.1)

# Print da tabela
def print_table(data):
    print(tabulate(data, headers='firstrow', tablefmt='rounded_outline'))

# Print bold
def bold(msg):
    return f"\033[1m{msg}\033[0m"

def resume_new_instace(new_instance_props, sec_group):
    print("Resumo da nova instância:\n")
    print(bold("Nome: ") + new_instance_props["name"])
    print(bold("Imagem: ") + new_instance_props["image"])
    print(bold("Tipo: ") + new_instance_props["type"])
    print(bold("Tags: ") + new_instance_props["tags"])
    print(bold("Grupos de segurança: ") + ", ".join(sec_group))
    print("")

def resume_new_security_group(new_security_group_props):
    print("Resumo do novo grupo de segurança:\n")
    print(bold("Nome: ") + new_security_group_props["name"])
    print(bold("Descrição: ") + new_security_group_props["description"])
    print(bold("Tags: ") + new_security_group_props["tags"])

    security_groups_data = [['PORTA ENTRADA', 'PORTA SAÍDA', 'PROTOCOLO', 'Blocos CIDR']]
    for ingress in new_security_group_props["ingress_list"]:
        security_groups_data.append([
            ingress["from_port"],
            ingress["to_port"],
            ingress["protocol"],
            "; ".join(ingress["cidr_blocks"])
        ])
    print_table(security_groups_data)

    print("")


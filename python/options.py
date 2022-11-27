import inquirer
import re

server_options = [
    inquirer.List(
        "server",
        message="Selecione um servidor",
        choices=["sa-east-1 (São Paulo)", "us-east-1 (Norte da Virgínia)", "us-east-2 (Ohio)", "us-west-1 (Norte da Califórnia)", "us-west-2 (Oregon)"],
    ),
]

menu_options = [
    inquirer.List(
        "main_menu",
        message="Selecione uma opção",
        choices=["Instâncias EC2", "Usuários", "Grupos de segurança", "Alterar localização", "Sair"],
    ),
]

instance_options = [
    inquirer.List(
        "instance_menu",
        message="Você deseja",
        choices=["Criar uma nova instância", "Listar instâncias", "Deletar uma instância", "Voltar"],
    ),
]

back_options = [
    inquirer.List(
        "go_back",
        message="Para voltar pressione enter",
        choices=["Voltar"],
    ),
]

new_instance_options = [
    inquirer.Text('name', message="Nome da instância"),
    inquirer.List(
        "image",
        message="Imagem da instância",
        choices=["18.04 LTS", "20.04 LTS", "22.04 LTS"],
    ),
    inquirer.List(
        "type",
        message="Tipo de instância",
        choices=["t2.nano", "t2.micro", "t2.small", "t2.medium", "t2.large", "t2.xlarge", "t2.2xlarge"],
    ),
    inquirer.Text('tags', message="Tags da instância (separadas por vírgula)"),
    inquirer.List(
        "confirm",
        message="Confirmar dados",
        choices=["Confirmar", "Refazer"],
    ),
]

confirm_options = [
    inquirer.List(
        "confirm",
        message="Para confirmar pressione enter",
        choices=["Confirmar"],
    ),
]

delete_instance_options = [
    inquirer.List(
        "confirm",
        message="Para confirmar pressione enter",
        choices=["Confirmar"],
    ),
]

security_groups_menu_options = [
    inquirer.List(
        "security_groups_menu",
        message="Você deseja",
        choices=["Criar um novo grupo de segurança", 
                 "Listar grupos de segurança", 
                 "Deletar um grupo de segurança", 
                 "Editar um grupo de segurança", 
                 "Voltar"],
    ),
]

new_security_group_options = [
    inquirer.Text('name', message="Nome"),
    inquirer.Text('description', message="Descrição"),
    inquirer.Text('tags', message="Tags da instância (separadas por vírgula)"),
    inquirer.List(
        "add_ingress",
        message="Adicionar regra de ingresso",
        choices=["Sim"],
    ),
]

new_ingress_rule_options = [
    inquirer.Text('from_port', message="Porta de entrada", validate=lambda _, x: re.match('^([0-9][0-9]{0,2}|1000)$', x)),
    inquirer.Text('to_port', message="Porta de saída", validate=lambda _, x: re.match('^([0-9][0-9]{0,2}|1000)$', x)),
    inquirer.Text('protocol', message="Protocolo"),
    inquirer.Text('cidr_blocks', message="Blocos CIDR (separados por vírgula). Ex.: 0.0.0.0/16"),
    inquirer.List(
        "confirm",
        message="Confirmar dados",
        choices=["Confirmar", "Refazer"],
    ),
]

add_new_rule_options = [
    inquirer.List(
        "add_new_rule",
        message="Adicionar nova regra",
        choices=["Sim", "Não"],
    ),
]

security_group_confirm_options = [
    inquirer.List(
        "confirm",
        message="Confirmar dados",
        choices=["Confirmar", "Refazer"],
    ),
]

edit_security_group_options = [
    inquirer.List(
        "option",
        message="Selecione uma opção",
        choices=["Adicionar regra", "Remover regra", "Voltar"],
    ),
]

users_options = [
    inquirer.List(
        "option",
        message="Selecione uma opção",
        choices=["Criar um novo usuário", 
                 "Listar usuários", 
                 "Deletar um usuário",
                 "Voltar"],
    ),
]

create_user_options = [
    inquirer.Text('name', message="Nome", validate=lambda _, x: re.match('^\S+\w{0,32}', x)),
    inquirer.Text('restriction_name', message="Nome da restrição", validate=lambda _, x: re.match('^\S+\w{0,32}', x)),
    inquirer.Text('restriction_description', message="Descrição"),
    inquirer.Text('restriction_actions', message="Ações"),
    inquirer.Text('restriction_resources', message="Recursos"),
    inquirer.List(
        "confirm",
        message="Confirmar dados",
        choices=["Confirmar", 
                 "Refazer"],
    ),
]
from aux_funcs import *
from terraform import *
from simple_colors import *
import inquirer
import options
from inquirer.themes import GreenPassion

# Carregando arquivos
amis = open_file('../configs/ami.json')

# Config
server = None

# Máquina de estados
states = {
    "SELECT_SERVER": True,
    "MAIN_MENU": False,
    "INSTANCES": False,
    "SHOW_INSTANCES": False,
    "CREATE_INSTANCE": False,
    "DELETE_INSTANCE": False,
    "SECURITY_GROUPS": False,
    "SHOW_SECURITY_GROUPS": False,
    "CREATE_SECURITY_GROUP": False,
    "DELETE_SECURITY_GROUP": False,
    "EDIT_SECURITY_GROUP": False,
    "USERS": False,
    "SHOW_USERS": False,
    "CREATE_USER": False,
    "DELETE_USER": False,
}

header(None)

# Init servers folders
init_folders()
clear_terminal()

# Loop principal
while True:

    if states["SELECT_SERVER"]:

        answers = inquirer.prompt(options.server_options, theme=GreenPassion())
        server = answers["server"].split()[0]

        terraform = TerraformInfrastructure(server)

        change_state(states, new_state = "MAIN_MENU", server = server)

    if states["MAIN_MENU"]:

        answer = inquirer.prompt(options.menu_options, theme=GreenPassion())["main_menu"]

        if answer == "Instâncias EC2":
            change_state(states, new_state = "INSTANCES", server = server)

        elif answer == "Usuários":
            change_state(states, new_state = "USERS", server = server)
        
        elif answer == "Grupos de segurança":
            change_state(states, new_state = "SECURITY_GROUPS", server = server)
            
        elif answer == "Alterar localização":
            server = None
            change_state(states, new_state = "SELECT_SERVER", server = server)
        
        elif answer == "Sair":
            break

#====================================================================================================
#|                                         INSTÂNCIAS                                               |
#====================================================================================================

    if states["INSTANCES"]:

        answer = inquirer.prompt(options.instance_options, theme=GreenPassion())["instance_menu"]

        if answer == "Criar uma nova instância":
            change_state(states, new_state = "CREATE_INSTANCE", server = server)

        elif answer == "Listar instâncias":
            change_state(states, new_state = "SHOW_INSTANCES", server = server)

        elif answer == "Deletar uma instância":
            change_state(states, new_state = "DELETE_INSTANCE", server = server)
        
        elif answer == "Voltar":
            change_state(states, new_state = "MAIN_MENU", server = server)

    if states["SHOW_INSTANCES"]:

        instances_data = [[f"{'NOME': <15}", f"{'UBUNTU': <15}", f"{'TIPO': <15}", f"{'TAGS': <15}", f"{'GRUPO DE SEGURANÇA': <15}"]]
        for instance in terraform.instances:
            instances_data.append([
                instance.name,
                instance.image,
                instance.type,
                ", ".join(instance.tags),
                ", ".join(instance.security_groups)
            ])
        print_table(instances_data)

        print("")
        answer = inquirer.prompt(options.back_options, theme=GreenPassion())["go_back"]

        change_state(states, new_state = "INSTANCES", server = server)

    if states["CREATE_INSTANCE"]:

        while True:
            answers = inquirer.prompt(options.new_instance_options, theme=GreenPassion())
            clear_terminal(server)

            for security_group in terraform.security_groups:
                print(f"{security_group.name} - {security_group.description}")

                security_groups_data = [['PORTA ENTRADA', 'PORTA SAÍDA', 'PROTOCOLO', 'Blocos CIDR']]
                for ingress in security_group.ingress_list:
                    security_groups_data.append([
                        ingress["from_port"],
                        ingress["to_port"],
                        ingress["protocol"],
                        "; ".join(ingress["cidr_blocks"])
                    ])
                print_table(security_groups_data)

            print("")
            print(red("Pressione BARRA DE ESPAÇO para selecionar os grupos de segurança e ENTER para confirmar\n"))

            choices = [security_group.name for security_group in terraform.security_groups]
            answer_sec_group = inquirer.prompt([    
                inquirer.Checkbox(
                    "select_security_groups",
                    message="Selecione o(s) grupo(s) de segurança",
                    choices=choices,
                )
            ,], theme=GreenPassion())["select_security_groups"]
            
            if answers["confirm"] == "Confirmar":
                break
        
        clear_terminal(server)
        resume_new_instace(answers, answer_sec_group)
        answer = inquirer.prompt(options.confirm_options, theme=GreenPassion())["confirm"]

        instance_ami = amis[server][answers["image"]]
        
        terraform.create_instance(answers["name"], answers["type"], answers["image"], instance_ami, answers["tags"], answer_sec_group)
        clear_terminal(server)
        terraform.save()

        change_state(states, new_state = "INSTANCES", server = server)

    if states["DELETE_INSTANCE"]:

        instances_data = [[f"{'NOME': <15}", f"{'UBUNTU': <15}", f"{'TIPO': <15}", f"{'TAGS': <15}"]]
        for instance in terraform.instances:
            instances_data.append([
                instance.name,
                instance.image,
                instance.type,
                ", ".join(instance.tags)
            ])
        print_table(instances_data)

        print("")
        choices = [instance.name for instance in terraform.instances]
        choices.append("Voltar")
        answer = inquirer.prompt([    
            inquirer.List(
                "instance_to_delete",
                message="Selecione a instância que deseja deletar",
                choices=choices,
            )
        ,], theme=GreenPassion())

        if answer["instance_to_delete"] == "Voltar":
            change_state(states, new_state = "INSTANCES", server = server)
            continue 

        terraform.delete_instance(answer["instance_to_delete"])
        clear_terminal(server)
        terraform.save()

        change_state(states, new_state = "INSTANCES", server = server)

#====================================================================================================
#|                                  GRUPOS DE SEGURANÇA                                             |
#====================================================================================================

    if states["SECURITY_GROUPS"]:

        answer = inquirer.prompt(options.security_groups_menu_options, theme=GreenPassion())["security_groups_menu"]

        if answer == "Criar um novo grupo de segurança":
            change_state(states, new_state = "CREATE_SECURITY_GROUP", server = server)

        elif answer == "Listar grupos de segurança":
            change_state(states, new_state = "SHOW_SECURITY_GROUPS", server = server)
        
        elif answer == "Deletar um grupo de segurança":
            change_state(states, new_state = "DELETE_SECURITY_GROUP", server = server)

        elif answer == "Editar um grupo de segurança":
            change_state(states, new_state = "EDIT_SECURITY_GROUP", server = server)
        
        elif answer == "Voltar":
            change_state(states, new_state = "MAIN_MENU", server = server)

    if states["SHOW_SECURITY_GROUPS"]:

        for security_group in terraform.security_groups:
            print(f"{security_group.name} - {security_group.description}")

            security_groups_data = [['PORTA ENTRADA', 'PORTA SAÍDA', 'PROTOCOLO', 'Blocos CIDR']]
            for ingress in security_group.ingress_list:
                security_groups_data.append([
                    ingress["from_port"],
                    ingress["to_port"],
                    ingress["protocol"],
                    "; ".join(ingress["cidr_blocks"])
                ])
            print_table(security_groups_data)

            print("")
        
        answer = inquirer.prompt(options.back_options, theme=GreenPassion())["go_back"]

        change_state(states, new_state = "SECURITY_GROUPS", server=server)

    if states["CREATE_SECURITY_GROUP"]:
        
        while True:
            answers = inquirer.prompt(options.new_security_group_options, theme=GreenPassion())
            new_sec_group = {
                "name": answers["name"],
                "description": answers["description"],
                "tags": answers["tags"],
            }
            ingress_rules = []

            while True:
                clear_terminal(server)
                ingress = inquirer.prompt(options.new_ingress_rule_options, theme=GreenPassion())
                if ingress["confirm"] == "Confirmar":
                    ingress_rules.append({
                        "from_port": ingress["from_port"],
                        "to_port": ingress["to_port"],
                        "protocol": ingress["protocol"],
                        "cidr_blocks": ingress["cidr_blocks"].split(",")
                    })

                    answer = inquirer.prompt(options.add_new_rule_options, theme=GreenPassion())

                    if answer["add_new_rule"] == "Não":
                        break
                    

                else:
                    clear_terminal(server)

            new_sec_group["ingress_list"] = ingress_rules
            clear_terminal(server)
            resume_new_security_group(new_sec_group)
            answer = inquirer.prompt(options.security_group_confirm_options, theme=GreenPassion())
            if answer["confirm"] == "Confirmar":
                break

        terraform.create_security_group(answers["name"], answers["description"], ingress_rules, answers["tags"])
        clear_terminal(server)
        terraform.save()

        change_state(states, new_state = "SECURITY_GROUPS", server = server)

    if states["DELETE_SECURITY_GROUP"]:
            
        for security_group in terraform.security_groups:
            print(f"{security_group.name} - {security_group.description}")

            security_groups_data = [['PORTA ENTRADA', 'PORTA SAÍDA', 'PROTOCOLO', 'Blocos CIDR']]
            for ingress in security_group.ingress_list:
                security_groups_data.append([
                    ingress["from_port"],
                    ingress["to_port"],
                    ingress["protocol"],
                    "; ".join(ingress["cidr_blocks"])
                ])
            print_table(security_groups_data)
    
        print("")
        choices = [security_group.name for security_group in terraform.security_groups]
        choices.append("Voltar")
        security_group_to_delete = inquirer.prompt([    
            inquirer.List(
                "security_group_to_delete",
                message="Selecione o grupo de segurança que deseja deletar",
                choices=choices,
            )
        ,], theme=GreenPassion())["security_group_to_delete"]

        if security_group_to_delete == "Voltar":
            change_state(states, new_state = "SECURITY_GROUPS", server = server)
            continue

        if terraform.verify_if_security_group_is_used(security_group_to_delete):

            clear_terminal(server)

            print(red("O grupo de segurança está sendo usado por uma ou mais instâncias\n"))
            answer = inquirer.prompt([    
                inquirer.List(
                    "delete_how",
                    message="O que deseja fazer",
                    choices=["Deletar o grupo de segurança e as instâncias que o utilizam", 
                             "Cancelar"],
                )
            ,], theme=GreenPassion())["delete_how"]

            if answer == "Cancelar":
                change_state(states, new_state = "SECURITY_GROUPS", server = server)
                continue

            elif answer == "Deletar o grupo de segurança e as instâncias que o utilizam":
                terraform.delete_instances_with_security_group(security_group_to_delete)

        terraform.delete_security_group(security_group_to_delete)
        clear_terminal(server)
        terraform.save()

        change_state(states, new_state = "SECURITY_GROUPS", server = server)

    if states["EDIT_SECURITY_GROUP"]:
        
        clear_terminal(server)
        for security_group in terraform.security_groups:
            print(f"{security_group.name} - {security_group.description}")

            security_groups_data = [['PORTA ENTRADA', 'PORTA SAÍDA', 'PROTOCOLO', 'Blocos CIDR']]
            for ingress in security_group.ingress_list:
                security_groups_data.append([
                    ingress["from_port"],
                    ingress["to_port"],
                    ingress["protocol"],
                    "; ".join(ingress["cidr_blocks"])
                ])
            print_table(security_groups_data)
    
        print("")
        choices = [security_group.name for security_group in terraform.security_groups]
        choices.append("Voltar")
        answer = inquirer.prompt([    
            inquirer.List(
                "security_group_to_edit",
                message="Selecione o grupo de segurança que deseja editar",
                choices=choices,
            )
        ,], theme=GreenPassion())

        security_group_to_edit = answer["security_group_to_edit"]
        if answer["security_group_to_edit"] == "Voltar":
            change_state(states, new_state = "SECURITY_GROUPS", server=server)

        else:
            clear_terminal(server)
            for security_group in terraform.security_groups:
                if security_group.name == answer["security_group_to_edit"]:
                    print(f"{security_group.name} - {security_group.description}")

                    security_groups_data = [['PORTA ENTRADA', 'PORTA SAÍDA', 'PROTOCOLO', 'Blocos CIDR']]
                    for ingress in security_group.ingress_list:
                        security_groups_data.append([
                            ingress["from_port"],
                            ingress["to_port"],
                            ingress["protocol"],
                            "; ".join(ingress["cidr_blocks"])
                        ])
                    print_table(security_groups_data)

            answer = inquirer.prompt(options.edit_security_group_options, theme=GreenPassion())['option']

            if answer == "Voltar":
                clear_terminal(server)

            elif answer == "Adicionar regra":
                while True:
                    ingress = inquirer.prompt(options.new_ingress_rule_options, theme=GreenPassion())
                    if ingress["confirm"] == "Confirmar":                        
                        terraform.add_ingress_rule(security_group_to_edit, ingress["from_port"], ingress["to_port"], ingress["protocol"], ingress["cidr_blocks"].split(","))
                        clear_terminal(server)
                        terraform.save()
                        break
            
            elif answer == "Remover regra":
                clear_terminal(server)

                security_group = terraform.get_security_group(security_group_to_edit)
                choices = []
                print(f"{security_group.name} - {security_group.description}")
                security_groups_data = [['ID', 'PORTA ENTRADA', 'PORTA SAÍDA', 'PROTOCOLO', 'Blocos CIDR']]
                i = 0
                for ingress in security_group.ingress_list:
                    security_groups_data.append([
                        i,
                        ingress["from_port"],
                        ingress["to_port"],
                        ingress["protocol"],
                        "; ".join(ingress["cidr_blocks"])
                    ])
                    i+=1
                print_table(security_groups_data)
                
                print("")

                choices = list(range(len(security_group.ingress_list)))
                choices.append("Voltar")

                answer = inquirer.prompt([    
                    inquirer.List(
                        "security_group_to_remove",
                        message="Selecione a regra que deseja remover",
                        choices=choices,
                    )
                ,], theme=GreenPassion())["security_group_to_remove"]

                terraform.remove_rule_by_index(security_group_to_edit, int(answer))
                clear_terminal(server)
                terraform.save()

                if answer == "Voltar":
                    continue


#====================================================================================================
#|                                          USUÁRIOS                                                |
#====================================================================================================

    if states["USERS"]:
        answer = inquirer.prompt(options.users_options, theme=GreenPassion())["option"]

        if answer == "Criar um novo usuário":
            change_state(states, new_state = "CREATE_USER", server = server)

        if answer == "Listar usuários":
            change_state(states, new_state = "SHOW_USERS", server = server)
        
        elif answer == "Deletar um usuário":
            change_state(states, new_state = "DELETE_USER", server = server)
        
        elif answer == "Voltar":
            change_state(states, new_state = "MAIN_MENU", server = server)

    if states["SHOW_USERS"]:

        users_data = [['NOME DE USUÁRIO', "NOME DA RESTRIÇÃO", 'DESCRIÇÂO DA RESTRIÇÃO', 'AÇÕES', 'RECURSOS']]

        for user in terraform.users:
            users_data.append([
                user.name,
                user.restriction["name"],
                user.restriction["description"],
                ", ".join(user.restriction["actions"]),
                ", ".join(user.restriction["resources"])
            ])

        print_table(users_data)
        print("")
        
        answer = inquirer.prompt(options.back_options, theme=GreenPassion())["go_back"]

        change_state(states, new_state = "USERS", server=server)

    if states["CREATE_USER"]:

        while True:
            answer = inquirer.prompt(options.create_user_options, theme=GreenPassion())

            restriction = {
                "name": answer["restriction_name"],
                "description": answer["restriction_description"],
                "actions": answer["restriction_actions"].split(","),
                "resources": answer["restriction_resources"].split(",")
            }

            if answer["confirm"] == "Confirmar":
                terraform.create_user(answer["name"], restriction)
                clear_terminal(server)
                terraform.save()
                break

        change_state(states, new_state = "USERS", server=server)

    if states["DELETE_USER"]:

        users_data = [['NOME DE USUÁRIO', "NOME DA RESTRIÇÃO", 'DESCRIÇÂO DA RESTRIÇÃO', 'AÇÕES', 'RECURSOS']]

        for user in terraform.users:
            users_data.append([
                user.name,
                user.restriction["name"],
                user.restriction["description"],
                ", ".join(user.restriction["actions"]),
                ", ".join(user.restriction["resources"])
            ])

        print_table(users_data)
        print("")

        choices = []
        for user in terraform.users:
            choices.append(user.name)
        choices.append("Voltar")
        answer = inquirer.prompt([    
            inquirer.List(
                "user_to_delete",
                message="Selecione o usuário que deseja deletar",
                choices=choices,
            )
        ,], theme=GreenPassion())

        if answer["user_to_delete"] == "Voltar":
            change_state(states, new_state = "USERS", server=server)

        else:
            terraform.delete_user(answer["user_to_delete"])
            clear_terminal(server)
            terraform.save()
            change_state(states, new_state = "USERS", server=server)


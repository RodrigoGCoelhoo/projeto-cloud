import json
import os
import subprocess
import time
from simple_colors import *

os.chdir('..')
root = os.getcwd()
os.chdir('python')

class Instance():

    def __init__(self, name, itype, image, ami, tags, security_groups):
        # count, security_groups, key_name, user_data
        self.name = name
        self.type = itype
        self.image = image
        self.ami = ami
        self.tags = tags
        self.security_groups = security_groups
        # self.key_name = None
        # self.user_data = None

class SecurityGroup():

    def __init__(self, name, description, ingress_list, tags):
        self.name = name
        self.description = description
        self.ingress_list = ingress_list
        self.tags = tags

class User():

    def __init__(self, name, restriction):
        self.name = name
        self.restriction = restriction

class TerraformInfrastructure():

    def __init__(self, server):
        self.instances = []
        self.security_groups = []
        self.users = []
        self.server = server

        with open(f'{root}/servers/{server}/.auto.tfvars.json') as file:
            self.file = json.load(file)

        for instance in self.file["instances"]:
            new_instance = Instance(
                instance["name"],
                instance["type"],
                instance["image"],
                instance["ami"],
                instance["tags"],
                instance["security_groups"]
            )
            self.instances.append(new_instance)

        for security_group in self.file["security_groups"]:
            new_security_group = SecurityGroup(
                security_group["name"],
                security_group["description"],
                security_group["ingress"],
                security_group["tags"]
            )
            self.security_groups.append(new_security_group)

        for user in self.file["users"]:
            new_user = User(
                user["name"],
                user["restriction"],
            )
            self.users.append(new_user)


    def create_instance(self, name, itype, image, ami, tags, security_groups):
        new_instance = Instance(
            name,
            itype,
            image,
            ami,
            tags.split(","),
            security_groups
        )
        self.instances.append(new_instance)

    def delete_instance(self, name):
        for instance in self.instances:
            if instance.name == name:
                self.instances.remove(instance)
                break

    def create_security_group(self, name, description, ingress, tags):
        new_security_group = SecurityGroup(
            name,
            description,
            ingress,
            tags.split(",")
        )
        self.security_groups.append(new_security_group)

    def delete_security_group(self, name):
        for security_group in self.security_groups:
            if security_group.name == name:
                self.security_groups.remove(security_group)
                break

    def verify_if_security_group_is_used(self, name):
        for instance in self.instances:
            if name in instance.security_groups:
                return True
        return False

    def delete_instances_with_security_group(self, name):
        for instance in self.instances:
            if name in instance.security_groups:
                self.delete_instance(instance.name)

    def add_ingress_rule(self, name, from_port, to_port, protocol, cidr_blocks):
        for security_group in self.security_groups:
            if security_group.name == name:
                security_group.ingress_list.append({
                    "from_port": from_port,
                    "to_port": to_port,
                    "protocol": protocol,
                    "cidr_blocks": cidr_blocks
                })
                break

    def get_security_group(self, name):
        for security_group in self.security_groups:
            if security_group.name == name:
                return security_group

    def remove_rule_by_index(self, name, index):
        for security_group in self.security_groups:
            if security_group.name == name:
                del security_group.ingress_list[index]
                break

    def create_user(self, name, restriction):
        new_user = User(
            name,
            restriction
        )
        self.users.append(new_user)

    def delete_user(self, name):
        for user in self.users:
            if user.name == name:
                self.users.remove(user)
                break

    def save(self):
        # Instances

        list_instaces = []
        for instance in self.instances:
            list_instaces.append({
                "name": instance.name,
                "image": instance.image,
                "ami": instance.ami,
                "type": instance.type,
                "tags": instance.tags,
                "security_groups": instance.security_groups
            })

        self.file["instances"] = list_instaces

        list_security_groups = []
        for security_group in self.security_groups:

            list_ingress = []
            for ingress in security_group.ingress_list:
                list_ingress.append({
                    "from_port": ingress["from_port"],
                    "to_port": ingress["to_port"],
                    "protocol": ingress["protocol"],
                    "cidr_blocks": ingress["cidr_blocks"]
                })

            list_security_groups.append({
                "name": security_group.name,
                "description": security_group.description,
                "ingress": list_ingress,
                "tags": security_group.tags
            })

        self.file["security_groups"] = list_security_groups

        users = []
        for user in self.users:
            users.append({
                "name": user.name,
                "restriction": user.restriction
            })

        self.file["users"] = users


        with open(f'{root}/servers/{self.server}/.auto.tfvars.json', 'w') as file:
            json.dump(self.file, file, indent=2, separators=(',',': '))

        self.apply()

    
    def apply(self):
        os.chdir(f'{root}/servers/{self.server}')
        process = subprocess.Popen(['terraform apply -auto-approve'],stdout = subprocess.PIPE, stderr = subprocess.DEVNULL, shell = True)
        completed = False
        
        bar = [
            30*" " + "Aplicando alteração na nuvem ⢿",
            30*" " + "Aplicando alteração na nuvem ⣻",
            30*" " + "Aplicando alteração na nuvem ⣽",
            30*" " + "Aplicando alteração na nuvem ⣾",
            30*" " + "Aplicando alteração na nuvem ⣷",
            30*" " + "Aplicando alteração na nuvem ⣯",
            30*" " + "Aplicando alteração na nuvem ⣟",
            30*" " + "Aplicando alteração na nuvem ⡿",
        ]

        i = 0
        while not completed:
            print(f"\033[1m{bar[i % len(bar)]}\033[0m", end="\r")
            time.sleep(.1)
            if process.poll() is not None:
                completed = True
            i += 1

        print(green(30*" " + "Alteração aplicada com sucesso!                   ", "bold"))

        time.sleep(2)

        print("communicating")
        process.communicate("k")
        print("communicated")
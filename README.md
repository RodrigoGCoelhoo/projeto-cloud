# Projeto Terraform-AWS

Autor:
Rodrigo Guimarães Coelho

---

Nesse projeto desenvolvemos uma aplicação utilizando Terraform responsável por gerenciar recursos na AWS. A proposta do projeto pode ser encontrada [aqui](https://insper.github.io/computacao-nuvem/projetos/projeto_2022/).

## Como executar o projeto?

1. Instalar dependências:

- [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. Definir as variáveis de ambiente locais para que o programa consiga acessar a AWS. Para isso abra o terminal e execute os comandos abaixo alterando o valor entre áspas pelos valores da sua credencial:

```bash
export AWS_ACCESS_KEY_ID="anaccesskey"
export AWS_SECRET_ACCESS_KEY="asecretkey"
```

## O que é possível fazer com o projeto?

- Criar:

  - Automaticamente VPC e sub-rede
  - Instâncias em mais de uma região e pelo menos 2 tipos de hosts
  - Grupos de segurança e associação com instâncias
  - Usuário
  - Novas regras em grupos de segurança

- Deletar:

  - Instâncias
  - Grupos de segurança
  - Usuários
  - Regras de grupos de segurança

- Listar:
  - Instâncias
  - Usuários
  - Grupos de segurança
  - Regras

## Modo de uso

1. A partir da raiz do projeto, acesse a pasta "python"

```bash
cd python
```

2. Executar o arquivo "main.py"

```bash
python main.py
```

> **Importante:** A primeira execução do programa é lenta pois o programa inicializa o terraform em todas as pastas usadas na aplicação.

## Bibliotecas auxiliares

- [Simple Colors](https://github.com/weaming/simple-colors)
- [Inquirer](https://github.com/magmax/python-inquirer)
- [Tabulate](https://github.com/gregbanks/python-tabulate)

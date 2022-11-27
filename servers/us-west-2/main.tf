terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-2"
}

#====================================================================================================
#|                                             VPC                                                  |
#====================================================================================================

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  instance_tenancy     = "default"

  tags = {
    Name = "VPC"
  }
}

#====================================================================================================
#|                                           SUBREDE                                                |
#====================================================================================================

resource "aws_subnet" "subnet1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"
  map_public_ip_on_launch = true
 
 tags = {
    Name = "subnet"
 }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Public RT"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.public_rt.id
}


#====================================================================================================
#|                                         INSTÂNCIAS                                               |
#====================================================================================================

resource "aws_instance" "app_server" {
  for_each      = {for instance in var.instances : instance.name => instance}
  ami           = each.value.ami
  instance_type = each.value.type
  vpc_security_group_ids = [for security_group_name in each.value.security_groups : aws_security_group.security_group[security_group_name].id]
  subnet_id     = aws_subnet.subnet1.id 

  tags = {
    Name = each.value.name
  }
}

#====================================================================================================
#|                                  GRUPOS DE SEGURANÇA                                             |
#====================================================================================================


resource "aws_security_group" "security_group" {
  for_each     = {for group in var.security_groups : group.name => group}
  name         = each.value.name
  description  = each.value.description
  vpc_id      = aws_vpc.main.id

  dynamic "ingress" {
      for_each = each.value.ingress
      content {
          from_port   = ingress.value.from_port
          to_port     = ingress.value.to_port
          protocol    = ingress.value.protocol
          cidr_blocks = ingress.value.cidr_blocks
          }
      }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = each.value.name
  }
}

#====================================================================================================
#|                                          USUÁRIOS                                                |
#====================================================================================================


resource "aws_iam_user" "iam_user" {
  for_each = { for iam_user in var.users : iam_user.name => iam_user }
  name     = each.value.name
}	

resource "aws_iam_access_key" "iam_access_key" {
  for_each = { for user in var.users : user.name => user }
  user     = aws_iam_user.iam_user[each.value.name].name
}

resource "aws_iam_policy" "ec2_policy" {
  for_each    = { for user in var.users : user.name => user }
  name        = each.value.restriction.name
  description = each.value.restriction.description
  policy      = data.aws_iam_policy_document.ec2_policy[each.value.name].json
}

data "aws_iam_policy_document" "ec2_policy" {
  for_each    = { for user in var.users : user.name => user }
  policy_id   = each.value.name
  statement {
    effect    = "Allow"
    actions   = each.value.restriction.actions
    resources = each.value.restriction.resources
  }
}

resource "aws_iam_user_login_profile" "profile" {
    for_each                = { for user in var.users : user.name => user }
    user                    = aws_iam_user.iam_user[each.value.name].name
    password_reset_required = true
}

resource "aws_iam_user_policy_attachment" "user_policy_attachment" {
  for_each   = { for user in var.users : user.name => user }
  user       = aws_iam_user.iam_user[each.value.name].name
  policy_arn = aws_iam_policy.ec2_policy[each.value.name].arn
}
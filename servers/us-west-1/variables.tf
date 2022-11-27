variable "instances" {
  type = list(object({
    name          = string
    image         = string
    ami           = string
    type          = string
    tags          = list(string)
    security_groups = list(string)
  }))
}

variable "security_groups" {
  type = list(object({
    name          = string
    description   = string

    ingress = list(object({
      from_port        = number
      to_port          = number
      protocol         = string
      cidr_blocks      = list(string)
    }))
    
    tags = list(string)
  }))
}

variable "users" {
  type = list(object({
    name = string
    restriction = object({
      name = string
      description = string
      actions = list(string)
      resources = list(string)
    })
  }))
}
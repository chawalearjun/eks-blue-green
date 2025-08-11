variable "aws_region" {
  type    = string
  default = "us-east-1" # change if needed
}

variable "cluster_name" {
  type    = string
  default = "blue-green-eks"
}

variable "node_type" {
  type    = string
  default = "t3.small"
}

variable "node_count" { default = 1 }

resource "aws_eks_cluster" "demo" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn
  vpc_config {
    subnet_ids = aws_subnet.eks_subnets[*].id
  }
}

data "aws_eks_cluster_auth" "demo" {
  name = aws_eks_cluster.demo.name
}

resource "aws_eks_node_group" "demo_nodes" {
  cluster_name    = aws_eks_cluster.demo.name
  node_group_name = "${var.cluster_name}-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = aws_subnet.eks_subnets[*].id
  scaling_config {
    desired_size = var.node_count
    max_size     = 3
    min_size     = 1
  }
  instance_types = [var.node_type]
}

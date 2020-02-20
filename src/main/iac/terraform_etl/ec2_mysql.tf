resource "aws_instance" "ec2_mysql" {
  count           = 1
  ami             = "ami-759bc50a"
  instance_type   = "t2.medium"
  key_name        = aws_key_pair.mysql_key_pair.key_name
  security_groups = [aws_security_group.mysql.name]
  tags = { Name = "Mysql Server" }
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
    timeout     = "10m"
  }
  provisioner "file" {
    source      = "../../../../docker-compose-mysql-and-mysql-data.yml"
    destination = "/home/ubuntu/docker-compose-mysql-and-mysql-data.yml"
  }
  provisioner "file" {
    source      = "../../../../mysql-data.tar.gz"
    destination = "/home/ubuntu/mysql-data.tar.gz"
  }
  provisioner "file" {
    source      = "../terraform_provisioning_scripts/provision_mysql.sh"
    destination = "/home/ubuntu/provision_mysql.sh"
  }
  provisioner "remote-exec" {
    inline = ["chmod +x /home/ubuntu/provision_mysql.sh"]
  }
  provisioner "remote-exec" {
    inline = ["/home/ubuntu/provision_mysql.sh"]
  }
}

resource "aws_key_pair" "mysql_key_pair" {
  key_name   = "mysql_key_pair"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_security_group" "mysql" {
  name        = "Mysql Security Group"
  description = "Mysql Security Group"
  ingress {
    protocol  = "tcp"
    from_port = 22
    to_port   = 22
    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }
  ingress {
    protocol  = "tcp"
    from_port = 3306
    to_port   = 3306
    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }
  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }
  tags = {
    Name = "Mysql Security Group"
  }
}

output "mysql_dns" {
  value = [aws_instance.ec2_mysql.*.public_dns]
}
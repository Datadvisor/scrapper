provider "aws" {
	profile = "default"
	region 	= "eu-west-3"
}

resource "aws_key_pair" "ssh_vpl-datadvisor-001" {
  key_name   = "ssh_vpl-datadvisor-001"
  public_key = file("~/.ssh/vpl-datadvisor-001.pub")
}

resource "aws_default_vpc" "default" {

}

resource "aws_security_group" "sg_vpl-datadvisor-001" {
	name				= "sg_vpl-datadvisor-001"
	description = "Security Group for vpl-datadvisor-001"

	vpc_id			= aws_default_vpc.default.id

	ingress {
		description = "Allow ssh"

		from_port		= 22
		to_port			= 22
		protocol		= "tcp"

		cidr_blocks = ["0.0.0.0/0"]
	}

	ingress {
		description = "Allow inbound http traffic"

		from_port		= 80
		to_port			= 80
		protocol		= "tcp"

		cidr_blocks = ["0.0.0.0/0"]
  }

 	ingress {
 		description = "Allow inbound https traffic"

 		from_port		= 443
 		to_port			= 443
 		protocol		= "tcp"

 		cidr_blocks = ["0.0.0.0/0"]
 	}

	egress {
		description = "Allow all outbound traffic"

		from_port   = 0
		to_port     = 0
		protocol    = "-1"
		cidr_blocks = ["0.0.0.0/0"]
	}

	tags = {
		Name = "sg_vpl-datadvisor-001"
	}
}

resource "aws_eip" "eip_vpl-datadvisor-001" {
	instance = aws_instance.vpl-datadvisor-001.id
	vpc      = true

	tags = {
		Name = "eip_vpl-datadvisor-001"
	}
}

resource "aws_instance" "vpl-datadvisor-001" {
	ami = "ami-06e03995351444c50" // Debian 11
	instance_type = "t2.medium"

	key_name = aws_key_pair.ssh_vpl-datadvisor-001.id

	root_block_device {
		volume_size = 40
		delete_on_termination = true
	}

	security_groups = [aws_security_group.sg_vpl-datadvisor-001.name]

	tags = {
		Name = "vpl-datadvisor-001"
	}
}

output "public_ip" {
	value = aws_instance.vpl-datadvisor-001.public_ip
}

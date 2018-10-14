provider "aws" {
  region                   = "${var.aws_region}"
  profile                  = "default"
}


data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-16.04-amd64-server-*"]
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "ec2_instance" {
  count                   = 1
  ami                     = "${data.aws_ami.ubuntu.id}"
  availability_zone       = "${var.availability_zone}"
  iam_instance_profile    = "${var.iam_instance_profile}"
  instance_type           = "${var.instance_type}"
  key_name                = "${var.key_name}"
  subnet_id               = "${var.subnet_id}"
  vpc_security_group_ids  = ["${split(",", var.security_groups)}"]
  instance_initiated_shutdown_behavior = "terminate"


  root_block_device = {
    volume_size           = "${var.root_block_device_vol_size}"
  }

   tags = {
      "Name"                = "${var.ec2_name}"
  }

  connection {
    user = "${var.ec2_user}"
    private_key = "${file("~/.ssh/${var.key_name}.pem")}"
  }


  # Sends over script, then run it
  provisioner "file" {
    source = "${var.ec2_user_data}"
    destination = "/tmp/${var.ec2_user_data}"

    connection {
      user = "${var.ec2_user}"
      private_key = "${file("~/.ssh/${var.key_name}.pem")}"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/${var.ec2_user_data}",
      "/tmp/${var.ec2_user_data}"
    ]

    connection {
      user = "${var.ec2_user}"
      private_key = "${file("~/.ssh/${var.key_name}.pem")}"
    }
  }

  provisioner "local-exec" {
    command = "echo ${aws_instance.ec2_instance.private_ip}"
  }
}
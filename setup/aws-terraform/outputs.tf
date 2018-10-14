# This file defines the outputs from launching the EC2 instance module.

output "ec2_public_ip" {
  value = "${aws_instance.ec2_instance.public_ip}"
}

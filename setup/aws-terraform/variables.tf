#AWS
variable "aws_region"                 {default = "us-east-1"}

# Resource Tags
variable "ec2_name"                   {default = "pyspark_vs_dask"}

# Instance details
variable "key_name"                   { default = "default"}
variable "subnet_id"                  { default = "subnet-54f5a631" }
variable "iam_instance_profile"       { default = "EC2-S3-FULL-ACCESS" }
variable "security_groups"            { default = "sg-37b7ee48,sg-839e54f6" }
variable "instance_type"              { default = "r5.xlarge" }
variable "availability_zone"          { default = "us-east-1a" }
variable "ebs_delete_on_termination"  { default = true }
variable "root_block_device_vol_size" { default = 20 }

# bootstrap the ec2 instance
variable "ec2_user"                   { default = "ubuntu" }
variable "ec2_user_data"              { default = "user_data.sh" }
variable "bashrc"                     { default = "bashrc.sh" }
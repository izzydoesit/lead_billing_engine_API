# resource "aws_internet_gateway" "internet_gateway" {}

# resource "aws_ec2_transit_gateway" "transit_gateway" {}

# resource "aws_ec2_transit_gateway_vpc_attachment" "gateway_attachement" {
#   subnet_ids = [
#     aws_subnet.private_subnet_one.id,
#     aws_subnet.private_subnet_two.id,
#     aws_subnet.private_subnet_three.id
#   ]
#   vpc_id             = aws_vpc.vpc.id
#   transit_gateway_id = aws_ec2_transit_gateway.transit_gateway.id
# }

# resource "aws_route_table" "public_route_table" {
#   vpc_id = aws_vpc.vpc.id
# }

# resource "aws_route" "public_route" {
#   route_table_id         = aws_route_table.public_route_table.id
#   destination_cidr_block = "0.0.0.0/0"
#   gateway_id             = aws_internet_gateway.internet_gateway.id
# }

# resource "aws_route_table_association" "public_subnet_one_route_table_association" {
#   subnet_id      = aws_subnet.public_subnet_one.id
#   route_table_id = aws_route_table.public_route_table.id
# }

# resource "aws_route_table_association" "public_subnet_two_route_table_association" {
#   subnet_id      = aws_subnet.public_subnet_two.id
#   route_table_id = aws_route_table.public_route_table.id
# }

# resource "aws_route_table_association" "public_subnet_three_route_table_association" {
#   subnet_id      = aws_subnet.public_subnet_three.id
#   route_table_id = aws_route_table.public_route_table.id
# }

# resource "aws_eip" "nat_gateway_one_attachment" {
#   vpc = true
# }

# resource "aws_eip" "nat_gateway_two_attachment" {
#   vpc = true
# }

# resource "aws_eip" "nat_gateway_three_attachment" {
#   vpc = true
# }

# resource "aws_nat_gateway" "nat_gateway_one" {
#   allocation_id = aws_eip.nat_gateway_one_attachment.allocation_id
#   subnet_id     = aws_subnet.public_subnet_one.id
# }

# resource "aws_nat_gateway" "nat_gateway_two" {
#   allocation_id = aws_eip.nat_gateway_two_attachment.allocation_id
#   subnet_id     = aws_subnet.public_subnet_two.id
# }

# resource "aws_nat_gateway" "nat_gateway_three" {
#   allocation_id = aws_eip.nat_gateway_three_attachment.allocation_id
#   subnet_id     = aws_subnet.public_subnet_three.id
# }

# resource "aws_route_table" "private_route_table_one" {
#   vpc_id = aws_vpc.vpc.id
# }

# resource "aws_route" "private_route_one" {
#   route_table_id         = aws_route_table.private_route_table_one.id
#   destination_cidr_block = "0.0.0.0/0"
#   nat_gateway_id         = aws_nat_gateway.nat_gateway_one.id
# }

# resource "aws_route_table_association" "private_route_table_one_association" {
#   route_table_id = aws_route_table.private_route_table_one.id
#   subnet_id      = aws_subnet.private_subnet_one.id
# }

# resource "aws_route_table" "private_route_table_two" {
#   vpc_id = aws_vpc.vpc.id
# }

# resource "aws_route" "private_route_two" {
#   route_table_id         = aws_route_table.private_route_table_two.id
#   destination_cidr_block = "0.0.0.0/0"
#   nat_gateway_id         = aws_nat_gateway.nat_gateway_two.id
# }

# resource "aws_route_table_association" "private_route_table_two_association" {
#   route_table_id = aws_route_table.private_route_table_two.id
#   subnet_id      = aws_subnet.private_subnet_two.id
# }

# resource "aws_route_table" "private_route_table_three" {
#   vpc_id = aws_vpc.vpc.id
# }

# resource "aws_route" "private_route_three" {
#   route_table_id         = aws_route_table.private_route_table_three.id
#   destination_cidr_block = "0.0.0.0/0"
#   nat_gateway_id         = aws_nat_gateway.nat_gateway_three.id
# }

# resource "aws_route_table_association" "private_route_table_three_association" {
#   route_table_id = aws_route_table.private_route_table_three.id
#   subnet_id      = aws_subnet.private_subnet_three.id
# }

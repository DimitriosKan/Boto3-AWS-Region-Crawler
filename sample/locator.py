import boto3

# this sets the client/resource with the new region name
# that has been cycled in from the region cycle
def client_cycle(current_r):
    ec2_cycle = boto3.client('ec2', region_name=current_r)
    return ec2_cycle

def resource_cycle(current_r):
    ec2_res_cycle = boto3.resource('ec2', region_name=current_r)
    return ec2_res_cycle

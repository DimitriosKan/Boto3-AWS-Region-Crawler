from sample.locator import client_cycle, resource_cycle

'''
EC2 Instances ...
'''
# properties for instances (add display details here)
def describe_instances(ec2_cycle):
    ec2_response = ec2_cycle.describe_instances()

    return ec2_response

# this deletes instance ...
def delete_instance(ec2_res_cycle, inst_id):
    instance = ec2_res_cycle.Instance(inst_id)
    #print (instance)
    #print (inst_id)
    instance.terminate()

    print (f'Deleting instance {inst_id} ...')

'''
VPCs ...
'''
# properties for vpcs (add display details here)
def describe_vpcs(ec2_cycle):
    vpc_response = ec2_cycle.describe_vpcs()
 
    return vpc_response

# this deletes vpc ...
def delete_vpc(ec2_res_cycle, vpc_id):   
    vpc = ec2_res_cycle.Vpc(vpc_id)
    #print (vpc)
    #print (vpc_id)
    vpc.delete()

    print (f'Deleting vpc {vpc_id} ...')

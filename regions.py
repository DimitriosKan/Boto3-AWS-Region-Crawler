import boto3

ec2 = boto3.client('ec2')

# this sets the client with the new region name that has been cycled in from the region cycle
def client_cycle(current_r):
    ec2_cycle = boto3.client('ec2', region_name=current_r)
    return ec2_cycle

# this prinths out the entire list of regions
# and returns the entire list, which allows a simple cycle used in list_things()
def region_cycle():
    cycle_regions = ec2.describe_regions()
    
    # print an 'index' thing at start (independant from functionality)
    for r in cycle_regions['Regions']:
        print (f"{r['RegionName']}")
    print ('\n')

    # return a itterable piece that will be used below
    return cycle_regions

# properties for instances (add display details here)
def describe_instances(ec2_cycle):
    ec2_response = ec2_cycle.describe_instances()

    return ec2_response

# properties for vpcs (add display details here)
def describe_vpcs(ec2_cycle):
    vpc_response = ec2_cycle.describe_vpcs()

    #print (vpc_response)
    #print (vpc_response['Vpcs'])
    #print (ec2_response['Reservations'])
 
    return vpc_response

# this is the one that is supposed to list the things and run commands
# not much to worry about here ...
# the for loop runs thorugh the list received from 'region_cycle()'
def list_things():
    cycle_regions = region_cycle()

    num = 1

    # functional loop to pick current region and send it up to 'client_cycle()'
    for r in cycle_regions['Regions']:
        current_r = r['RegionName']
        ec2_cycle = client_cycle(current_r)

        print (f'{num}: {current_r}')


        # @ @ @ Below we run whatever we wanna do to the region @ @ @
        ec2_response = describe_instances(ec2_cycle)
        vpc_response = describe_vpcs(ec2_cycle)
       

        # Ideas:
        # - add an emailing thing to send you a message if it finds anything exstraordinary in the other regions
        # - auto delete with confirmation ?
        # Edit below > 
        for i in ec2_response['Reservations']:
            #print (i['Instances'])
            for i_id in i['Instances']:
                print (i_id['InstanceId'])
                # fetch the id and run it to a function that does the actions

        # print out everything about VPCs on selected region
        for v in vpc_response['Vpcs']:
            print (v['VpcId'])
            # fetch the id and run it to a function that does the actions

        # block for testing
        input()
        
        num += 1


if __name__ == "__main__":
    list_things()

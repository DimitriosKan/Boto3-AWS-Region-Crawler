import boto3

ec2 = boto3.client('ec2')

# this sets the client/resource with the new region name
# that has been cycled in from the region cycle
def client_cycle(current_r):
    ec2_cycle = boto3.client('ec2', region_name=current_r)
    return ec2_cycle

def resource_cycle(current_r):
    ec2_res_cycle = boto3.resource('ec2', region_name=current_r)
    return ec2_res_cycle

# this prints out the entire list of regions
# and returns the entire list, which allows a simple cycle used in list_things()
def region_cycle():
    cycle_regions = ec2.describe_regions()
    
    # print an 'index' thing at start (independant from functionality)
    for r in cycle_regions['Regions']:
        print (f"{r['RegionName']}")
    print ('\n')

    # return a itterable piece that will be used below
    return cycle_regions
'''
Below is less immediate functionality (so will consider modularizing the next few functions)
Would [possibly] make expanding the thing much easier
 ... but will still need to edit the "confirm" function (unless I send it to a mudule as well)
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

'''
Confirmation of choice
Asks the user if they want to delete the certain element
'''
def confirm(current_r, some_id):
    ec2_res_cycle = resource_cycle(current_r)
    
    # Error check for wrong or unsupported input    
    while True:
        try:
            confirm_check = input ('Do you want to continue? [Y/n]: ')

        except ValueError:
            continue

        # Check user input and run according function for the correct element
        # by checking the id precursor
        if confirm_check == 'Y':
            # print ('Continuing with whatever ...')
            if 'i-' in some_id:
                # print (f'* Deletes the dang {some_id} instance *')
                delete_instance(ec2_res_cycle, some_id)
            if 'vpc-' in some_id:
                # print (f'* Delete the dang {some_id} vpc *')
                delete_vpc(ec2_res_cycle, some_id)
            break
        elif confirm_check == 'n':
            print ('Breaking out ...')
            break

# this is the one that is supposed to list the things and run commands
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
        # Edit below > 
        for i in ec2_response['Reservations']:
            
            # check state of instance
            for s in i['Instances']:
                state = s['State']['Name']

            # run through instances in region and if state is not terminated ...
            # go to confirm()
            for i_id in i['Instances']:
                if state != 'terminated':
                    inst_id = i_id['InstanceId']
                    print (f'{inst_id}: {state}')
                    
                    # Do something with the instance below
                    confirm(current_r, inst_id)
                else:
                    print (f'No active instance(or {state})')            

        # get needed details about VPCs on selected region
        for v in vpc_response['Vpcs']:
            is_default = v['IsDefault']
            vpc_id = v['VpcId']

            # exclude the default vpcs before recommended cleanup
            if is_default is not True:
                print (f'{vpc_id}: Is not default')
            
                # Do something with VPCs below
                confirm(current_r, vpc_id)
            if is_default is True:
                print (f'{vpc_id}: Default')


        # block for testing
        input()
        
        num += 1


if __name__ == "__main__":
    list_things()

import boto3

ec2 = boto3.client('ec2')

def client_cycle(current_r):
    region = region_assign()
    ec2_cycle = boto3.client('ec2', region_name=current_r)
    return ec2_cycle

# should be creating called every time it needs to run thourgh all the availalbe regions
# feel like this one is the issue !!
def region_cycle():
    '''
    # may not be needed
    region = region_assign()
    print (f'damn: {region}')
    ec2_cycle = boto3.client('ec2', region_name=region)
    '''
    # look into below this line (try and get the full list)
    # call it in the 'list_things' function
    # and run through the list there ?
    # will it be saving the state ? Will it be refreshing the lsit it runs though every time it calls this function ? I DONT KNOW ...
    regions = ec2.describe_regions()
    print (regions)
    return regions

    for response in regions['Regions']:
        print (response)
        res = response['RegionName']
        print (f'cycle: {res}')
        return res

# should be the one that assigns the name (used by both the cycle and the list)
def region_assign():
    #ec2 = boto3.client('ec2')
    response = ec2.describe_regions()
    for r in response['Regions']:
        region_as = r['RegionName']
        print (f'assigner: {region_as}')
        return region_as

# this is the one that is supposed to list the things and run commands
# not much to worry about here ...
# the for loop runs thorugh thelist received from 'region_cycle'
def list_things():
    # region = region_assign()
    #ec2_cycle = client_cycle()
    cycle_regions = region_cycle()
    #ec2 = boto3.client('ec2', region_name=region)
    #response = ec2.describe_regions()

    num = 1

    for r in cycle_regions['Regions']:
        current_r = r['RegionName']
        ec2_cycle = client_cycle(current_r)
        #region = region_assign(current_r)
        print (f"loop: {current_r}")
    #for r in response['Regions']:
        # i'll want this to go to the top line and populate region_name=''
        #region = r['RegionName']
        
        # this is local
        print (f'{num}: {current_r}')
        
        ec2_response = ec2_cycle.describe_instances()
        vpc_response = ec2_cycle.describe_vpcs()
        
        #print (vpc_response)
        #print (vpc_response['Vpcs'])
        #print (ec2_response['Reservations'])
        
        # print out everything (currently jsut an indicator) for available instances
        # in region
        for i in ec2_response['Reservations']:
            #print (i['Instances'])
            for i_id in i['Instances']:
                print (i_id['InstanceId'])
        # print out everything about VPCs on selected region
        for v in vpc_response['Vpcs']:
            print (v['VpcId'])
        
        # block for testing
        input()
        
        num += 1
        
    print (num)


if __name__ == "__main__":
    list_things()

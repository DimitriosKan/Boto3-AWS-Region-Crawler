import boto3
import sample.cleanup, sample.confirmation, sample.locator

ec2 = boto3.client('ec2')

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

# this is the one that is supposed to list the things and run commands
# the for loop runs thorugh the list received from 'region_cycle()'
def list_things():
    cycle_regions = region_cycle()

    num = 1

    # functional loop to pick current region and send it up to 'client_cycle()'
    for r in cycle_regions['Regions']:
        current_r = r['RegionName']
        ec2_cycle = sample.locator.client_cycle(current_r)

        print (f'{num}: {current_r}')


        # @ @ @ Below we run whatever we wanna do to the region @ @ @
        ec2_response = sample.cleanup.describe_instances(ec2_cycle)
        vpc_response = sample.cleanup.describe_vpcs(ec2_cycle)
        
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
                    sample.confirmation.confirm(current_r, inst_id)
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
                sample.confirmation.confirm(current_r, vpc_id)
            if is_default is True:
                print (f'{vpc_id}: Default')


        # block for testing
        input()
        
        num += 1


if __name__ == "__main__":
    list_things()

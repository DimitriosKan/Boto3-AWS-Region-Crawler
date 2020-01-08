from sample.locator import resource_cycle
from sample import cleanup

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
                cleanup.delete_instance(ec2_res_cycle, some_id)
            if 'vpc-' in some_id:
                # print (f'* Delete the dang {some_id} vpc *')
                cleanup.delete_vpc(ec2_res_cycle, some_id)
            break
        elif confirm_check == 'n':
            print ('Breaking out ...')
            break

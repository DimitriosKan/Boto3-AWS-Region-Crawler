# Boto3-AWS-Region-Crawler
So the common issue when learning AWS is that you might (somehow) end up with resources in different regions.
This script sorts ALL (not all) your issues.

- Run your standard 'aws configure' to set up credentials
- Run the regions.py file and watch it run
- If anything that is not under it's criteria (not a default vpc or a terminated instance) it will prompt you for confirmation


I will add more checks, or you can do it yourself ...
      
As I'm writing this I thought it might be cool to add an exclude function to allow the user
to input an ID or something that will whitelist the certain service

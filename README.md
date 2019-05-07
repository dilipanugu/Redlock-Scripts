# RedLock_AWS_Account_Onboarding (redlock_aws.py)

This script automates the process of on boarding AWS EH accounts to Redlock. This script is hosted on AWS Lambda and will be run on schedule (12:00 AM EST/Everyday)

1. Gather all Enterpises AWS accounts names and numbers.
2. Gather all the accounts already onboarded on Redlock.
3. Compare 1 and 2 to check if all AWS accounts are present in Redlock.
4. If they are not in RedLock, add those to Redlock

# RedLock_Azure_Account_Onboarding (redlock_azure.py)

This script is run on demand, it gathers the azure subscription name and number from a csv file and automates the addition of Azure accounts to redlock

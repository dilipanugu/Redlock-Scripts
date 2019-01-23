# RedLock_Account_Onboarding

This script automates the process of on boarding AWS EH accounts to Redlock. This script is hosted on AWS Lambda and will be run on schedule (12:00 AM EST/Everyday)

## Logic 

1. Gather all Enterpises AWS accounts names and numbers.
2. Gather all the accounts already onboarded on Redlock.
3. Compare 1 and 2 to check if all AWS accounts are present in Redlock.
4. If they are not in RedLock, add those to Redlock

import requests
import pprint
import json
import re
import os
import boto3
from base64 import b64decode

name_acctnum = {}
eh_accounts_aws = {}
accounts_in_redlock = {}

Headers = {}

Account_Groups = { 
		"AWS FactSet Development":"XYZ",
		"AWS FactSet Production":"XYZ",
		"AWS EH Client Production": "XYZ", 
		"Azure FactSet Production":"XYZ",
		"Azure Open FactSet":"XYZ"
		}		

# Function to login to Redlock and generate an API token 
def redlock_login():

	encrypt_username = os.environ['USERNAME_RL']
	encrypt_password = os.environ['PASSWORD_RL']

	# Decrypt code should run once and variables stored outside of the function
	# handler so that these are decrypted once per container
	decrypt_username = boto3.client('kms').decrypt(CiphertextBlob=b64decode(encrypt_username))['Plaintext']
	decrypt_password = boto3.client('kms').decrypt(CiphertextBlob=b64decode(encrypt_password))['Plaintext']
	
	un = decrypt_username.decode("utf-8")
	pwd = decrypt_password.decode("utf-8")

	url = "https://api.redlock.io/login"

	Headers = {"Content-Type":"application/json"}
	payload = {"username":un,"customerName":"", "password":pwd}
	response = requests.request("POST", url, data=json.dumps(payload), headers=Headers, verify=False)

	return response.json()["token"]
	

# Function to get the account names and numbers from http:/x.y.z/scripts/accounts.json (managed by Cloud team)
def get_account_names_numbers():

	url = "http://x.y.z.x/scripts/accounts.json"
	response = requests.request("GET", url)
	
	for d in response.json():
		name_acctnum[d['Name']] = d['Id']

	for k,v in name_acctnum.items():
		if 'eh-' in str(k):
			eh_accounts_aws.update({k:v})
	#print(eh_accounts_aws)

# Function to add aws accounts to Redlock for monitoring  
def aws_account_addition(name, account_num, groupids):

	url = "https://api.redlock.io/cloud/aws"

	Body = {
		"accountId":account_num, 
		"enabled": "true", 
		"externalId": "abc", 
		"groupIds": [groupids],
		"name": name,
		"roleArn": "arn:aws:iam::" + account_num +":role/redlock-ro-iam-role"
		}

	response = requests.request("POST", url, data=json.dumps(Body), headers=Headers)
	# print(response.status_code)


# Function to view all accounts onboarded on Redlock 
def view_account_in_redlock():
	url = "https://api.redlock.io/cloud/name?onlyActive=true"
	response = requests.request("GET", url, headers=Headers)

	for d in response.json():
		accounts_in_redlock[d['name']] = d['id']
	# print(accounts_in_redlock)	

# Function to view account groups on Redlock 
def view_account_group():
	
	url = "https://api.redlock.io/cloud/group/name"
	response = requests.request("GET", url, headers=Headers)
	
	# print(response.json())
	for d in response.json():
		for k,v in d.items():
			print(k,v)

def lambda_handler(event, context):

	api_key = redlock_login()
	
	# Mandatory headers for RedLock API calls
	global Headers
	Headers = {
		"Content-Type":"application/json", 
		"x-redlock-auth":api_key 
		}

	get_account_names_numbers()
	view_account_in_redlock()

	for x,y in eh_accounts_aws.items():
		if y not in accounts_in_redlock.values():
			aws_account_addition(x, y,"XYZ")

	return {
		'statusCode': 200,
		'body': json.dumps('accounts are added to RedLock')
	}

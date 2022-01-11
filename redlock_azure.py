import requests
import json
import os
import csv

azure_subscriptions = {}
Headers = {}

Account_Groups = { 
		"Azure XYZ":"123456789abc",
		"Azure":"123456789abc"
		}		

# Function to login to Redlock and generate an API token 
def redlock_login():

	username = os.environ['USERNAME_RL']
	password = os.environ['PASSWORD_RL']
	
	url = "https://api.redlock.io/login"

	Headers = {"Content-Type":"application/json"}
	payload = {"username":username,"customerName":"", "password":password}
	response = requests.request("POST", url, data=json.dumps(payload), headers=Headers)

	return response.json()["token"]
	

# Function to get the account names and numbers from a csv file "Azure_accts.csv" with subscription names and numbers (managed by Cloud team)
def get_account_names_numbers_azure():
	
	with open("Azure_accts.csv",'r') as my_file:
		csv_reader = csv.reader(my_file)

		for line in csv_reader:
			azure_subscriptions[line[0]] = line[1]

	#print(azure_subscriptions)

def azure_account_addition(name, account_num, groupids):

	url = "https://api.redlock.io/cloud/azure"

	Body = {
  			"cloudAccount": {
    				"accountId": account_num,
    				"enabled": True,
    				"groupIds": [groupids],
    				"name": name
    				},
  					"clientId": "12345-6789-1233-zzzz-1234567qwerty",
  					"key": "123456789mysecretkey",
  					"monitorFlowLogs": True,
  					"tenantId": "456789-1234-3333-zzzz-qwerty1234567",
  					"servicePrincipalId": "a123456-7777-5555-b777-zzzzzzzzz"
					
			}

	response = requests.request("POST", url, data=json.dumps(Body), headers=Headers)
	print(response.status_code)
	if response.status_code == 200:
		print(name, account_num, "was added Redlock")

def main():
	api_key = redlock_login()
	global Headers
	Headers = {
		"Content-Type":"application/json", 
		"x-redlock-auth":api_key 
		}
	#print(api_key)
	get_account_names_numbers_azure()

	for x,y in azure_subscriptions.items():
		azure_account_addition(x, y, "123456789abc")
			
main()



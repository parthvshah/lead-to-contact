'''
Run the script. It will initially ask you for the Intercom and HubSpot keys.
Set skip_setup to True if you wish to continue with default values.
'''
import requests
import json

skip_setup = True

intercom_access_token = ''
hubspot_api_key = ''

# Setup
if(skip_setup == False):
    print("Welcome to the Lead-to-Contact Script. You are now setting up Intercom and HubSpot.")
    intercom_access_token = input("Enter your extended scope access token from Intercom: ")
    hubspot_api_key = input("Enter your HubSpot HAPI-Key: ")
    print("Setup completed. Running...")

# Intercom Query
headers = {
    'Authorization': 'Bearer '+intercom_access_token,
    'Accept': 'application/json',
}
url = 'https://api.intercom.io/contacts/'
response = requests.get(url, headers=headers)
intercomData = response.json()
print("Total Number of Leads: ", intercomData['total_count'])

# Iterating through the leads
for lead in intercomData['contacts']:
    # Enable to display the received lead
    # print("Lead: ", lead)

    # HubSpot works with email field as primary key
    if(lead['email'] != None):
        url = 'https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/'+ lead['email'] +'/?hapikey='+hubspot_api_key
        formattedData = []

        # Checks for availability of data
        if(lead['phone'] == None):
            formattedData.append("")
        else:
            formattedData.append(lead['phone'])

        if (lead['name'] == None):
            formattedData.append("")
            formattedData.append("")
        else:
            formattedData.append(lead['name'].split(' ')[0])
            formattedData.append(lead['name'].split(' ')[1])

        try:
            companyName = lead['companies']['companies'][0]['name']
        except IndexError:
            companyName = ""
        finally:
            formattedData.append(companyName)

        if(lead['location_data']['country_name'] == None):
            formattedData.append("")
        else:
            formattedData.append(lead['location_data']['country_name'])

        if (lead['location_data']['region_name'] == None):
            formattedData.append("")
        else:
            formattedData.append(lead['location_data']['region_name'])

        if (lead['location_data']['city_name'] == None):
            formattedData.append("")
        else:
            formattedData.append(lead['location_data']['city_name'])

        if (lead['location_data']['postal_code'] == None):
            formattedData.append("")
        else:
            formattedData.append(lead['location_data']['postal_code'])

        print("Formatted Data: ", formattedData)
        data = {
            "properties": [
                {
                    "property": "phone",
                    "value": formattedData[0]
                },
                {
                    "property": "firstname",
                    "value": formattedData[1]
                },
                {
                    "property": "lastname",
                    "value": formattedData[2]
                },
                {
                    "property": "company",
                    "value": formattedData[3]
                },
                {
                    "property": "country",
                    "value": formattedData[4]
                },
                {
                    "property": "state",
                    "value": formattedData[5]
                },
                {
                    "property": "city",
                    "value": formattedData[6]
                },
                {
                    "property": "zip",
                    "value": formattedData[7]
                }
            ]
        }

        # HubSpot Updating Query
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Response Code: ", response.status_code)
        print("Response: ", response.text)

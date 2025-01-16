import os
import pickle
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import vobject

# The scope needed to access contacts
SCOPES = ['https://www.googleapis.com/auth/contacts']

# Path to the credentials file you downloaded from Google Cloud
CREDS_FILE = 'credentials.json'

# Path to the dummy vCard file you want to upload
VCF_FILE = 'dummy_contact2.vcf'

# Authenticate and get credentials
def authenticate():
    creds = None
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

# Function to create a contact from a vCard
def create_contact_from_vcard(vcard_data, service):
    # Parse the vCard data using vobject library
    vcard = vobject.readOne(vcard_data)

    # Extract contact details (name, email, phone)
    name = vcard.fn.value if vcard.fn else 'Unknown'
    email = vcard.email.value if vcard.email else ''
    phone = vcard.tel.value if vcard.tel else ''

    # Create a new contact in Google People API
    contact = {
        'names': [{'givenName': name}],
        'emailAddresses': [{'value': email}],
        'phoneNumbers': [{'value': phone}],
    }

    # Upload the contact using Google People API
    result = service.people().createContact(body=contact).execute()

    print(f"Contact created: {result['names'][0]['displayName']}")

# Main function
def main():
    # Read the vCard data from the file
    with open(VCF_FILE, 'r') as vcard_file:
        vcard_data = vcard_file.read()

    # Authenticate and get the API service
    creds = authenticate()
    service = build('people', 'v1', credentials=creds)

    # Create the contact from vCard and upload it
    create_contact_from_vcard(vcard_data, service)

if __name__ == '__main__':
    main()

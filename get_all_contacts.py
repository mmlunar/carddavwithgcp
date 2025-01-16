import os
import pickle
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# The scope needed to access contacts
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

# Path to the credentials file you downloaded from Google Cloud
CREDS_FILE = 'credentials.json'

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

# Function to get all contacts, handling pagination
def get_all_contacts(service):
    connections = []
    next_page_token = None

    while True:
        # Call the API with the nextPageToken (if exists)
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,  # The maximum number of contacts to fetch in a single API call
            personFields='names,emailAddresses',
            pageToken=next_page_token).execute()

        connections.extend(results.get('connections', []))
        next_page_token = results.get('nextPageToken')

        # If there are no more pages, break the loop
        if not next_page_token:
            break
    
    return connections

# Function to print the user's contacts
def print_contacts():
    creds = authenticate()
    service = build('people', 'v1', credentials=creds)

    # Get all contacts (handling pagination)
    contacts = get_all_contacts(service)

    if not contacts:
        print('No contacts found.')
    else:
        print('Contacts:')
        for person in contacts:
            # Get names and email addresses
            names = person.get('names', [])
            email_addresses = person.get('emailAddresses', [])

            if names:
                print(f"Name: {names[0].get('displayName')}")
            if email_addresses:
                print(f"Email: {email_addresses[0].get('value')}")
            print('---')

if __name__ == '__main__':
    print_contacts()

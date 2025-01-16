# CardDAV and Google Contacts Integration

This repository contains Python scripts to interact with **CardDAV servers** and **Google Contacts API**. The scripts are designed to:

1. **Fetch contacts from a CardDAV server**.
2. **Upload a vCard (.vcf file)** to Google Contacts using the Google People API.

## Prerequisites

Before using the scripts, ensure the following:

- **Python 3.x** installed on your system.
- **Google Cloud Project** with **Google People API** enabled.
- **credentials.json** file from Google Cloud.
- Access to a **CardDAV server** (e.g., Nextcloud, etc.).
- Install required Python libraries by running:

    ```bash
    pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests vobject
    ```

## Setup Instructions

### 1. Get `credentials.json` from Google Cloud

To use Google APIs like **Google People API** for uploading contacts, you need to set up a **Google Cloud Project** and **enable the People API**.

1. **Create a Google Cloud Project** at [Google Cloud Console](https://console.cloud.google.com/).
2. **Enable the People API** from the [Google People API page](https://console.cloud.google.com/apis/library/people.googleapis.com).
3. **Create OAuth 2.0 credentials**:
   - Go to **APIs & Services > Credentials**.
   - Create **OAuth 2.0 Client ID** for a **Desktop App**.
   - Download the **credentials.json** file and save it in your project folder.

### 2. `get_all_contacts.py` – Fetch Contacts from CardDAV Server

This script retrieves contacts from a **CardDAV server** (e.g., Nextcloud, ownCloud, etc.).

#### Configuration:
- Modify the `CARDDAV_SERVER_URL` in the script to point to your CardDAV server URL (you may need an appropriate CardDAV client library).

Run the script to fetch and display contacts:

```bash
python get_all_contacts.py
```

### 3. `upload_vcard_to_google.py` – Upload vCard to Google Contacts

This script uploads a **vCard (.vcf file)** to **Google Contacts** using the **Google People API**.

#### Configuration:
- Place your **`credentials.json`** in the same directory as the script.
- Specify the path to the vCard file you want to upload.

Run the script to upload the vCard:

```bash
python upload_vcard_to_google.py
```

### Code Explanation

- **authenticate_google_account**: Handles OAuth 2.0 authentication with Google, saving credentials in `token.pickle`.
- **upload_vcard_to_google**: Uploads a contact to Google Contacts. You can extend this to parse a vCard file and upload its contents.

#### First-Time Authentication

The script will prompt you to sign in with your Google account and authorize access to your contacts. After successful login, credentials will be stored in `token.pickle`.

## Example Use Case

### Migrating Contacts from CardDAV to Google Contacts

1. Use `get_all_contacts.py` to fetch contacts from your **CardDAV server**.
2. Export contacts to a **vCard file**.
3. Use `upload_vcard_to_google.py` to upload the vCard to **Google Contacts**.

## Notes

- **CardDAV server** URL and credentials should be set up correctly.
- **Google API OAuth 2.0** requires the **`credentials.json`** for authentication.
- The **People API scope** used is `https://www.googleapis.com/auth/contacts` to manage contacts.
- Large contacts lists might hit **API rate limits**; ensure proper error handling and pagination in such cases.

## License

This project is licensed under the GNU GPL License v3.0 – see the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to fork the repository and submit pull requests with improvements or additional features.

## Contact

For issues or questions, open an issue on the GitHub repository.


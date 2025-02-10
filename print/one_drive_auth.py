import configparser
import msal
import requests

def list_files_in_directory(access_token, directory_path):
    """
    List the files and folders in the specified OneDrive directory.

    :param access_token: The Microsoft Graph API access token.
    :param directory_path: The OneDrive directory path (e.g., "/Documents").
                           Use "/" or an empty string for the root directory.
    :return: A list of dictionaries representing files/folders.
    """
    # Determine the correct URL endpoint based on the directory path.
    if directory_path == "/" or not directory_path.strip():
        url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    else:
        # Ensure the path starts with a '/' and does not end with one for correct formatting.
        # Example: "/Documents" becomes "drive/root:/Documents:/children"
        url = f"https://graph.microsoft.com/v1.0/me/drive/root:{directory_path}:/children"
    
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        return data.get("value", [])
    else:
        print("Error fetching OneDrive items:", response.text)
        return []

def main():
    # Load configuration from file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Retrieve configuration values
    username = config['onedrive']['username']
    password = config['onedrive']['password']
    onedrive_path = config['onedrive']['path']  # This can be any directory path, e.g., "/Documents"
    client_id = config['onedrive']['client_id']
    tenant_id = config['onedrive']['tenant_id']
    scope = config['onedrive'].get('scope', 'https://graph.microsoft.com/.default')
    
    # Build the authority URL for your tenant
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    
    # Initialize the MSAL public client application
    app = msal.PublicClientApplication(client_id, authority=authority_url)
    
    # Acquire token using Resource Owner Password Credentials (ROPC) flow.
    result = app.acquire_token_by_username_password(username, password, scopes=[scope])
    
    if "access_token" in result:
        print("Authentication successful!")
        access_token = result["access_token"]
        
        # Call the function to list files in the specified directory.
        files = list_files_in_directory(access_token, onedrive_path)
        print(f"Files and folders in directory '{onedrive_path}':")
        for item in files:
            print(" -", item.get('name'))
    else:
        print("Authentication failed!")
        print("Error:", result.get("error"))
        print("Error description:", result.get("error_description"))

if __name__ == '__main__':
    main()

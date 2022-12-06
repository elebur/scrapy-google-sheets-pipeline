import os
import sys

import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# Scope for which access is granted
# see: https://developers.google.com/identity/protocols/oauth2/scopes#script
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def main() -> None:
    """Save credentials for Google Sheets api to file token.pickle"""
    # create a flow from Google Client secret file
    root_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(root_dir, 'credentials.json'),
        SCOPES)
    # get token from flow
    result = flow.run_local_server(port=0)
    # save token to .pickle file
    with open(os.path.join(root_dir, 'token.pickle'), 'wb') as token:
        pickle.dump(result, token)


if __name__ == '__main__':
    main()

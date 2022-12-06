# scrapy-google-sheets-pipeline
A Scrapy ItemPipeline to write Items to the Google Sheets via Google API.

## Google API setup
[Google's Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
### Configure the API
1. Step 1. Create a project. [Click here](https://console.cloud.google.com/projectcreate)
2. Step 2. Enable API for the created project. [Click here](https://console.cloud.google.com/apis/dashboard)
    * Choose your project at the top left of the screen
    * Press *+ ENABLE API AND SERVICES* button (it is slightly below the drop down list with projects)
    * Type *sheets* in search input and then choose *Google Sheets API*
    * Press *ENABLE*
3. Step 3. Create credentials. [Click here](https://console.cloud.google.com/apis/credentials)
    * Make sure you chose right project.
    * Press *+ CREATE CREDENTIALS* button (it is slightly below the drop down list with projects)
    * Choose *OAuth Client ID* from the drop down list
        * Before creating credentials you have to configure consent screen (to do this, click on the corresponding button). After you finished configuring consent screen repeat step 3 from the begining
    * Choose *Desktop App* and set any name and press *CREATE* button
    * Congratulations. Now download your *credentials.json* file (keep it in a secure place!).

### Install the Client Library
Afterwards you will probably need to install some libraries. The following command should do it in most cases:
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

### Get your token
Now you can retrieve your token with the included file `get_token.py`. 
You should be able to start it with `python get_token.py`. After granting permissions, you should end up with a file named `token.pickle`. Move this file to the `scrapy_google_sheets_example/resources` folder.

### Usage limits
December 2022. In future the limits might change.
* Sheets API has no hard size limits for an API request, but Google recommends a 2-MB maximum payload.
* 300 requests in a minute per project
* 60 requests in a minute per user per project

[Click here](https://developers.google.com/sheets/api/limits) to get more info about limits.

On [this page](https://console.cloud.google.com/projectselector2/iam-admin/quotas) you can see current quota usage and limits.

[This page](https://console.cloud.google.com/apis/dashboard) shows statistic for Google API.

## Settings
* `GOOGLE_SHEET_ID` - the ID of the Spreadsheet you want to save your data to. You can get the ID from the url. 
For example, for this url https://docs.google.com/spreadsheets/d/1eX8ftT1jKY2MyUcaHFV-Oo93qGP1NgHdcC-4MFm6UUc/edit#gid=0 the ID is **1eX8ftT1jKY2MyUcaHFV-Oo93qGP1NgHdcC-4MFm6UUc**.
* `GOOGLE_SHEET_TOKEN_FILEPATH` - absolute path to the `token.pickle` file (you got this file after running `get_token.py`)
* `GOOGLE_SHEET_EXPORT_FIELDS` - same as [FEED\_EXPORT\_FIELDS](https://docs.scrapy.org/en/latest/topics/feed-exports.html?#feed-export-fields), but for Google Sheets. If the setting doesn't exist then FEED\_EXPORT\_FIELDS will be used.

## Starting the example spider
The included spider is an example that gets quotes and their authors from [quotes.toscrape.com](http://quotes.toscrape.com/).
You can use the command `scrapy crawl quotes` to start the process. 


## TODO
- [ ] `RANGE` setting to manually set the range where data will be appended (e.g. `A:AB`, `C:Z`)
- [ ] `START_COLUMN` setting. Data will be appended starting from this column.
- [ ] Bulk appending
- [ ] Async Google API?
- [ ] Adding a header to a sheet (if the sheet is not empty then the header mustn't be added)
- [ ] API error handling
- [ ] Checking a sheet availability on startup and [closing spider](https://stackoverflow.com/q/9699049/19813684) if the sheet is not available.
    - [ ] Check write permisions for the sheet (how?)
- [ ] Saving data from the failed requests to a local file
- [ ] How to deal with [limits](https://developers.google.com/sheets/api/limits)? [Retry Strategy](https://cloud.google.com/storage/docs/retry-strategy)
- [ ] if a sheet in trash data will be appended anyway
- [ ] Tests
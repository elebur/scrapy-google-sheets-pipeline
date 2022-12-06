import os

from .pipelines import GoogleSheetsPipeline

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Scrapy settings for scrapy_google_sheets_example project
BOT_NAME = 'scrapy_google_sheets_example'
SPIDER_MODULES = ['scrapy_google_sheets_example.spiders']
NEWSPIDER_MODULE = 'scrapy_google_sheets_example.spiders'

# id of the spreadsheet you want to use to store your data
GOOGLE_SHEET_ID = '1eX8ftT1jKY2MyUcaHFV-Oo93qGP1NgHdcC-4MFm6UUc'

# Absolut path to the pickled file with auth data
GOOGLE_SHEET_TOKEN_FILEPATH = os.path.join(PROJECT_ROOT, "resources", "token.pickle")

# Fields to export to the sheet.
# This settings has higher priority than FEED_EXPORT_FIELDS
GOOGLE_SHEET_EXPORT_FIELDS = {
    "quote": "Quote",
    "author": "Author"
}
# activate the pipeline to transfer data to google sheets
ITEM_PIPELINES = {
    GoogleSheetsPipeline: 300
}

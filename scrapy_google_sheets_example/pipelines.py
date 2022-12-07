import pickle

from itemadapter import ItemAdapter
from googleapiclient.discovery import build


class GoogleSheetsPipeline:
    """
    Pipeline for saving data to Google Sheets
    """

    def __init__(self, crawler) -> None:
        # Sheet id for saving data to.
        self.sheet_id = crawler.settings.get("GOOGLE_SHEET_ID")
        # Get the Item fields that should be saved to the Google Sheet.
        # If fields aren't set in GOOGLE_SHEET_EXPORT_FIELDS setting,
        # then try getting them from FEED_EXPORT_FIELDS (it also could be None)
        self.export_fields = (
            crawler.settings.get("GOOGLE_SHEET_EXPORT_FIELDS")
            or crawler.settings.get("FEED_EXPORT_FIELDS")
            or {}
        )

        # load token from pickle file which you
        # hopefully saved to the "resources" folder
        token_file_path = crawler.settings.get("GOOGLE_SHEET_TOKEN_FILEPATH")
        with open(token_file_path, "rb") as fin:
            token = pickle.load(fin)

        # Should we replace decimal dot with comma for float.
        self.replace_dot_with_comma = crawler.settings.get(
            "GOOGLE_SHEET_REPLACE_DECIMAL_DOT_WITH_COMMA",
            True)

        # build connection to google sheets api
        service = build("sheets", "v4", credentials=token)
        self.sheet = service.spreadsheets()

    @classmethod
    def from_crawler(cls, crawler) -> None:
        return cls(crawler)

    def _build_body(self, item) -> dict:
        """build body for data to submit to google sheets from item"""
        def serialize(item, field, value):
            """
            Inner function to apply serializer if it is set.
            """
            adapter = ItemAdapter(item)
            meta = adapter.get_field_meta(field)
            # https://github.com/scrapy/scrapy/blob/f9a29f03d9a0eb9173a91f225177b7bee7d382c9/scrapy/exporters.py#L48-L50
            serializer = meta.get('serializer', lambda x: x)
            return serializer(value)

        if not self.export_fields:
            fields_iterable = None
            if hasattr(item, "fields"):
                fields_iterable = item.fields()
            elif hasattr(item, "keys"):
                fields_iterable = item.items()
            else:
                raise ValueError(f"Couldn't get export_fields for item of type {str(type(item))}")

            for name, value in fields_iterable:
                self.export_fields[name] = name

        values = list()

        for field in self.export_fields.keys():
            value = item.get(field, "")

            value = serialize(item, field, value)
            s = str(value)
            if isinstance(value, float) and self.replace_dot_with_comma:
                s = s.replace(".", ",")
            values.append(s)

        return {'values': [values]}

    def _append_to_sheet(self, item) -> None:
        """
        Append item to spreadsheet
        https://developers.google.com/sheets/api/guides/values
        """
        # get body for sheets request from item
        body = self._build_body(item)
        range_end = get_column_letter(len(self.export_fields))
        # append body to spreadsheet
        self.sheet.values().append(
            spreadsheetId=self.sheet_id,
            range=f"A:{range_end}",
            body=body,
            valueInputOption="USER_ENTERED"
        ).execute()

    def process_item(self, item, spider):
        self._append_to_sheet(item)
        return item


def get_column_letter(num):
    """
    Converts numeric column to letter:
    1 -> 'A', 26 -> 'Z', 333 -> 'LU'

    Based on this answer https://stackoverflow.com/a/28782635/19813684

    Checking edge cases.
    >>> get_column_letter(1)
    'A'
    >>> get_column_letter(0)
    Traceback (most recent call last):
      ...
    ValueError: Column number must be greater then 0.
    >>> get_column_letter(18278)
    'ZZZ'
    >>> get_column_letter(18279)
    Traceback (most recent call last):
      ...
    ValueError: Column number must be less then or equal to 18278.

    Checking wrong types.
    >>> get_column_letter("")
    Traceback (most recent call last):
      ...
    ValueError: Column number must be of type <int>
    >>> get_column_letter(12.2)
    Traceback (most recent call last):
      ...
    ValueError: Column number must be of type <int>
    >>> get_column_letter(True)
    Traceback (most recent call last):
      ...
    ValueError: Column number must be of type <int>

    Checking all posible combinations of letters.
    >>> from itertools import product
    >>> letters = list()
    >>> for i in range(1, 4):
    ...     tmp = map(
    ...         lambda x: "".join(x),
    ...         product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=i)
    ...     )
    ...     letters.extend(tmp)
    >>> for i, value in enumerate(letters):
    ...     index = i+1
    ...     res = get_column_letter(index)
    ...     if res != value:
    ...         print(f"Got - {res}, expected - {value}, index - {index}")


    """
    if type(num) is not int:
        raise ValueError("Column number must be of type <int>")
    elif num <= 0:
        raise ValueError("Column number must be greater then 0.")
    elif num > 18278:
        raise ValueError("Column number must be less then or equal to 18278.")
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = list()
    while num:
        mod = (num - 1) % 26
        num = int((num - mod) / 26)
        result.append(letters[mod])
    return "".join(reversed(result))

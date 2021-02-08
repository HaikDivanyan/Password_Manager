import gspread
from pprint import pprint

gc = gspread.service_account(filename= 'credentials.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1q0k31oZvubARl1k89BKuJlW6GbxqMlhHTCcNddU-llo/edit#gid=0')
worksheet = sh.sheet1

def updateSheet(data):
    max_rows = len(worksheet.get_all_values())
    worksheet.delete_rows(2, max_rows)
    for entry in data:   
        worksheet.append_row(entry)


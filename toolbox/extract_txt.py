import csv

class Extracted_User:
    def __init__(self, display_name:str, login:str, password:str):
        self.display_name = display_name
        self.login = login
        self.password = password

raw = []
with open("voteApp_users.txt", encoding="utf-8") as users:
    for line in users:
        raw.append(line.strip())
raw = [x for x in raw if x != '' and ":" not in x]

extracted_users = []
user = []
for i, info in enumerate(raw):
    user.append(info)
    if (i+1)%3 == 0:
        extracted_users.append(user)
        user = []

with open("users.csv", 'w', encoding='utf-8') as fcsv:
    writer = csv.writer(fcsv)
    for credentials in extracted_users:
        writer.writerow(credentials)

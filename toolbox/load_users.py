import csv
import django 
import os

class Extracted_User:
    def __init__(self, display_name:str, login:str, password:str):
        self.display_name = display_name
        self.login = login
        self.password = password

extracted_users = []

with open('users.csv', 'r', encoding='utf-8') as fscv:
    reader = csv.reader(fscv)
    for row in reader:
        new_user = Extracted_User(row[0], row[1], row[2])
        extracted_users.append(new_user)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voteProject.settings')
django.setup()
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

for extracted_user in extracted_users:
    user = CustomUser.objects.create_user(
        username=extracted_user.login,
        password=extracted_user.password,
        display_name = extracted_user.display_name
    )
    print(f"{user.display_name} has been added!")
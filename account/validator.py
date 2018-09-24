from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile

def valid_username(username_value):
    allow_username_char = ["a", "b", 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', "2", '3', '4', '5', '6', '7', '8', '9', '_', '-', "A", "B", 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for char in username_value:
        if not char in allow_username_char:
            return False
    return True

def username_exist(username_value):
    try:
        existing_user = User.objects.get(username__iexact=username_value)
    except User.DoesNotExist:
        return False
    if existing_user:
        return True

def valid_contact_email(contact):
    allow_email_char = ["a", "b", 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', "2", '3', '4', '5', '6', '7', '8', '9', '_', '-', '@', '.', '&', '=', "A", "B", 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if "@" in contact and "." in contact:
        for char in contact[:3]:
            if char == "@":
                return False
        arobase_come_first = False
        point_come_first = False
        for char in contact:
            if char == "@" and not point_come_first:
                arobase_come_first =True
            if char == "." and not arobase_come_first:
                point_come_first =True
        if point_come_first:
            return False
        for char in contact:
            if not char in allow_email_char:
                return False
    else:
        return "Not email"
    return True

def existing_mail_address(contact):
    try:
        existing_email = User.objects.get(email=contact)
    except User.DoesNotExist:
        return False
    if existing_email:
        return True

def valid_contact_phone_number(contact):
    allow_phone_number_char = ["+",'0', "1", "2", "3", "4", '5', '6', '7', '8', '9']
    for char in contact:
        if not char in allow_phone_number_char:
            return False
    if not '+' in contact:
        return False
    if not contact[0] == "+":
        return False
    plus_count = 0
    for char in contact:
        if char == "+":
            plus_count = plus_count + 1
    if plus_count != 1:
        return False
    return True

def existing_phone_number(contact):
    try:
        existing_number = Profile.objects.get(phone_number=contact)
    except Profile.DoesNotExist:
        return False
    if existing_number:
        return True

def passwords_match(value, confirm_value):
    if value == confirm_value:
        return True
    return False

def valid_password(password):
    if password.count('') < 9:
        return False
    try:
        int(password)
        return False
    except ValueError:
        pass
    return True

def salting_password(password):
    password = "&12@kichichi" + password + "&12@infinity"
    return password

def GETis404(request):
    pass
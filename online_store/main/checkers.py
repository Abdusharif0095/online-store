import re
from datetime import datetime


def isRightCharField(field):
    return re.search(r'\w', field) and 0 < len(field) < 257


def isRightAddress(town, street, building):
    return isRightCharField(town) and isRightCharField(street) and isRightCharField(building)


def isRightApartment(number):
    if type(number) == int and 0 < number:
        return True
    else:
        return False


def isRightName(name):
    for char in name:
        if char != ' ' and not char.isalpha():
            return False
    return True


def isRightDate(date):
    try:
        is_right_date = re.fullmatch(r'\d\d\.\d\d\.\d\d\d\d', date)
        return True
    except Exception as e:
        return False


def getRightDate(date):
    try:
        if isRightDate(date):
            date = datetime.strptime(date, '%d.%m.%Y')
            now_date = datetime.utcnow()
            if date < now_date:
                return date.date()
            else:
                return False
        else:
            return False
    except Exception as e:
        return False


def isRightId(id):
    return type(id) == int and 0 < id


def isRightGender(gender):
    return gender in ('male', 'female')


def isRightRelativesList(relatives):
    if type(relatives) != list:
        return False

    for id in relatives:
        if type(id) != int:
            return False

    return True

# print(getRightDate('11.12.2022'))
# print(isRightName('a b мам 1'))

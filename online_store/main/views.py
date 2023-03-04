import json
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from . import checkers
from collections import Counter


bad_request = HttpResponse(status=400)

def index(request):
    return HttpResponse("<h1>Hello from online-store!</h1>")


def check_time_out(counter, timeout=10, limit=10000):
    counter += 1

    if counter > limit:
        time.sleep(timeout)
        counter = 0

    return counter


@csrf_exempt
def add_imports(request):
    try:
        data = json.loads(request.body.decode())
        new_import = Import()
        new_import.save()
        counter = 0

        created_request = HttpResponse(
            status=201,
            headers={
                "data": {
                    "import_id": new_import.pk
                }
            }
        )

        for dt in data["citizens"]:
            if len(dt) != 9:
                return bad_request
            if (checkers.isRightId(dt['citizen_id'])
                    and checkers.isRightAddress(
                    dt['town'], dt['street'], dt['building'])
                    and checkers.isRightApartment(dt['apartment'])
                    and checkers.isRightName(dt['name'])
                    and checkers.isRightDate(dt['birth_date'])
                    and checkers.isRightGender(dt['gender'])
                    and checkers.isRightRelativesList(dt['relatives'])):
                relatives = {'citizen_ids': dt['relatives']}
                new_citizen = Citizen(
                    import_id=new_import.pk,
                    citizen_id=dt['citizen_id'],
                    town=dt['town'],
                    street=dt['street'],
                    building=dt['building'],
                    apartment=dt['apartment'],
                    name=dt['name'],
                    birth_date=checkers.getRightDate(dt['birth_date']),
                    gender=dt['gender'],
                    relatives=json.dumps(relatives))
                new_citizen.save()
                new_import.citizens.add(new_citizen)
                counter = check_time_out(counter)

        new_import.save()
        return created_request
    except Exception as e:
        print(e)
        return bad_request


@csrf_exempt
def change_citizen_data(request, import_id, citizen_id):
    try:
        data = json.loads(request.body.decode())
        fields_check = {
            "town": checkers.isRightCharField,
            "street": checkers.isRightCharField,
            "building": checkers.isRightCharField,
            "apartment": checkers.isRightApartment,
            "name": checkers.isRightName,
            "birth_date": checkers.isRightDate,
            "gender": checkers.isRightGender,
            "relatives": checkers.isRightRelativesList
        }

        import_citizens = Import.objects.filter(id=import_id).first().citizens.all()
        citizen = import_citizens.filter(citizen_id=citizen_id).first()

        if citizen is None:
            return bad_request

        for key in data:
            if not key in fields_check:
                return bad_request

        if 'town' in data:
            if fields_check['town'](data['town']):
                citizen.town = data['town']
            else:
                return bad_request

        if 'street' in data:
            if fields_check['street'](data['street']):
                citizen.street = data['street']
            else:
                return bad_request

        if 'building' in data:
            if fields_check['building'](data['building']):
                citizen.building = data['building']
            else:
                return bad_request

        if 'apartment' in data:
            if fields_check['apartment'](data['apartment']):
                citizen.apartment = data['apartment']
            else:
                return bad_request

        if 'name' in data:
            if fields_check['name'](data['name']):
                citizen.name = data['name']
            else:
                return bad_request

        if 'birth_date' in data:
            if fields_check['name'](data['name']):
                citizen.birth_date = checkers.getRightDate(data['birth_date'])
            else:
                return bad_request

        if 'gender' in data:
            if fields_check['gender'](data['gender']):
                citizen.gender = data['gender']
            else:
                return bad_request

        if 'relatives' in data:
            new_relatives = data['relatives']
            old_relatives = json.loads(citizen.relatives)['citizen_ids']

            if not fields_check['relatives'](new_relatives):
                return bad_request

            if list(set(new_relatives)) != new_relatives:
                return bad_request

            new_relatives_counter = Counter(new_relatives)
            old_relatives_counter = Counter(old_relatives)

            for key in new_relatives_counter:
                if key not in old_relatives_counter:
                    cur_citizen = import_citizens.filter(citizen_id=new_relatives_counter[key]).first()
                    rels = json.loads(cur_citizen.relatives)
                    rels['citizen_ids'].append(citizen_id)
                    cur_citizen.relatives = json.dumps(rels)
                    cur_citizen.save()

            for key in old_relatives_counter:
                if key not in new_relatives_counter:
                    cur_citizen = import_citizens.filter(citizen_id=key).first()
                    rels = json.loads(cur_citizen.relatives)
                    rels['citizen_ids'].remove(citizen_id)
                    cur_citizen.relatives = json.dumps(rels)
                    cur_citizen.save()

            new_res = {
                "citizen_ids": new_relatives
            }
            citizen.relatives = json.dumps(new_res)
            citizen.save()

        return HttpResponse(
            status=200,
            headers={
                "data": {
                    "citizen_id": citizen.citizen_id,
                    "town": citizen.town,
                    "street": citizen.street,
                    "building": citizen.building,
                    "apartment": citizen.apartment,
                    "name": citizen.name,
                    "birth_date": citizen.birth_date,
                    "gender": citizen.gender,
                    "relatives": json.loads(citizen.relatives)['citizen_ids']
                }
            },
        )
    except Exception as e:
        print(e)
        return bad_request


def get_citizens(request, import_id):
    pass


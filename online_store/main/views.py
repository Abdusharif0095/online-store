import json
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from . import checkers


def index(request):
    return HttpResponse("<h1>Hello!</h1>")


def time_out(counter, timeout=10, limit=10000):
    counter += 1

    if counter > limit:
        time.sleep(timeout)
        counter = 0

    return counter


@csrf_exempt
def add_imports(request):
    # print(request.body)
    try:
        data = json.loads(request.body.decode())
        new_import = Import()
        new_import.save()
        created_request = HttpResponse(
            status=201,
            headers={
                "data": {
                    "import_id": new_import.pk
                }
            }
        )
        bad_request = HttpResponse(status=400)

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
            else:
                print(dt)
                print(checkers.isRightId(dt['citizen_id']),
                    checkers.isRightAddress(
                    dt['town'], dt['street'], dt['building']), checkers.isRightApartment(dt['apartment']), checkers.isRightName(dt['name']), checkers.isRightDate(dt['birth_date']), checkers.isRightGender(dt['gender']), checkers.isRightRelativesList(dt['relatives']))
                return bad_request

        new_import.save()
        return created_request
    except Exception as e:
        print(e)
        return JsonResponse({
            'Error': f'{e}',
        })


@csrf_exempt
def change_citizen_data(request, import_id, citizen_id):
    try:
        data = json.loads(request.body.decode())
        print(type(data))
        import_id = 1
        return HttpResponse(
            status=200,
            headers={
                "data": json.dumps(data)
            }
        )
    except Exception as e:
        print(e)
        return JsonResponse({
            'error': f'{e}',
        })


def get_citizens(request, import_id):
    pass


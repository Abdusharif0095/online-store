import json
import time
import numpy
import datetime
from .models import *
from . import checkers
from collections import Counter
from collections import defaultdict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


counter = 0
bad_request = HttpResponse(status=400)


def index(request):
    return HttpResponse("<h1>Hello from online-store!</h1>")


def check_time_out(counter, timeout=10, limit=10000):
    if counter > limit:
        time.sleep(timeout)

    return counter


def get_age(birth_date):
    now = datetime.datetime.utcnow()
    age = now.year - birth_date.year

    if now.month < birth_date.month:
        age -= 1
    elif now.month == birth_date.month:
        age -= (birth_date.day > now.day)

    return age


def citizen_to_dict(citizen):
    data = {
        "citizen_id": citizen.citizen_id,
        "town": citizen.town,
        "street": citizen.street,
        "building": citizen.building,
        "apartment": citizen.apartment,
        "name": citizen.name,
        "birth_date": citizen.birth_date,
        "gender": citizen.gender,
        "relatives": json.loads(citizen.relatives)["citizen_ids"]
    }
    return data


@csrf_exempt
def add_imports(request):
    global counter
    check_time_out(counter)
    try:
        data = json.loads(request.body.decode())
        new_import = Import()
        new_import.save()

        created_request = JsonResponse(
            status=201,
            data={
                "data": {"import_id": new_import.pk}
            }
        )

        for dt in data["citizens"]:
            if len(dt) != 9:
                return bad_request
            if (checkers.isRightId(dt["citizen_id"])
                    and checkers.isRightAddress(
                        dt["town"], dt["street"], dt["building"])
                    and checkers.isRightApartment(dt["apartment"])
                    and checkers.isRightName(dt["name"])
                    and checkers.isRightDate(dt["birth_date"])
                    and checkers.isRightGender(dt["gender"])
                    and checkers.isRightRelativesList(dt["relatives"])):
                relatives = {"citizen_ids": dt["relatives"]}
                new_citizen = Citizen(
                    import_id=new_import.pk,
                    citizen_id=dt["citizen_id"],
                    town=dt["town"],
                    street=dt["street"],
                    building=dt["building"],
                    apartment=dt["apartment"],
                    name=dt["name"],
                    birth_date=checkers.getRightDate(dt["birth_date"]),
                    gender=dt["gender"],
                    relatives=json.dumps(relatives))
                new_citizen.save()
                new_import.citizens.add(new_citizen)
                counter += 1
        new_import.save()
        return created_request
    except Exception as e:
        return bad_request


@csrf_exempt
def change_citizen_data(request, import_id, citizen_id):
    global counter
    check_time_out(counter)
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

        if "town" in data:
            if fields_check["town"](data["town"]):
                citizen.town = data["town"]
            else:
                return bad_request

        if "street" in data:
            if fields_check["street"](data["street"]):
                citizen.street = data["street"]
            else:
                return bad_request

        if "building" in data:
            if fields_check["building"](data["building"]):
                citizen.building = data["building"]
            else:
                return bad_request

        if "apartment" in data:
            if fields_check["apartment"](data["apartment"]):
                citizen.apartment = data["apartment"]
            else:
                return bad_request

        if "name" in data:
            if fields_check["name"](data["name"]):
                citizen.name = data["name"]
            else:
                return bad_request

        if "birth_date" in data:
            if fields_check["name"](data["name"]):
                citizen.birth_date = checkers.getRightDate(data["birth_date"])
            else:
                return bad_request

        if "gender" in data:
            if fields_check["gender"](data["gender"]):
                citizen.gender = data["gender"]
            else:
                return bad_request

        if "relatives" in data:
            new_relatives = data["relatives"]
            old_relatives = json.loads(citizen.relatives)["citizen_ids"]

            if not fields_check["relatives"](new_relatives):
                return bad_request

            if list(set(new_relatives)) != new_relatives:
                return bad_request

            new_relatives_counter = Counter(new_relatives)
            old_relatives_counter = Counter(old_relatives)

            for key in new_relatives_counter:
                if key not in old_relatives_counter:
                    cur_citizen = import_citizens.filter(citizen_id=new_relatives_counter[key]).first()
                    rels = json.loads(cur_citizen.relatives)
                    rels["citizen_ids"].append(citizen_id)
                    cur_citizen.relatives = json.dumps(rels)
                    cur_citizen.save()

            for key in old_relatives_counter:
                if key not in new_relatives_counter:
                    cur_citizen = import_citizens.filter(citizen_id=key).first()
                    rels = json.loads(cur_citizen.relatives)
                    rels["citizen_ids"].remove(citizen_id)
                    cur_citizen.relatives = json.dumps(rels)
                    cur_citizen.save()

            new_res = {
                "citizen_ids": new_relatives
            }
            citizen.relatives = json.dumps(new_res)
            citizen.save()
        print(citizen_to_dict(citizen))
        return JsonResponse(
            status=200,
            data={"data": citizen_to_dict(citizen)}
        )
    except Exception as e:
        return bad_request


def get_citizens(request, import_id):
    global counter
    check_time_out(counter)
    try:
        import_citizens = Import.objects.filter(id=import_id).first().citizens.all()
        data = []
        for citizen in import_citizens:
            data.append(citizen_to_dict(citizen))

        return JsonResponse(
            status=200,
            data={"data": data},
            safe=False
        )
    except Exception as e:
        return bad_request


def get_import_citizens_birthsdays(request, import_id):
    global counter
    check_time_out(counter)
    try:
        import_citizens = Import.objects.filter(id=import_id).first().citizens.all()
        presents_in_every_month = {}
        citizens_birth_months_presents = {
            1: {}, 2: {}, 3: {}, 4: {},
            5: {}, 6: {}, 7: {}, 8: {},
            9: {}, 10: {}, 11: {}, 12: {}
        }

        for citizen in import_citizens:
            birth_month = citizen.birth_date.month
            relatives = json.loads(citizen.relatives)["citizen_ids"]

            for relative_id in relatives:
                citizens_birth_months_presents[birth_month][relative_id] = \
                    citizens_birth_months_presents[birth_month]. \
                        get(relative_id, 0) + 1

        for month in range(1, 13):
            result_list = []
            for citizen_id in citizens_birth_months_presents[month]:
                result_dict = {
                    "citizen_id": citizen_id,
                    "presents": citizens_birth_months_presents[month][citizen_id]
                }
                result_list.append(result_dict)
            presents_in_every_month[str(month)] = result_list

        return JsonResponse(
            status=200,
            data={"data": presents_in_every_month},
        )
    except Exception as e:
        return bad_request


def get_percentile_age(request, import_id):
    global counter
    check_time_out(counter)
    try:
        import_citizens = Import.objects.filter(id=import_id).first().citizens.all()
        town_ages = defaultdict(list)

        for citizen in import_citizens:
            town_ages[citizen.town].append(get_age(citizen.birth_date))

        result_list = []

        for town, ages in town_ages.items():
            result_dict = {
                "town": town
            }

            for percent in [50, 75, 99]:
                print(ages, percent)
                result_dict[f"p{percent}"] = numpy.percentile(ages, percent, interpolation="linear")
            result_list.append(result_dict)

        return JsonResponse(
            status=200,
            data={
                "data": result_list
            },
            safe=False
        )
    except Exception as e:
        return bad_request

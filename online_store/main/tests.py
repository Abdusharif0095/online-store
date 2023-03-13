import os
import json
import random
from django.test import TestCase
from django.urls import reverse
from .models import *


curDir = os.getcwd()


def generate_citizens(citizens_count=1, max_relatives_count=0):
    citizens = {
        "citizens": []
    }

    towns = []
    streets = []
    names = []
    dates = []

    with open(f"{curDir}/main/test_data/towns.txt", "r") as f:
        towns = list(map(str, f.read().split('\n')))[:-1]

    with open(f"{curDir}/main/test_data/streets.txt", "r") as f:
        streets = list(map(str, f.read().split('\n')))[:-1]

    with open(f"{curDir}/main/test_data/names.txt", "r") as f:
        names = list(map(str, f.read().split('\n')))[:-1]

    with open(f"{curDir}/main/test_data/dates.txt", "r") as f:
        dates = list(map(str, f.read().split('\n')))[:-1]

    for id in range(1, citizens_count + 1):
        citizen = {
            "citizen_id": id,
            "town": random.choice(towns),
            "street": random.choice(streets),
            "building": str(random.randint(1, 100)),
            "apartment": random.randint(1, 100),
            "name": random.choice(names),
            "birth_date": random.choice(dates),
            "gender": random.choice(["male", "female"]),
            "relatives": []
        }
        citizens["citizens"].append(citizen)

    count = random.randint(1, 10) * max_relatives_count

    for _ in range(count):
        first_id = random.randint(1, citizens_count)
        second_id = random.randint(1, citizens_count)
        citizens["citizens"][first_id - 1]["relatives"].append(second_id)
        citizens["citizens"][second_id - 1]["relatives"].append(first_id)

    for id in range(0, len(citizens["citizens"])):
        citizens["citizens"][id]["relatives"] = list(set(citizens["citizens"][id]["relatives"]))

    return citizens


class ServerTestCase(TestCase):
    def test_post_add_import(self):
        """
        Check post method that saves the new import to the DataBAse
        :return:
        """

        citizens = json.dumps(generate_citizens(1000, 10))
        response = self.client.post(
            reverse('add_import'),
            data=citizens,
            content_type='application/json'
        )

        if response.status_code != 201:
            print("error")

        self.assertEqual(response.status_code, 201)

    def test_post_add_import_with_error_lines(self):
        """
        Check post method /imports
        :return:
        """

        error_lines = ["citizen_id", "town", "street",
                       "building", "apartment", "name",
                       "birth_date", "gender", "relatives"
                       ]

        for line in error_lines:
            citizens = generate_citizens(50, 10)
            if line == "relatives":
                citizens["citizens"][0]["relatives"] = [2]
                citizens["citizens"][1]["relatives"] = []
            elif line == "birth_date":
                citizens["citizens"][0][line] = "31.11.2022"
            else:
                citizens["citizens"][0][line] = ""
            response = self.client.post(
                reverse("add_import"),
                data=json.dumps(citizens),
                content_type="application/json"
            )
            if response.status_code == 201:
                print(line)
            self.assertEqual(response.status_code, 400)

    def test_patch_change_citizen(self):
        """
        Check patch method /imports/$import_id/citizens/$citizen_id
        :return:
        """

        self.test_post_add_import()

        data = {
            "name": "Иванова Мария Леонидовна",
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "relatives": []
        }

        response = self.client.patch(
            "/imports/1/citizens/1",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_change_citizen_errors(self):
        """
        Check patch method /imports/$import_id/citizens/$citizen_id with erroneous data
        :return:
        """

        self.test_post_add_import()
        data = {
            "birth_date": "29.02.2012",
        }

        response = self.client.patch(
            "/imports/1/citizens/1",
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.patch(
            "/imports/-1/citizens/1",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.patch(
            "/imports/1/citizens/-1",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_get_import_citizens(self):
        """
        Check get method /imports/$import_id/citizens
        :return:
        """

        self.test_post_add_import()

        response = self.client.get("/imports/1/citizens")
        self.assertEqual(response.status_code, 200)

    def test_get_import_citizens_errors(self):
        """
        Check get method /imports/$import_id/citizens
        with erroneous data
        :return:
        """

        self.test_post_add_import()

        response = self.client.get("/imports/-1/citizens")
        self.assertEqual(response.status_code, 404)

    def test_get_import_citizens_birthdays(self):
        """
        Check get method /imports/$import_id/citizens/birthdays
        :return:
        """

        self.test_post_add_import()

        # print(Import.objects.all().first())
        response = self.client.get(
            "/imports/1/citizens/birthdays"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_import_citizens_birthdays_error(self):
        self.test_post_add_import()

        response = self.client.get(
            "/imports/-1/citizens/birthdays"
        )
        self.assertEqual(response.status_code, 404)

    def test_get_import_town_percentile_age(self):
        self.test_post_add_import()

        response = self.client.get(
            "/imports/1/towns/stat/percentile/age"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_import_town_percentile_age_error(self):
        self.test_post_add_import()

        response = self.client.get(
            "/imports/-1/towns/stat/percentile/age"
        )
        self.assertEqual(response.status_code, 404)

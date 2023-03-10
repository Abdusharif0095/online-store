import os
import json
import random
from django.test import TestCase
from django.urls import reverse


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
        towns = list(map(str, f.read().split('\n')))

    with open(f"{curDir}/main/test_data/streets.txt", "r") as f:
        streets = list(map(str, f.read().split('\n')))

    with open(f"{curDir}/main/test_data/names.txt", "r") as f:
        names = list(map(str, f.read().split('\n')))

    with open(f"{curDir}/main/test_data/dates.txt", "r") as f:
        dates = list(map(str, f.read().split('\n')))

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

    count = (citizens_count - 1) * random.randint(1, max_relatives_count)

    for _ in range(count):
        first_id = random.randint(1, citizens_count)
        second_id = random.randint(1, citizens_count)
        citizens["citizens"][first_id - 1]["relatives"].append(second_id)
        citizens["citizens"][second_id - 1]["relatives"].append(first_id)

    return citizens


class AddImportTestCase(TestCase):
    def test_post(self):
        citizens = json.dumps(generate_citizens(5, 5))
        response = self.client.post(
            reverse('add_import'),
            data=citizens,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

    def test_post_with_error_lines(self):
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
            self.assertEqual(response.status_code, 400)


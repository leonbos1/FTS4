from time import sleep
import json
import random

class MockData:
    def __init__(self):
        """Initializes the config file"""
        self._data = json.load(open('config.json'))
        self.speed = self._data['speed']
        self.amount_of_people = self._data['amount_of_people']
        self.heartrate = self._data['heartrate']
        self.adrenaline_levels = self._data['adrenaline_levels']
        self.mood = self._data['mood']
        self.body_temperature = self._data['body_temperature']
        self.blood_pressure = self._data['blood_pressure']
        self.amount_of_people_per_room = self._data['amount_of_people_per_room']
        self.people = self.init_people()

    def init_people(self):
        first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph", "Thomas", "Christopher", "Daniel", "Paul", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony", "Kevin", "Jason", "Matthew", "Gary", "Timothy", "Jose", "Larry", "Jeffrey", "Frank", "Scott", "Eric", "Stephen", "Andrew", "Raymond", "Gregory", "Joshua", "Jerry", "Dennis", "Walter", "Patrick", "Peter", "Harold", "Douglas", "Henry", "Carl", "Arthur", "Ryan", "Roger"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins"]
        people = []

        for i in range(self.amount_of_people):
            name = random.choice(first_names) + " " + random.choice(last_names)
            age = random.randint(18, 80)
            person = Person(name, age)
            person.heart_rate = 80
            people.append(person)
        return people

    def init_rooms(self):
        rooms_json = json.load(open('rooms.json'))["rooms"]
        rooms = []
        for room in rooms_json:
            rooms.append(Room(room["name"], room["capacity"]))



    def debug(self, persons=True, config=False):
        if config:
            print(self.speed)
            print(self.amount_of_people)
            print(self.heartrate)
            print(self.adrenaline_levels)
            print(self.mood)
            print(self.body_temperature)
            print(self.blood_pressure)
            print(self.amount_of_people_per_room)

        if persons:
            for person in self.people:
                person.print_person()

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def set_heart_rate(self, heart_rate):
        self.heart_rate = heart_rate

    def set_adrenaline_levels(self, adrenaline_levels):
        self.adrenaline_levels = adrenaline_levels

    def set_mood(self, mood):
        self.mood = mood

    def set_body_temperature(self, body_temperature):
        self.body_temperature = body_temperature

    def set_blood_pressure(self, blood_pressure):
        self.blood_pressure = blood_pressure

    def print_person(self):
        for key, value in self.__dict__.items():
            print(key, value)

class Room:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.people = []

    def add_person(self, person):
        if len(self.people) < self.capacity:
            self.people.append(person)
            return True
        else:
            return False

    def get_people(self):
        return self.people

    def get_person_with_higher_heart_rate(self):
        person = self.people[0]
        for p in self.people:
            if p.heart_rate > person.heart_rate:
                person = p
        return person

def main():
    """Main function"""
    mock_data = MockData()
    mock_data.debug()

if __name__ == '__main__':
    sleep(1)
    main()
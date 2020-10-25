class CarBase:
    def __init__(self, car_type=None, brand=None, photo_file_name=None, carrying=0.0):
        self.car_type = car_type
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        import os
        return os.path.splitext(self.photo_file_name)[1][0:]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count=0):
        super().__init__("Car", brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, body_volume, carrying):
        super().__init__("Truck", brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.body_length, self.body_width, self.body_height = get_whl(str(body_volume))

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra=None):
        super().__init__("SpecMachine", brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.extra = extra


car_type_index = 0
brand_index = 1
passenger_seats_count_index = 2
photo_file_name_index = 3
body_volume = 4
carrying_index = 5
extra_index = 6


def get_whl(whl):
    try:
        w, h, l = whl.split("x")
        return w, h, l
    except ValueError:
        return 0.0, 0.0, 0.0


def generate_car(car):
    try:
        photo_file_name = car[photo_file_name_index]
        brand = car[brand_index]
        carrying = car[carrying_index]
        if car[car_type_index] == "car":
            passenger_seats_count = car[passenger_seats_count_index]
            if passenger_seats_count.isnumeric():
                return Car(photo_file_name=photo_file_name, brand=brand, carrying=carrying)

        if car[car_type_index] == "truck":
            return Truck(photo_file_name=photo_file_name, brand=brand, carrying=carrying,
                         body_volume=get_whl(car[body_volume]))

        if car[car_type_index] == "spec_machine":
            if car[extra_index]:
                return SpecMachine(photo_file_name=photo_file_name, brand=brand, carrying=carrying,
                                   extra=car[extra_index])

        return

    except IndexError:
        return


def get_car_list(file_name):
    import csv
    cars = []
    with open(file_name) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            car = generate_car(row)
            if car:
                cars.append(car)
    return cars


cars = get_car_list("coursera_week3_cars.csv")
print(len(cars))
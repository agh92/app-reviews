import csv


def from_csv(path):
    with open(path) as ids_file:
        csv_reader = csv.reader(ids_file)
        apps = []
        for row in csv_reader:
            apps.append(App(row[0], row[1], row[2]))
    return apps


class App:
    def __init__(self, name, play_id, itunes_id):
        self.itunes_id = itunes_id
        self.play_id = play_id
        self.name = name
        self.reviews = []

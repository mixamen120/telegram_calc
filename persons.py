from database import Requests


class Person:
    def __init__(self, ID):
        self.ID = ID
        self.is_authorized = None
        self.name = None
        self.surname = None
    def authorize(self):
        db = Requests().select_person()
        for i in range(len(db)):
            if db[i]['id_person'] == self.ID:
                self.is_authorized = True
                self.name = db[i]['name']
                self.surname = db[i]['surname']
                break
        if self.is_authorized is None:
            self.is_authorized = False

    def registration(self, name, surname):
        self.name = name
        self.surname = surname
        Requests().add_person(self.ID, self.name, self.surname)
        self.is_authorized = True

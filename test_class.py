class person:
    def __init__(self, age, name, city):
        self.age = age
        self.name = name
        self.city = city
    def change_age(self, new_age):
        self.age = new_age
    def add_to_age(self, years):
        return years+self.age
    

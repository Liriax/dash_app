class person:
    def __init__(self, age):
        self.age = age
    def change_age(self, new_age):
        self.age = new_age
    def add_to_age(self, years):
        return years+self.age
    

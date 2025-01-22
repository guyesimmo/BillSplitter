from dataclasses import dataclass
from util.persons.persons import Person

@dataclass
class Group:

    members: list[Person]

    def add_member(self, person: Person):
        if person not in self.members:
            self.members.append(person) 
        else:
            raise Exception("Person already in Group.")
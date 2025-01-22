from dataclasses import dataclass
from util.persons.persons import Person

@dataclass
class Transaction:
    person_owed: Person
    person_paying: Person
    amount: int
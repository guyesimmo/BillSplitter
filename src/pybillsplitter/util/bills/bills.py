from dataclasses import dataclass
from util.groups.groups import Group
from util.persons.persons import Person

@dataclass
class Bill:
    pass

@dataclass
class SingleBill(Bill):

    bill_payer: Person
    bill_ower: Person
    total_paid: int

@dataclass
class EvenSplitBill(Bill):

    bill_payer: Person
    bill_owers: Group
    total_paid: int

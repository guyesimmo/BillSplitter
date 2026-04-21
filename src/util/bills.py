from .people import Person
from dataclasses import dataclass, field

@dataclass
class OwedAmount:
    person: Person
    amount: float

@dataclass
class Bill:
    paid_by: Person
    amount: float
    owed_list: list[OwedAmount] = field(default_factory=list)

@dataclass
class EvenSplitBill(Bill):
    shared_by: list[Person] = field(default_factory=list)

    def __post_init__(self):
        for person in self.shared_by:
            self.owed_list.append(OwedAmount(person=person, amount=self.amount/len(self.shared_by)))

@dataclass
class SplitBill(Bill):
    
    def __post_init__(self):
        if self.amount != sum([x.amount for x in self.owed_list]):
            raise ValueError("Total amount owed does not match amount paid.")

@dataclass  
class BillCollection:
    bill_list: list[Bill] = field(default_factory=list)
    
    def add_bill(self, bill: Bill):
        self.bill_list.append(bill)

@dataclass
class Transaction:
    from_person: Person
    to_person: Person
    amount: float
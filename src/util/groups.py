from collections import deque

from .people import Person
from .bills import BillCollection, Transaction
from typing import Optional

class Group:
    people: list[Person]
    bill_collection: Optional[BillCollection]

    def __init__(self, people: list = []):
        self.people = people

    def add_person(self, person: Person):
        self.people.append(person)

    def add_bill_collection(self, bill_collection: BillCollection):
        self.bill_collection = bill_collection

    def _calculate_net_balances(self):
        for bill in self.bill_collection.bill_list:
            bill.paid_by.running_balance += bill.amount
            for owed in bill.owed_list:
                owed.person.running_balance = owed.person.running_balance - owed.amount
        self.bill_collection = None
            
    def calculate_split(self) -> list[Transaction]:

        if self.bill_collection:
            self._calculate_net_balances()
            debtors = deque(sorted(
                [(p.running_balance, p.full_name, p) for p in self.people if p.running_balance < 0],
                reverse=True
            ))
            creditors = deque(sorted(
                [(p.running_balance, p.full_name, p) for p in self.people if p.running_balance > 0],
                reverse=True
            ))
            
            transactions = []
            
            while debtors and creditors:
                debt_amt, debtor, debtor_person = debtors.popleft()
                cred_amt, creditor, creditor_person = creditors.popleft()
                
                transfer = min(abs(debt_amt), cred_amt)
                transactions.append(Transaction(from_person=debtor_person, to_person=creditor_person, amount=transfer))
                
                new_debt = debt_amt + transfer
                new_cred = cred_amt - transfer
                
                if new_debt < 0:
                    debtors.appendleft((new_debt, debtor, debtor_person))
                if new_cred > 0:
                    creditors.appendleft((new_cred, creditor, creditor_person))

            for persons in self.people:
                persons.running_balance = 0
            
            return transactions
        
        else:
            raise AttributeError("To calculate a split, a BillCollection must be provided to the Group. Try using add_bill_collection().")
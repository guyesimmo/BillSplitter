from dataclasses import dataclass
from util.persons.persons import Person
from util.groups.groups import Group
from util.bills.bills import Bill, EvenSplitBill, SingleBill
from util.transactions.transactions import Transaction

class BillSplitterService:

    def __init__(self, group: Group):
        self.group: Group = group

    def add_single_bill(self, bill: SingleBill):

        for i in self.group.members:
            if bill.bill_ower == i:
                i.balance = i.balance - bill.total_paid
            elif bill.bill_payer == i:
                i.balance = i.balance + bill.total_paid
            else:
                pass

    def add_even_split_bill(self, bill: EvenSplitBill):

        if bill.bill_payer not in bill.bill_owers.members:
            raise ValueError("Bill Payer Must be in Bill Owers (Include their amount in the bill)...")

        amount_owed = bill.total_paid / len(bill.bill_owers.members)

        total_owed = bill.total_paid - amount_owed

        bill.bill_owers.members.remove(bill.bill_payer)

        for i in self.group.members:
            if i == bill.bill_payer:
                i.balance += total_owed
            elif i in bill.bill_owers.members:
                i.balance -= amount_owed

    def return_transactions(self) -> list[Transaction]:

        transaction_list = []
        balances = [x.balance for x in self.group.members]

        while len([b for b in balances if b != 0]) > 1:
            
            balances = [x.balance for x in self.group.members]
            payer = min(balances)
            payer_index = balances.index(payer)
            receiver = max(balances)
            receiver_index = balances.index(receiver)
            amount = min(-payer, receiver)

            transaction = Transaction(self.group.members[receiver_index], self.group.members[payer_index], amount)

            transaction_list.append(transaction)
            self.group.members[receiver_index].balance -= amount
            self.group.members[payer_index].balance += amount

        return transaction_list
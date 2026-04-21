import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.util.bills import SplitBill, EvenSplitBill, BillCollection, OwedAmount
from src.util.groups import Group
from src.util.people import Person

alice = Person(full_name="Alice")
robert = Person(full_name="Robert")
charlie = Person(full_name="Charlie")

group = Group([robert, charlie])
group.add_person(alice)

bill_1 = EvenSplitBill(
    paid_by=alice,
    amount=50,
    shared_by=[alice, robert, charlie]
)

bill_2 = SplitBill(
    paid_by=robert,
    amount=100,
    owed_list=[
        OwedAmount(alice, 20),
        OwedAmount(charlie, 50),
        OwedAmount(robert, 30)
    ]
)

bills = BillCollection(
    bill_list=[bill_1, bill_2]
)

group.add_bill_collection(bills)

for bill in group.bill_collection.bill_list:
    if isinstance(bill, EvenSplitBill):
        print(f"{bill.paid_by.full_name} Paid a bill for {bill.amount}, split equally between: {[x.person.full_name for x in bill.owed_list]}")
    elif isinstance(bill, SplitBill):
        print(f"{bill.paid_by.full_name} Paid a bill for {bill.amount}, split as: {[f"{x.person.full_name}, £{x.amount}" for x in bill.owed_list]}")
    else:
        pass

res = group.calculate_split()

for transactions in res:
    print(f"{transactions.from_person.full_name} Owes {transactions.to_person.full_name} £{round(transactions.amount)}")
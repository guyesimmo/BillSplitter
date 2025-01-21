from util.groups.groups import Group
from util.persons.persons import Person
from util.services.bill_splitter_service import BillSplitterService
from util.bills.bills import Bill, EvenSplitBill, SingleBill


def main():
    
    guy: Person = Person(name="Guy")
    miles: Person = Person(name="Miles")
    robert: Person = Person(name="Robert")

    my_group: Group = Group(members = [])
    my_group.add_member(guy)
    my_group.add_member(miles)
    my_group.add_member(robert)

    single_bill = SingleBill(miles, guy, 10)
    single_bill_2 = SingleBill(guy, robert, 30)
    group_bill = EvenSplitBill(miles, Group([miles, robert, guy]), 100)

    bill_splitter = BillSplitterService(my_group)

    bill_splitter.add_single_bill(single_bill)
    bill_splitter.add_single_bill(single_bill_2)
    bill_splitter.add_even_split_bill(group_bill)

    transactions = bill_splitter.return_transactions()

    for transaction in transactions:
        print(transaction.person_paying.name + " owes: " + transaction.person_owed.name + " " + str(transaction.amount))

if __name__ == "__main__":
    main()
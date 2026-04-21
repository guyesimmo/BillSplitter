import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.util.bills import SplitBill, EvenSplitBill, Bill, BillCollection, OwedAmount, Transaction
from src.util.people import Person
from src.util.groups import Group

class TestBillSplitting:

    @pytest.fixture
    def setup_test_bills(self):
        rob = Person("Rob")
        david = Person("David")
        miles = Person("Miles")

        bill_1 = EvenSplitBill(
            paid_by=rob,
            amount=60,
            shared_by=[rob, david, miles]
        )

        bill_2 = SplitBill(
            paid_by=rob,
            amount=100,
            owed_list=[
                OwedAmount(rob, 20),
                OwedAmount(david, 50),
                OwedAmount(miles, 30)
            ]
        )

        yield rob, david, miles, bill_1, bill_2
    
    def test_bill_collections(self, setup_test_bills):

        rob, david, miles, bill_1, bill_2 = setup_test_bills

        bill_collection = BillCollection()

        bill_collection.add_bill(bill=bill_1)
        bill_collection.add_bill(bill=bill_2)

        assert len(bill_collection.bill_list) == 2

    def test_calculate_group_net_balances(self, setup_test_bills):

        rob, david, miles, bill_1, bill_2 = setup_test_bills

        group = Group(
            people=[rob, david, miles]
        )

        bill_collection = BillCollection()

        bill_collection.add_bill(bill=bill_1)
        bill_collection.add_bill(bill=bill_2)

        group.add_bill_collection(bill_collection=bill_collection)

        group._calculate_net_balances()

        assert group.people[0].running_balance == 120.0
        assert group.people[1].running_balance == -70.0
        assert group.people[2].running_balance == -50.0

        assert sum([x.running_balance for x in group.people]) == 0

    def test_calculate_full_bill_split(self, setup_test_bills):

        rob, david, miles, bill_1, bill_2 = setup_test_bills

        group = Group(
            people=[rob, david, miles]
        )

        bill_collection = BillCollection()

        bill_collection.add_bill(bill=bill_1)
        bill_collection.add_bill(bill=bill_2)

        group.add_bill_collection(bill_collection=bill_collection)

        result = group.calculate_split()

        assert result == [
            Transaction(from_person=miles, to_person=rob, amount=50.0), 
            Transaction(from_person=david, to_person=rob, amount=70.0)
        ]

        assert all(isinstance(item, Transaction) for item in result)

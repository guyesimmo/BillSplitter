import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.util.bills import SplitBill, EvenSplitBill, Bill, BillCollection, OwedAmount
from src.util.people import Person

class TestBills:

    @pytest.fixture
    def setup_test_persons(self):
        rob = Person("Rob")
        david = Person("David")
        miles = Person("Miles")

        yield rob, david, miles

    def test_even_split_bill(self, setup_test_persons):
        
        person_1, person_2, person_3 = setup_test_persons
        amount=90

        even_bill = EvenSplitBill(
            paid_by=person_1,
            amount=amount,
            shared_by=[
                person_1,
                person_2,
                person_3
            ]
        )

        assert isinstance(even_bill, Bill)
        for item in even_bill.owed_list:
            assert item.amount == amount/len(even_bill.shared_by)

    def test_uneven_split_bill(self, setup_test_persons):
        person_1, person_2, person_3 = setup_test_persons
        amount = 100

        uneven_bill = SplitBill(
            paid_by=person_1,
            amount=amount,
            owed_list=[
                OwedAmount(person=person_1, amount=20),
                OwedAmount(person=person_2, amount=50),
                OwedAmount(person=person_3, amount=30)
            ]
        )

        assert isinstance(uneven_bill, Bill)

    def test_uneven_split_bill_value_error(self, setup_test_persons):
        person_1, person_2, person_3 = setup_test_persons
        amount = 100

        with pytest.raises(ValueError, match="Total amount owed does not match amount paid") as exc_info:
            uneven_bill = SplitBill(
                paid_by=person_1,
                amount=amount,
                owed_list=[
                    OwedAmount(person=person_1, amount=amount/2),
                    OwedAmount(person=person_2, amount=amount/2),
                    OwedAmount(person=person_3, amount=amount/2)
                ]
            )

            assert str(exc_info.value) == "Total amount owed does not match amount paid."
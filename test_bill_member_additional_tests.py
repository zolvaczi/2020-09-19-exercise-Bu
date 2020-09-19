import datetime
import unittest

import bill_member
from tariff import BULB_TARIFF as tariff

class TestBillMember(unittest.TestCase):

    def test_calculate_bill_for_august(self):
        amount, kwh = bill_member.calculate_bill(member_id='member-123',
                                                 account_id='ALL',
                                                 bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)

    def test_no_member_data(self):
        self.assertRaises(bill_member.MemberNotFound,
                          bill_member.calculate_bill(member_id='joe-lycett',
                                                     account_id='ALL',
                                                     bill_date='2017-08-31'))

    #1. data points
    #    1. bill date is an exact date match with a reading date
    def test_exact_date_match_1(self):
        r = {'m': [{'a': [{'gas': [
                    {'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z', 'unit': 'kWh'},
                    {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z', 'unit': 'kWh'},
                    {'cumulative': 18002, 'readingDate': '2017-05-08T00:00:00.000Z', 'unit': 'kWh'},
                    {'cumulative': 18270, 'readingDate': '2017-06-18T00:00:00.000Z', 'unit': 'kWh'}]}]}]}

        amount, kwh = bill_member.calculate_bill(member_id='m',
                                                 account_id='ALL',
                                                 bill_date='2017-05-08',
                                                 readings=r)

        self.assertEqual(amount, 7*24.56)
        self.assertEqual(kwh, 167)


    #    1. extrapolation from last two readings
    #    1. only one reading is available (assumption: this is not an error, only standing charge applied in this case*)
    #    1. no data points at all (assumption: this is an error*)
    #1. bill dates
    #    1. end of month
    #    1. not the last day of a month
    #    1. no date specified: current month's last day (assumption*)
    #1. meters: member has
    #    1. gas meter
    #    1. electricity meter
    #    1. both
    #    1. none (assumption: this is an error*)
    #1. accounts
    #    1. member has one account
    #    1. member has more accounts
    #    1. member has no account (assumption: this is an error*)
    #1. units
    #    1. electricity/gas consumption specified in kWh
    #    1. gas consumption specified in cubic meters (assumption*)


if __name__ == '__main__':
    unittest.main()

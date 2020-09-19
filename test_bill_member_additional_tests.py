"""
Additional unit test module for the edge cases listed in README.md
"""

import unittest
import bill_member

class TestBillPerMeter(unittest.TestCase):
    #1. data points
    #    1. bill date is an exact date match with a reading date
    def test_exact_date_match_1(self):
        m = [{'cumulative': 18270, 'readingDate': '2017-06-18T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18453, 'readingDate': '2017-07-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18620, 'readingDate': '2017-08-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18682, 'readingDate': '2017-09-10T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)

    def test_exact_date_match_2(self):
        m = [{'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2017-05-08T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2017-05-08')

        self.assertEqual(amount, 12.12) #round(8*24.56 + round((18002-17759)/23*8)*11.949)/100
        self.assertEqual(kwh, 85) #round((18002-17759)/23*8)

    #    1. extrapolation from last two readings
    def test_extrapolation_1(self):
        m = [{'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2017-05-08T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2017-05-09')

        self.assertEqual(amount, 13.56) #round(9*24.56 + round((18002-17759)/23*9)*11.949)/100
        self.assertEqual(kwh, 95) #round((18002-17759)/23*9)

    def test_extrapolation_2(self):
        m = [{'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2017-05-08T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2017-05-31')

        self.assertEqual(amount, 46.81) #round(31*24.56 + round((18002-17759)/23*31)*11.949)/100
        self.assertEqual(kwh, 328) #round((18002-17759)/23*31)

    #    1. only one reading is available (assumption: this is an error*)
    def test_one_reading_only(self):
        m = [{'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z', 'unit': 'kWh'}]

        with self.assertRaises(bill_member.InsufficientNumberOfReadings):
            bill_member.calculate_meter_bill(fuel_type='electricity',
                                             meter_readings=m,
                                             bill_date='2017-05-31')

    #    1. no data points at all (assumption: this is an error*)
    def test_no_reading_avaialble(self):
        with self.assertRaises(bill_member.InsufficientNumberOfReadings):
            bill_member.calculate_meter_bill(fuel_type='electricity',
                                             meter_readings=[],
                                             bill_date='2017-05-31')

    #1. bill dates
    #    1. end of month -> see: test_extrapolation_2
    #    1. not the last day of a month -> see: test_extrapolation_1
    #    1. no date specified: (assumption: error*)
    def test_no_date_specififed_1(self):
        with self.assertRaises(bill_member.InvalidBillingDate):
            bill_member.calculate_meter_bill(fuel_type='electricity',
                                             meter_readings=[],
                                             bill_date=None)

    def test_no_date_specififed_2(self):
        with self.assertRaises(bill_member.InvalidBillingDate):
            bill_member.calculate_meter_bill(fuel_type='electricity',
                                             meter_readings=[],
                                             bill_date='')

    #    1. test for leap years
    def test_leap_year_1(self):
        m = [{'cumulative': 17580, 'readingDate': '2020-01-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2020-02-15T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2020-03-08T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2020-03-31')

        self.assertEqual(amount, 48.48) # round(31*24.56 + round((18002-17759)/22*31)*11.949)/100
        self.assertEqual(kwh, 342) # round((18002-17759)/22*31)

    def test_leap_year_2(self):
        m = [{'cumulative': 17580, 'readingDate': '2020-01-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2020-02-15T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2020-03-08T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2020-03-08')

        self.assertEqual(amount, 12.48) # round(8*24.56 + round((18002-17759)/22*8)*11.949)/100
        self.assertEqual(kwh, 88) # round((18002-17759)/22*8)

    def test_leap_year_3(self):
        m = [{'cumulative': 17580, 'readingDate': '2020-01-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2020-02-29T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2020-03-08T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2020-03-08')

        self.assertEqual(amount, 31.0) # round(8*24.56 + (18002-17759)*11.949)/100
        self.assertEqual(kwh, 243) # 18002-17759

    def test_leap_year_4(self):
        m = [{'cumulative': 17580, 'readingDate': '2020-01-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2020-02-29T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2020-03-08T00:00:00.000Z', 'unit': 'kWh'}]

        amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                       meter_readings=m,
                                                       bill_date='2020-02-29')

        self.assertEqual(amount, 26.48) # round(29*24.56 + round((17759-17580)/32*29)*11.949)/100
        self.assertEqual(kwh, 162) # round((17759-17580)/32*29)

#1. yearly total charges == sum of monthly bills?
    def test_yearly_total(self):
        """sum of monthly bills should roughly equal to yearly charges
        (the deltas will only hold if readings are from end of the month)
        with intra-month readings, we would need to record the last billed kWhs
        and produce the next bill with that 'reading'"""

        m = [{'cumulative': 17580, 'readingDate': '2017-03-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 17759, 'readingDate': '2017-04-30T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18002, 'readingDate': '2017-05-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18270, 'readingDate': '2017-06-30T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18453, 'readingDate': '2017-07-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18620, 'readingDate': '2017-08-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18682, 'readingDate': '2017-09-30T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 18905, 'readingDate': '2017-10-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 19150, 'readingDate': '2017-11-30T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 19517, 'readingDate': '2017-12-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 19757, 'readingDate': '2018-01-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 20090, 'readingDate': '2018-02-28T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 20276, 'readingDate': '2018-03-31T00:00:00.000Z', 'unit': 'kWh'},
             {'cumulative': 20600, 'readingDate': '2018-04-30T00:00:00.000Z', 'unit': 'kWh'}]

        bill_dates = ['2017-04-30', '2017-05-31', '2017-06-30', '2017-07-31', '2017-08-31', '2017-09-30',
                      '2017-10-31', '2017-11-30', '2017-12-31', '2018-01-31', '2018-02-28', '2018-03-31']

        total_amount = 0.0
        total_kwh = 0

        for d in bill_dates:
            amount, kwh = bill_member.calculate_meter_bill(fuel_type='electricity',
                                                           meter_readings=m,
                                                           bill_date=d)
            total_amount += amount
            total_kwh += kwh

        expected_amount = 411.79 #round((20276-17580)*11.949 + 365*24.56)/100
        expected_kwh = 2696 #20276-17580

        self.assertAlmostEqual(total_kwh, expected_kwh, delta=6)
        self.assertAlmostEqual(total_amount, expected_amount, delta=0.12)

class TestBillMember(unittest.TestCase):
    def test_calculate_bill_for_august(self):
        amount, kwh = bill_member.calculate_bill(member_id='member-123',
                                                 account_id='ALL',
                                                 bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)

    #1. meters: member has
    #    1. gas meter
    def test_one_account_with_gas(self):
        r = {'m': [{'a': [{'gas': [
                    {'cumulative': 17759, 'readingDate': '2017-04-30T00:00:00.000Z', 'unit': 'kWh'},
                    {'cumulative': 18002, 'readingDate': '2017-05-31T00:00:00.000Z', 'unit': 'kWh'}]}]},
                   ]}

        amount, kwh = bill_member.calculate_bill(member_id='m',
                                                 account_id='ALL',
                                                 bill_date='2017-05-31',
                                                 readings=r)

        self.assertEqual(amount, 16.85) #round(31*24.56 + (18002-17759)*3.8)/100
        self.assertEqual(kwh, 243)

    #    1. electricity meter
    def test_one_account_wit_electricity(self):
        r = {'m': [{'a': [{'electricity': [
                    {'cumulative': 17759, 'readingDate': '2017-04-30T00:00:00.000Z', 'unit': 'kWh'},
                    {'cumulative': 18002, 'readingDate': '2017-05-31T00:00:00.000Z', 'unit': 'kWh'}]}]},
                   ]}

        amount, kwh = bill_member.calculate_bill(member_id='m',
                                                 account_id='ALL',
                                                 bill_date='2017-05-31',
                                                 readings=r)

        self.assertEqual(amount, 36.65) #round(31*24.56 + (18002-17759)*11.949)/100
        self.assertEqual(kwh, 243)

    #    1. both
    def test_one_account_wit_dual_fuel(self):
        r = {'m': [{'a': [
                          {'gas': [
                            {'cumulative': 17759, 'readingDate': '2017-04-30T00:00:00.000Z', 'unit': 'kWh'},
                            {'cumulative': 18002, 'readingDate': '2017-05-31T00:00:00.000Z', 'unit': 'kWh'}]},
                          {'electricity': [
                            {'cumulative': 17759, 'readingDate': '2017-04-30T00:00:00.000Z', 'unit': 'kWh'},
                            {'cumulative': 18002, 'readingDate': '2017-05-31T00:00:00.000Z', 'unit': 'kWh'}]}
                    ]}]}

        amount, kwh = bill_member.calculate_bill(member_id='m',
                                                 account_id='ALL',
                                                 bill_date='2017-05-31',
                                                 readings=r)

        self.assertEqual(amount, 53.5) #round(31*24.56*2 + (18002-17759)*3.8 + (18002-17759)*11.949)/100
        self.assertEqual(kwh, 243*2)

    #    1. none (assumption: this is an error*)
    #1. accounts
    #    1. member has more accounts
    def test_two_accounts_by_one_meter(self):
        r = {'m': [{'acc-a': [{'electricity': [
                    {'cumulative': 17759, 'readingDate': '2017-04-30T00:00:00.000Z', 'unit': 'kWh'},
                    {'cumulative': 18002, 'readingDate': '2017-05-31T00:00:00.000Z', 'unit': 'kWh'}]}]},
                   {'acc-b': [{'electricity': [
                    {'cumulative': 17759, 'readingDate': '2017-04-30T00:00:00.000Z', 'unit': 'kWh'},
                    {'cumulative': 18002, 'readingDate': '2017-05-31T00:00:00.000Z', 'unit': 'kWh'}]}]}
                   ]}

        amount, kwh = bill_member.calculate_bill(member_id='m',
                                                 account_id='ALL',
                                                 bill_date='2017-05-31',
                                                 readings=r)

        self.assertEqual(amount, 36.65*2) #round(31*24.56 + (18002-17759)*11.949)/100*2
        self.assertEqual(kwh, 243*2)

    #    1. member has no account (assumption: this is an error*)
    def test_no_member_data(self):
        with self.assertRaises(bill_member.MemberNotFound):
            bill_member.calculate_bill(member_id='joe-lycett',
                                       account_id='ALL',
                                       bill_date='2017-08-31')

    #1. units
    #    1. electricity/gas consumption specified in kWh -> see other tests
    #    1. gas consumption specified in cubic meters (assumption*)

if __name__ == '__main__':
    unittest.main()

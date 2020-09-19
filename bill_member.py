import load_readings
import tariff
from dateutil.parser import parse

class MemberNotFound(Exception):
    """Raised when a member is not found in the data set"""
    def __init__(self, member_id):
        self.member_id=member_id

class InsufficientNumberOfReadings(Exception):
    """Raised when there is less than 2 readings which is necessary to calculate the consumption"""
    pass

class InvalidBillingDate(Exception):
    """Raised when there is less than 2 readings which is necessary to calculate the consumption"""
    def __init__(self, billing_date):
        self.billing_date=billing_date

def calculate_meter_bill(fuel_type, meter_readings, bill_date):
    """A 2-sample linear extrapolation to calculate the meter's consumption and charge"""
    # converting dates to datetime:
    try:
        bill_date_dt = parse(bill_date, ignoretz=True)
    except:
        raise InvalidBillingDate(bill_date)

    for r in meter_readings:
        r['dt'] = parse(r['readingDate'], ignoretz=True)
        r['dt'] = parse(r['readingDate'], ignoretz=True)
    past_readings = [r for r in meter_readings if r['dt'] <= bill_date_dt]
    if len(past_readings) < 2:
        raise InsufficientNumberOfReadings()

    #TODO: convert gas readings to kWh
    for r in past_readings[-2:]:
        if fuel_type=='gas' and r['unit'] != 'kWh':
            raise NotImplementedError('conversion from cubic meters to kWh not implemented yet')

    latest = past_readings[-1]
    previous = past_readings[-2]
    daily_avg_consumption = (latest['cumulative'] - previous['cumulative']) / (latest['dt'] - previous['dt']).days
    fuel_tariff = tariff.BULB_TARIFF[fuel_type]
    num_days_to_bill = bill_date_dt.day
    consumption = round(daily_avg_consumption * num_days_to_bill)
    consumption_charge = consumption * fuel_tariff['unit_rate']
    standing_charge = num_days_to_bill * fuel_tariff['standing_charge']

    return round(consumption_charge + standing_charge)/100, consumption

readings = load_readings.get_readings()

def calculate_bill(member_id=None, account_id=None, bill_date=None, readings=readings):
    """
    The function returns the bill amount and
    :param member_id: member identification string
    :param account_id: account ID of the member or the string 'ALL' to indicate all of their accounts
    :param bill_date: billing date as string in the form 'YYYY-MM-DD', always the last day of a month
    :return: tuple of (bill_amount -> float, kwh -> int)
    """
    return
    results_per_meters = []    # (amount, kwh) tuples per meter

    try:
        member_accounts = readings[member_id]
    except KeyError:
        raise MemberNotFound(member_id)

    for account in member_accounts:
        if account_id == 'ALL' or account_id in account:
            for meters in account.values()[0]:
                for meter in meters:
                    for (fuel_type, meter_readings) in meters.iteritems():
                        results_per_meters.append(calculate_meter_bill(fuel_type,
                                                                       meter_readings,
                                                                       bill_date))
    # sum the (amount, kwh) tuples:
    return list(map(sum, zip(*results_per_meters)))

    {'member-123': [{'account-abc': [{'electricity': [
        {'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 18002, 'readingDate': '2017-05-08T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 18270, 'readingDate': '2017-06-18T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 18453, 'readingDate': '2017-07-31T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 18620, 'readingDate': '2017-08-31T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 18682, 'readingDate': '2017-09-10T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 18905, 'readingDate': '2017-10-27T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 19150, 'readingDate': '2017-11-04T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 19517, 'readingDate': '2017-12-31T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 19757, 'readingDate': '2018-01-23T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 20090, 'readingDate': '2018-02-19T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 20276, 'readingDate': '2018-03-14T00:00:00.000Z', 'unit': 'kWh'},
        {'cumulative': 20600, 'readingDate': '2018-04-29T00:00:00.000Z', 'unit': 'kWh'}]}]}]}

def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))

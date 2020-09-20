"""
Low-level: calculate consumption and charges from a single series of meter readings (calculate_meter_bill function)
Higher-level: apply the above to each meter and each account of the member (calculate_bill function)
"""

from dateutil.parser import parse
import pytz
import load_readings
import tariff

class MemberNotFound(Exception):
    """Raised when a member is not found in the data set"""
    def __init__(self, member_id):
        self.member_id=member_id

class InsufficientNumberOfReadings(Exception):
    """Raised when there is less than 2 readings which is necessary to calculate the consumption"""

class InvalidBillingDate(Exception):
    """Wrong billing date format"""
    def __init__(self, billing_date):
        self.billing_date=billing_date

def calculate_meter_bill(fuel_type, meter_readings, bill_date):
    """A 2-sample linear extrapolation to calculate the meter's consumption and charge"""
    # converting dates to datetime:
    try:
        #Note: the following is dangerous, you should never do this in a production server.
        # Timezone should be properly specified in the input. This code challenge is about a backend system,
        #        and the best practice for machine-2-machine interfaces is to always include TZ information.
        # In a front-end application, input from a user should be assumed to be local time and for instance,
        #       parse(bill_date).astimezone(pytz.UTC) would correctly adjust the time to UTC from local time
        bill_date_dt = parse(bill_date).replace(tzinfo=pytz.UTC)
    except:
        raise InvalidBillingDate(bill_date)

    for r in meter_readings:
        r['dt'] = parse(r['readingDate'])
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

default_reading_source = load_readings.get_readings()

def calculate_bill(member_id=None, account_id=None, bill_date=None, readings=default_reading_source):
    """
    The function returns the bill amount and
    :param member_id: member identification string
    :param account_id: account ID of the member or the string 'ALL' to indicate all of their accounts
    :param bill_date: billing date as string
    :param readings: for test purposes, the default data source can be overridden
    :return: tuple of (bill_amount -> float, kwh -> int)
    """
    results_per_meters = []    # (amount, kwh) tuples per meter

    try:
        member_accounts = readings[member_id]
    except KeyError:
        raise MemberNotFound(member_id)

    for account in member_accounts:
        if account_id == 'ALL' or account_id in account:
            for meters in list(account.values()):
                for meter in meters:
                    for (fuel_type, meter_readings) in meter.items():
                        results_per_meters.append(calculate_meter_bill(fuel_type,
                                                                       meter_readings,
                                                                       bill_date))
    # sum the (amount, kwh) tuples:
    return list(map(sum, zip(*results_per_meters)))


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

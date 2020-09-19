import load_readings

class MemberNotFound(Exception):
    """Raised when a member is not found in the data set"""
    def __init__(self, member_id):
        self.member_id=member_id

class DataPoints:
    """Class to provide readings for each matching account/meter"""
    def __init__(self, data=None):
        """
        Constructor
        :param data: used for test purposes to inject test data to the instance, by default data is read from the load_readings module
        """
        self.data = data or load_readings.get_readings()

    def get_data_point_pairs(self, member_id, account_id, billing_date):
        """
        Get a list of the last two readings before the specified date in a unified form:
        - one pair per meter
        - possibly from multiple accounts of the member
        - TODO: All units are converted to kWh.
        :param member_id:
        :param account_id:
        :param billing_date:
        :return: a list of data point pairs for each meter of the member
        """
        try:
            member_data = self.data[member_id]
        except KeyError:
            raise MemberNotFound(member_id)


default_data = DataPoints()

def calculate_bill(member_id=None, account_id=None, bill_date=None, readings=default_data):
    """
    The function returns the bill amount and
    :param member_id: member identification string
    :param account_id: account ID of the member or the string 'ALL' to indicate all of their accounts
    :param bill_date: billing date as string in the form 'YYYY-MM-DD', always the last day of a month
    :return: tuple of (bill_amount -> float, kwh -> int)
    """
    # prechecks:
    # check if date is the last day of a month

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

    return amount, kwh


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

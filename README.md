# Billing Coding Challenge 2020-09-19

<h2 id="overview">Overview</h2>
<p>In this challenge, we’d like you to write a small program which, given a set of meter readings, computes a member’s monthly energy bill. To do this, we have stubbed out the following files for you:</p>
<ul>
<li>bill_member.py, which contains functions to compute the customer bill and print it to screen.<ul>
<li>You should implement <code>calculate_bill</code>. This is the entry point to your solution.</li>
<li><code>calculate_bill</code> is currently hardcoded to give the correct answer for August 2017.</li>
<li>There’s no need to change <code>calculate_and_print_bill</code>.</li>
</ul>
</li>
<li><code>test_bill_member.py</code>, a test module for bill_member.</li>
<li><code>main.py</code>, the entry point for the program, there’s no need to make changes to this module.</li>
<li><code>tariff.py</code>, prices by kWh for all energy</li>
<li><code>load_readings.py</code>, provides a function for loading the readings from the given json.</li>
<li><code>readings.json</code>, contains a set of monthly meter readings for a given year, member and fuel</li>
</ul>
<p>We’d like you to:</p>
<ul>
<li>Implement the calculate_bill function, so that given a member_id, optional account argument and billing date, we can compute the bill for the customer.</li>
</ul>
<p>We do not want you to spend time on:</p>
<ul>
<li>Making this backwards compatible with python &lt;= 3.</li>
</ul>
<p>You can assume:</p>
<ul>
<li>All times are UTC.</li>
<li>We’re only dealing with £ denominated billing.</li>
<li>You only need to handle electricity and gas billing.</li>
<li>Energy is consumed linearly.</li>
<li>The billing date is the last day of the month.</li>
<li>Readings are always taken at midnight.</li>
<li>There is only one meter reading per billing period.</li>
<li>The JSON file structure will remain the same in any follow on exercise.</li>
</ul>

## Analysis
###Problem breakdown:
1. Low-level: calculate consumption and charges from a single series of meter readings
1. Higher-level: apply the above to each meter and each account of the member

###Edge cases considered
1. data points
    1. bill date is an exact date match with a reading date
    1. extrapolation from last two readings
    1. only one reading is available (assumption: this is an error*) 
    1. no data points at all (assumption: this is an error*)
1. bill dates
    1. end of month
    1. not the last day of a month
    1. no date specified  (assumption: this is an error*)
    1. test for leap years
1. yearly total charges == sum of monthly bills (roughly: max rounding error: 12*.5=6 kWh, and 12*£0.005*2=£0.12)
1. meters: member has 
    1. gas meter
    1. electricity meter
    1. both
    1. none (assumption: this is an error*)
1. accounts
    1. member has one account
    1. member has more accounts
    1. member has no account (assumption: this is an error*)
1. units
    1. electricity/gas consumption specified in kWh
    1. gas consumption specified in cubic meters (conversion formula to be provided*)

*normally, assumed edge case should be verified and approved by the product manager before implementation
    
## Further Assumptions
1. No JSON schema has been provided and the JSON sample was very small, therefore the structure had be guessed.
1. It is assumed that the datasource is static during the runtime of this application, and therefore it is only read once.
1. extrapolation to a date before first available reading is not a valid business logic use-case
1. only one reading (starting reading) is assumed to be an invalid use-case for billing
1. VAT is not considered by this function, it could be applied to the total bill by a higher-level module/function (where the total can be adjusted by discounts, for instance)
1. scaling was not considered at this level of implementation, scalability could be solved at a higher level of the architecture, e.g. to decompose requests to processing individual members or smaller batches of members parallel, with data partitioning...
1. Leaving customers need a final bill, in which case billing date may fall to other than last day of the month
1. abstraction: normally, I would implement some sort of interface class to access the data, to decouple it from the underlying data structure + datasource implementation (see assumption "The JSON file structure will remain the same")
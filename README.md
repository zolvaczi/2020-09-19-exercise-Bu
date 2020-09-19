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
1. edge cases considered*
    1. data points
        1. bill date is an exact date match with a reading date
        1. extrapolation from last two readings
        1. only one reading is available (assumption: this is not an error, only standing charge applied in this case*) 
        1. no data points at all (assumption: this is an error*)
    1. bill dates
        1. end of month
        1. not the last day of a month
        1. no date specified: current month's last day (assumption*)
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
        1. gas consumption specified in cubic meters (assumption*)

*assumed edge case should be verified and approved by the product manager before implementation
    
## Further Assumptions
1. It is assumed that the datasource is static during the runtime of this application, and therefore it is only read once.
1. extrapolation to past values is not a supported business logic use-case
1. VAT is not considered by this function, it will be applied to the total bill by a higher-level module/function (which can be adjusted by discounts, for instance)
1. scaling was not considered at this level of implementation, scalability could be solved at a higher level of the architecture, e.g. to decompose requests to processing individual members or smaller batches of members, with data partitioning...
1. linear inter-/extrapolation is sufficient, however it should be easy to change to a different method should there be a specific future business requirement.
1. Leaving customers need a final bill, so bill dates may fall to other than last day of month

## Further Considerations
1. Use third-party/standard libraries for interpolation and extrapolation (`numpy`, etc.)
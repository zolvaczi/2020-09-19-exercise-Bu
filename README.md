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



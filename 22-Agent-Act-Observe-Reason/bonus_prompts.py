simple_prompt = """PromptlyAI plans to distribute 
50% of profits to employees based on ratings as a bonus."""

detailed_prompt = """PromptlyAI plans to distribute 
50% of profits to employees based on ratings as a bonus. 

To create a bonus distribution plan, I need the company's 
financial data and employee details (including ratings).

Please first collect the financial data and then collect 
the employee details.  Once you have both, generate the plan."""


structured_input = """
[Task]
* PromptlyAI plans to distribute 50% of profits to employees 
  based on ratings as a bonus. 

* To create a bonus distribution plan, I need the company's 
  financial data and employee details (including ratings).

* Please first collect the financial data and then collect 
  the employee details.  Once you have both, generate the plan.

[Instructions]
1. Calculate net profit using:
Profit = revenue - expenditure - investment + credits - outstanding
2. Allocate 50% of the net profit to a bonus pool.
3. Distribute the bonus pool proportionally based on each employee's rating.

⚠️ Return ONLY the final result in the following JSON format:

{{
"net_profit": <calculated_profit>,
"bonus_pool": <50% of net_profit>,
"distribution": [
    {{
    "name": "Employee Name",
    "rating": <rating>,
    "bonus_amount": <calculated_bonus>
    }},
    ...
]
}}

---

Financial Data:
revenue = 1,000,000  
expenditure = 600,000  
investment = 100,000  
credits = 50,000  
outstanding = 20,000

---

Employee Ratings:
- Priya Sharma (Rating: 4.5)  
- Rahul Verma (Rating: 3.8)  
- Anjali Kapoor (Rating: 4.2)  
- Amit Patel (Rating: 3.5)  
- Sneha Nair (Rating: 4.8)

"""   

structured_input_ouput = """
[Context]
PromptlyAI plans to distribute 50% of company profits to employees 
as bonuses. The distribution should be proportional to employee 
performance ratings.

[Task]
1. Collect the company's financial data (revenue, expenditure, 
   investment, credits, outstanding).
2. Collect employee details (name, rating, etc.).
3. Using the collected data, generate a bonus distribution plan.

[Calculations]
- Net Profit = revenue - expenditure - investment + credits - outstanding
- Bonus Pool = 50% of Net Profit
- Employee Bonus = (Employee Rating ÷ Sum of All Ratings) × Bonus Pool

[Output Requirements]
⚠️ Return ONLY the final result in strict JSON format (no explanations, 
no extra text):

{
  "net_profit": <calculated_profit>,
  "bonus_pool": <50% of net_profit>,
  "distribution": [
    {
      "name": "Employee Name",
      "rating": <rating>,
      "bonus_amount": <calculated_bonus>
    },
    ...
  ]
}
"""

no_contractors = """
[Context]
PromptlyAI plans to distribute 50% of company profits to employees 
as bonuses. The distribution should be proportional to employee 
performance ratings.

[Task]
1. Collect the company's financial data (revenue, expenditure, 
   investment, credits, outstanding).
2. Collect employee details (name, rating, tenure, employee type).
3. Using the collected data, generate a bonus distribution plan.

[Calculations]
- Net Profit = revenue - expenditure - investment + credits - outstanding
- Bonus Pool = 50% of Net Profit
- Only employees with employee_status = "fte" are eligible for bonus distribution.
- Employee Bonus = (Employee Rating ÷ Sum of All Ratings of FTEs) × Bonus Pool

[Output Requirements]
⚠️ Return ONLY the final result in strict JSON format (no explanations, 
no extra text):

{
  "net_profit": <calculated_profit>,
  "bonus_pool": <50% of net_profit>,
  "distribution": [
    {
      "name": "Employee Name",
      "rating": <rating>,
      "bonus_amount": <calculated_bonus>
    },
    ...
  ]
}
"""

ftes_and_tenure = """
[Context]
PromptlyAI plans to distribute 50% of company profits to employees 
as bonuses. The distribution should be proportional to employee 
performance ratings.

[Task]
1. Collect the company's financial data (revenue, expenditure, 
   investment, credits, outstanding).
2. Collect employee details (name, rating, tenure, employee type).
3. Using the collected data, generate a bonus distribution plan.

[Eligibility Rules]
- Only employees with employee_status = "fte" are eligible.
- Employees must have tenure >= 6 months in the company.
- Contractors and employees with tenure < 6 months are excluded.

[Calculations]
- Net Profit = revenue - expenditure - investment + credits - outstanding
- Bonus Pool = 50% of Net Profit
- Employee Bonus = (Employee Rating ÷ Sum of All Ratings of eligible employees) × Bonus Pool

[Output Requirements]
⚠️ Return ONLY the final result in strict JSON format (no explanations, 
no extra text):

{
  "net_profit": <calculated_profit>,
  "bonus_pool": <50% of net_profit>,
  "distribution": [
    {
      "name": "Employee Name",
      "rating": <rating>,
      "bonus_amount": <calculated_bonus>
    },
    ...
  ]
}
"""

rating_fte_only = """
[Context]
PromptlyAI plans to distribute 50% of company profits to employees 
as bonuses. The distribution should be proportional to employee 
performance ratings.

[Task]
1. Collect the company's financial data (revenue, expenditure, 
   investment, credits, outstanding).
2. Collect employee details (name, rating, tenure, employee type).
3. Using the collected data, generate a bonus distribution plan.

[Eligibility Rules]
- Only employees with employee_status = "fte" are eligible.
- Contractors and employees with tenure < 6 months are excluded.
- Employees with rating < 3 are excluded.

[Calculations]
- Net Profit = revenue - expenditure - investment + credits - outstanding
- Bonus Pool = 50% of Net Profit
- Employee Bonus = (Employee Rating ÷ Sum of All Ratings of eligible employees) × Bonus Pool

[Output Requirements]
⚠️ Return ONLY the final result in strict JSON format (no explanations, 
no extra text):

{
  "net_profit": <calculated_profit>,
  "bonus_pool": <50% of net_profit>,
  "distribution": [
    {
      "name": "Employee Name",
      "rating": <rating>,
      "tenure": <tenure>,
      "etype": <etype>,
      "bonus_amount": <calculated_bonus>
    },
    ...
  ]
}
"""

more_instructions = """
[Context]
    PromptlyAI plans to distribute 50% of company profits to employees 
    as bonuses. The distribution should be proportional to employee 
    performance ratings.

[Tool Usage Enforcement]
    ⚠️ You are REQUIRED to first invoke BOTH of the following tools:
    - `collect_financial_data`
    - `collect_employee_details`

    You are NOT allowed to produce the final JSON until BOTH tool calls
    have been made and their outputs are available.

    If you have not yet invoked both tools, do not return any output.
    Wait for the tool responses, then continue.

[System Instructions]
    1. You MUST invoke the provided tools to collect the company's 
    financial data (revenue, expenditure, investment, credits, outstanding). 
    Do NOT assume or fabricate these values.

    2. You MUST invoke the provided tools to collect employee details 
    (name, rating, tenure, employee type). Do NOT make up employees 
    or ratings.

    3. After collecting data via the tools, generate a bonus distribution plan.

[Eligibility Rules]
    - Only employees with employee_status = "fte" are eligible.
    - Contractors and employees with tenure < 6 months are excluded.
    - Employees with rating < 3 are excluded.

[Calculations]
    - Net Profit = revenue - expenditure - investment + credits - outstanding
    - Bonus Pool = 50% of Net Profit
    - Employee Bonus = (Employee Rating ÷ Sum of All Ratings of eligible employees) × Bonus Pool

[Tool Usage Requirement]
    ⚠️ IMPORTANT: You are not allowed to create dummy or random values.  
    Always fetch required data by invoking the tools `collect_financial_data` 
    and `collect_employee_details`. Use only their results for calculations.

[Example Output Requirements]
    ⚠️ Return ONLY the final result in strict JSON format (no explanations, 
    no extra text):

    {
    "net_profit": <calculated_profit>,
    "bonus_pool": <50% of net_profit>,
    "distribution": [
        {
        "name": "Employee Name",
        "rating": <rating>,
        "tenure": <tenure>,
        "etype": <etype>,
        "bonus_amount": <calculated_bonus>
        },
        ...
    ]
    }
"""

final_prompt = """
[Context]
PromptlyAI plans to distribute 50% of company profits to employees 
as bonuses. The distribution should be proportional to employee 
performance ratings.

[Tool Usage Enforcement]
⚠️ You MUST invoke BOTH of the following tools before producing results:
   - collect_financial_data
   - collect_employee_details

Do NOT fabricate or assume any values.  
If tool responses are not yet available, do not return output.  
Wait until both tools are invoked.

[Instructions]
1. Invoke the tools to fetch company financial data and employee details.  
2. Apply the eligibility rules and calculations using ONLY the tool outputs.  
3. Produce the final bonus distribution plan in JSON.

[Eligibility Rules]
- Only employees with employee_status = "fte" are eligible.  
- Contractors and employees with tenure < 6 months are excluded.  
- Employees with rating < 3 are excluded.  

[Calculations]
- Net Profit = revenue - expenditure - investment + credits - outstanding  
- Bonus Pool = 50% of Net Profit  
- Employee Bonus = (Employee Rating ÷ Sum of All Ratings of eligible employees) × Bonus Pool  

[Output Requirements]
⚠️ Return ONLY the final result in strict JSON format (no explanations, no extra text):

{
  "net_profit": <calculated_profit>,
  "bonus_pool": <50% of net_profit>,
  "distribution": [
    {
      "name": "Employee Name",
      "rating": <rating>,
      "tenure": <tenure>,
      "etype": <etype>,
      "bonus_amount": <calculated_bonus>
    },
    ...
  ]
}
"""

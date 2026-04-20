# agent/knowledge_base.py
# 10 HR policy documents — each covers ONE topic, 100-500 words

HR_DOCUMENTS = [
    {
        "id": "doc_001",
        "topic": "Annual Leave Policy",
        "text": """
Annual Leave Policy — Company HR Handbook

All permanent employees are entitled to 18 days of paid annual leave per calendar year.
Leave accrues at a rate of 1.5 days per month starting from the date of joining.
Employees must apply for annual leave at least 3 working days in advance through the HR portal.
Leave requests are subject to manager approval and team availability.
In cases of emergencies, leave can be applied retrospectively within 2 working days, with manager approval.
Unused annual leave can be carried forward to the next calendar year, subject to a maximum carry-forward limit of 5 days.
Any unused leave beyond 5 days will automatically lapse on December 31st each year and cannot be encashed.
Employees who have not completed 6 months of service are not eligible to take annual leave but will accrue it.
Leave cannot be taken during the probation period (first 3 months) without special approval from HR.
Employees planning to take more than 5 consecutive days must inform HR at least 2 weeks in advance.
Annual leave must not be taken in advance of accrual — negative leave balance requires HR Director approval.
For any leave disputes, employees should contact hr@company.com within 5 working days.
"""
    },
    {
        "id": "doc_002",
        "topic": "Sick Leave Policy",
        "text": """
Sick Leave Policy — Company HR Handbook

All full-time employees are entitled to 10 days of paid sick leave per calendar year.
Sick leave does not carry forward to the next year — any unused sick leave lapses on December 31st.
Sick leave cannot be encashed under any circumstances.
For absences of 1 to 2 days, the employee must notify their manager before 9:30 AM on the day of absence via phone or message.
For absences exceeding 2 consecutive days, a medical certificate from a registered medical practitioner is mandatory.
The medical certificate must be submitted to HR within 2 working days of returning to work.
Sick leave taken immediately before or after a public holiday or annual leave will require a medical certificate regardless of duration.
Repeated sick leave patterns (e.g., frequent Mondays or Fridays) may trigger a wellness review by HR.
Employees who exhaust their sick leave entitlement may apply for unpaid sick leave with HR approval and a doctor's recommendation.
Maternity-related illness is covered under the Maternity Leave Policy, not this Sick Leave Policy.
For mental health-related absences, employees are encouraged to speak confidentially with the HR wellness coordinator.
"""
    },
    {
        "id": "doc_003",
        "topic": "Work From Home Policy",
        "text": """
Work From Home (WFH) Policy — Company HR Handbook

Eligible employees may work from home up to 2 days per week, subject to manager approval.
WFH eligibility begins after completing the 3-month probation period — employees on probation are not eligible for WFH.
WFH requests must be submitted to the line manager every Monday for the upcoming week via the HR portal or email.
Approval is at the manager's discretion based on project requirements and team needs.
Core working hours of 10:00 AM to 4:00 PM must be strictly maintained while working from home.
Employees must be reachable on phone, email, and team communication tools during core hours.
WFH is not permitted on days when the employee has mandatory in-office meetings, client visits, or training sessions.
Employees are responsible for maintaining a professional and distraction-free work environment at home.
All company data security policies apply equally when working from home — VPN must be used at all times.
Misuse of the WFH privilege (e.g., unavailability during core hours) may result in withdrawal of WFH eligibility.
Internet and power outages are the employee's responsibility — WFH cannot be used as a reason for missed deadlines.
"""
    },
    {
        "id": "doc_004",
        "topic": "Payroll and Salary",
        "text": """
Payroll and Salary Policy — Company HR Handbook

All employee salaries are credited to the registered bank account on the last working day of every calendar month.
If the last working day falls on a bank holiday, salary is credited on the preceding working day.
Payslips are generated and made available on the HR portal by the 25th of each month.
Employees must verify their payslip and report discrepancies to payroll@company.com before the 20th of the following month.
Salary deduction queries raised after the 20th will be addressed in the next payroll cycle.
Overtime is applicable for employees in eligible grades only, paid at 1.5 times the basic hourly rate.
Overtime must be pre-approved by the department head in writing before the overtime hours are worked.
Tax deductions (TDS) are applied as per applicable income tax slab rates — employees must submit their investment declarations in April each year.
Salary revisions are processed in April following the annual performance review cycle.
Any salary advance requests must be submitted to HR with justification — a maximum of one month's basic salary can be advanced.
Bank account changes must be communicated to payroll@company.com at least 10 working days before month-end.
"""
    },
    {
        "id": "doc_005",
        "topic": "Maternity and Paternity Leave",
        "text": """
Maternity and Paternity Leave Policy — Company HR Handbook

Maternity Leave:
All female employees who have worked for the company for at least 80 days are entitled to 26 weeks of paid maternity leave.
Maternity leave can begin up to 8 weeks before the expected date of delivery.
In case of miscarriage or medical termination, 6 weeks of paid leave is provided.
Employees must submit a leave application along with a medical certificate from a registered gynaecologist at least 4 weeks before the expected start date.
The company will not terminate or demote an employee on account of maternity leave.

Paternity Leave:
All male employees who have completed 1 year of service are eligible for 15 days of paid paternity leave.
Paternity leave must be taken within 3 months of the child's birth or adoption.
Leave must be applied via the HR portal with a copy of the birth certificate or adoption order.
Paternity leave cannot be split — it must be taken as a single continuous block.
Paternity leave is available for a maximum of 2 children.

Both maternity and paternity leave are in addition to annual leave entitlements.
"""
    },
    {
        "id": "doc_006",
        "topic": "Performance Review Process",
        "text": """
Performance Review Process — Company HR Handbook

The company conducts formal performance reviews twice a year: in April and in October.
The April review covers performance from October to March. The October review covers April to September.
All employees must complete and submit a self-assessment form through the HR portal at least 2 weeks before the review date.
Managers are responsible for completing the review and sharing feedback with the employee within 1 week of the review date.
Performance ratings are: Exceeds Expectations (5), Meets Expectations (3–4), Needs Improvement (1–2).
Employees rated Meets Expectations or above for two consecutive cycles are eligible for a salary increment consideration.
Employees rated Needs Improvement for two consecutive cycles will be placed on a formal Performance Improvement Plan (PIP).
A PIP runs for 60 days with clearly defined targets and weekly check-ins with the manager and HR.
Failure to meet PIP targets may result in disciplinary action, including termination.
Employees who disagree with their review outcome may raise a formal appeal with HR within 5 working days.
"""
    },
    {
        "id": "doc_007",
        "topic": "Code of Conduct",
        "text": """
Code of Conduct — Company HR Handbook

All employees are expected to conduct themselves with professionalism, integrity, and respect in all work-related interactions.
Harassment, bullying, discrimination, or intimidation of any kind — including on the basis of gender, religion, caste, age, disability, or sexual orientation — is strictly prohibited and constitutes a dismissible offence.
Employees must maintain the confidentiality of all proprietary, financial, and personal data they have access to in the course of their work.
Sharing confidential company information with external parties, competitors, or on social media without authorisation is a serious violation of this policy.
Conflicts of interest must be disclosed to HR immediately — employees must not engage in business activities that compete with the company.
The use of company resources (laptops, software, internet) for personal commercial activities is not permitted.
All employees are expected to report ethical violations — including fraud, bribery, or misconduct — via the anonymous ethics hotline at ethics@company.com.
Whistleblowers are protected from retaliation under the company's Whistleblower Protection Policy.
Violations of the Code of Conduct will be investigated by HR and may result in warnings, suspension, or termination.
"""
    },
    {
        "id": "doc_008",
        "topic": "Travel and Expense Reimbursement",
        "text": """
Travel and Expense Reimbursement Policy — Company HR Handbook

All business travel must receive prior written approval from the department head before booking.
Travel bookings must be made through the company's empanelled travel agency or the self-booking portal.
Economy class is mandatory for domestic flights and for international flights under 6 hours.
Business class may be approved for international flights exceeding 6 hours, with VP-level approval.
Hotel accommodation is reimbursed up to Rs 3,500 per night for domestic travel and USD 120 per night for international travel.
Meal allowance: Rs 500 per day within the city; Rs 1,200 per day for outstation travel; USD 40 per day for international travel.
Local conveyance (cab, auto) must be supported by receipts — personal vehicle usage is reimbursed at Rs 7 per km.
All expense claims must be submitted within 15 calendar days of completing the trip.
Claims submitted beyond 15 days will not be reimbursed without a written exception approved by the Finance Head.
Original receipts (or clear digital scans) must be attached to all expense claims above Rs 200.
Expenses for alcohol, personal entertainment, or personal shopping are not reimbursable under any circumstance.
"""
    },
    {
        "id": "doc_009",
        "topic": "Resignation and Exit Policy",
        "text": """
Resignation and Exit Policy — Company HR Handbook

All permanent employees are required to serve a notice period of 60 calendar days upon resignation.
The notice period begins from the date the resignation is formally submitted via the HR portal and acknowledged by the manager.
Notice period buy-out (early exit before completing 60 days) is permitted with mutual written agreement between the employee and company.
The buy-out amount is calculated as the employee's basic salary for the remaining notice period days.
Garden leave may be granted at the company's discretion for senior roles — the employee remains on payroll but does not report to office.
During the notice period, the employee must complete all pending handovers and knowledge transfer as directed by the manager.
An exit interview will be conducted by HR on or before the last working day — attendance is mandatory.
Full and Final (F&F) settlement, including outstanding salary, reimbursements, and gratuity (if applicable), will be processed within 45 days of the last working day.
Separation documents (experience letter, relieving letter) are issued after F&F settlement is completed.
Employees who abandon their role without notice will forfeit any outstanding dues and will receive no relieving letter.
"""
    },
    {
        "id": "doc_010",
        "topic": "Employee Benefits and Perks",
        "text": """
Employee Benefits and Perks — Company HR Handbook

Health Insurance:
All permanent employees and their immediate family (spouse + 2 children) are covered under group health insurance of Rs 3 lakhs per annum.
Cashless hospitalisation is available at all network hospitals. Claims outside the network require pre-approval from HR.
Premium for the base cover is fully paid by the company. Employees may opt for a top-up cover at their own expense.

Other Reimbursements:
Gym or fitness membership reimbursement: up to Rs 2,000 per month, with receipt submitted via the HR portal.
Internet reimbursement for WFH-eligible employees: Rs 1,000 per month, credited with salary.
Mobile phone reimbursement (for eligible roles only): up to Rs 800 per month.

Learning and Development:
Annual learning budget of Rs 15,000 per employee for courses, certifications, and conferences.
Employees must apply for learning budget approval via the HR portal before making any purchase.
Reimbursement is processed within 30 days of submitting the receipt and completion certificate.
Sponsorship for higher education (MBA, MS) is available for high-performers — speak to HR for details.

Referral Bonus:
Employees who refer a candidate who is successfully hired and completes 6 months receive Rs 15,000 as a referral bonus.
"""
    },
]

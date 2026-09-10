"""
HR_docs.py
==========
Synthetic HR policy knowledge base for RAG (Retrieval-Augmented Generation)
pipelines. Contains realistic, generically-written corporate HR policy
documents covering the full lifecycle of an employee (hiring -> exit).

This is NOT copied from any real company's handbook — it's composed to
mirror the structure, tone, and level of detail typical of mid-to-large
tech/services companies, so it behaves like real-world data for chunking,
embedding, and retrieval testing.

Usage:
    from HR_docs import HR_POLICIES, get_policy_by_id, get_policies_by_category, CATEGORIES

    for doc in HR_POLICIES:
        # doc["content"] -> chunk this for your vector store
        ...
"""

from typing import List, Dict, Optional
import textwrap

# ---------------------------------------------------------------------------
# Policy documents
# ---------------------------------------------------------------------------

HR_POLICIES: List[Dict] = [

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-001",
        "category": "Leave & Time Off",
        "title": "Leave Policy",
        "version": "3.2",
        "effective_date": "2025-04-01",
        "owner": "Human Resources",
        "content": textwrap.dedent("""
            1. Purpose
            This policy defines the types of leave available to employees, eligibility
            criteria, accrual rules, and the process for applying for and approving leave.
            It applies to all full-time, permanent employees across all locations unless
            a local statutory requirement provides otherwise.

            2. Leave Year
            The leave year runs from April 1 to March 31. Leave balances are calculated
            and credited at the start of each leave year and do not carry over from a
            previous employer.

            3. Types of Leave

            3.1 Casual Leave (CL)
            Employees are entitled to 12 days of casual leave per year, credited at 1 day
            per completed month of service. Casual leave is intended for short, unplanned
            absences and cannot be availed for more than 3 consecutive days without prior
            manager approval. Casual leave cannot be carried forward or encashed.

            3.2 Sick Leave (SL)
            Employees are entitled to 10 days of sick leave per year, credited at 1 day
            per completed month of service. For sick leave exceeding 2 consecutive days,
            a medical certificate from a registered practitioner must be submitted within
            3 working days of returning to work. Unused sick leave up to 5 days may be
            carried forward to the next leave year.

            3.3 Earned / Privilege Leave (EL/PL)
            Employees accrue 1.5 days of earned leave per completed month of service
            (18 days annually). Earned leave must be applied for at least 5 working days
            in advance, except in emergencies. A maximum of 30 days of earned leave may be
            carried forward year over year; unused earned leave beyond this cap is
            automatically encashed at the end of the leave year, subject to applicable tax.

            3.4 Maternity Leave
            Eligible employees are entitled to 26 weeks of paid maternity leave for the
            first two children, and 12 weeks for the third child onward, in accordance
            with applicable maternity benefit legislation. Up to 8 weeks may be availed
            before the expected delivery date. A written request along with a medical
            certificate confirming the expected date of delivery must be submitted at
            least 8 weeks in advance where possible.

            3.5 Paternity Leave
            Male employees (including in same-sex partnerships/adoptions where legally
            recognized) are entitled to 15 calendar days of paid paternity leave, to be
            availed within 3 months of the child's birth or adoption.

            3.6 Adoption Leave
            An employee adopting a child below the age of 3 months is entitled to 12
            weeks of paid leave from the date the child is placed in the employee's care.

            3.7 Bereavement Leave
            Employees are entitled to 5 days of paid bereavement leave in the event of
            the death of an immediate family member (spouse, child, parent, sibling) and
            3 days for extended family members, at the discretion of the reporting manager.

            3.8 Leave Without Pay (LWP)
            Where an employee has exhausted all applicable paid leave, LWP may be granted
            at the discretion of the reporting manager and HR, up to a maximum of 30 days
            in a leave year. Any LWP beyond this requires VP-level and HR Business Partner
            approval and may affect the annual performance and increment cycle eligibility.

            4. Public Holidays
            The company observes a minimum of 12 public holidays per calendar year, as
            published on the HR portal by December of the preceding year, varying by
            work location to comply with local/regional observances.

            5. Application Process
            All leave (except emergency sick leave) must be applied through the HRMS
            portal and approved by the direct reporting manager prior to the leave being
            taken. Emergency leave must be communicated to the manager and marked in the
            system within 24 hours. Unapproved absences exceeding 3 consecutive working
            days without communication will be treated as unauthorized absence and may
            invoke the Disciplinary Action Policy (HR-014), including possible treatment
            as voluntary resignation ("job abandonment") after 10 consecutive uncommunicated
            working days.

            6. Leave During Notice Period
            Earned leave may be availed during the notice period subject to manager
            approval and business requirements; it cannot be used to reduce the effective
            last working day unless explicitly approved by HR.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-002",
        "category": "Workplace Conduct",
        "title": "Code of Conduct and Business Ethics",
        "version": "4.0",
        "effective_date": "2025-01-01",
        "owner": "Human Resources / Legal & Compliance",
        "content": textwrap.dedent("""
            1. Purpose
            This Code of Conduct sets out the standards of professional and ethical
            behavior expected of every employee, contractor, and officer of the company,
            regardless of role, level, or location.

            2. Core Principles
            - Integrity: Act honestly in all business dealings; never falsify records,
              expense claims, timesheets, or performance data.
            - Respect: Treat colleagues, clients, vendors, and the public with dignity.
              Harassment, bullying, discrimination, or retaliation of any kind is
              prohibited (see Anti-Harassment & Equal Opportunity Policy, HR-006).
            - Compliance: Comply with all applicable laws, regulations, and company
              policies in every jurisdiction of operation.
            - Confidentiality: Protect company, client, and employee confidential
              information both during and after employment (see HR-011).
            - Conflict of Interest: Disclose any personal, financial, or familial
              relationship that could reasonably be seen to influence business decisions,
              including relationships with vendors, competitors, or direct reports.

            3. Gifts and Entertainment
            Employees may not solicit or accept gifts, hospitality, or favors from
            vendors, clients, or partners that could reasonably be perceived to influence
            a business decision. Gifts with a value below the locally published threshold
            (typically equivalent to USD 75) that are token in nature may be accepted and
            must be declared to the manager if received more than twice from the same party
            in a calendar year.

            4. Anti-Bribery and Anti-Corruption
            The company has zero tolerance for bribery or corruption in any form,
            including facilitation payments. Employees must not offer, promise, give,
            request, or accept any bribe, kickback, or improper advantage to or from any
            person, whether in the public or private sector.

            5. Use of Company Assets
            Company assets (equipment, systems, intellectual property, brand, and funds)
            must be used for legitimate business purposes. Incidental personal use of
            email or internet is permitted provided it does not interfere with work,
            violate other policies, or incur material cost to the company.

            6. Insider Information
            Employees with access to material non-public information about the company,
            its clients, or its partners must not trade on such information or disclose
            it to others (including family members) who might trade on it.

            7. Reporting Violations
            Employees are required to report suspected violations of this Code through
            their manager, HR Business Partner, or the confidential Whistleblower Hotline
            (see HR-016). Reports made in good faith are protected from retaliation, even
            if the underlying concern is not ultimately substantiated.

            8. Consequences of Violation
            Violations of this Code may result in disciplinary action up to and including
            termination of employment, and may be reported to law enforcement or
            regulatory authorities where required by law.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-003",
        "category": "Work Arrangements",
        "title": "Remote Work and Hybrid Work Policy",
        "version": "2.1",
        "effective_date": "2025-06-01",
        "owner": "Human Resources",
        "content": textwrap.dedent("""
            1. Purpose
            This policy governs eligibility, expectations, and logistics for employees
            working remotely or in a hybrid arrangement (part-office, part-remote).

            2. Eligibility
            Roles are classified as Office-Based, Hybrid, or Fully Remote by the business
            unit head in consultation with HR, based on the nature of the work, client
            requirements, and team collaboration needs. Eligibility is reviewed annually
            or upon role change.

            3. Hybrid Work Expectations
            Hybrid employees are expected to be present in the office a minimum of 3 days
            per week, including all-hands days and any days designated as "team
            collaboration days" by the reporting manager. Attendance is tracked via badge
            swipe/HRMS and reviewed monthly by the manager.

            4. Fully Remote Work
            Fully remote arrangements require written approval from the department head
            and HR, and are typically granted for specialized roles, relocation for
            personal reasons, or documented medical/accessibility needs. Fully remote
            employees must attend in-person meetings (team offsites, client visits,
            onboarding) at company expense when required, with reasonable advance notice
            of at least 2 weeks except in urgent business situations.

            5. Work-from-Home Equipment and Reimbursement
            The company provides a laptop and, where applicable, a one-time home-office
            setup allowance (chair, monitor, keyboard) up to a locally defined cap.
            Employees are responsible for a stable internet connection and a private,
            professional working environment for calls.

            6. Core Collaboration Hours
            Regardless of work location, all employees must be reachable and available
            for meetings between 10:00 AM and 4:00 PM in their assigned time zone
            ("core hours"), unless an alternate schedule has been agreed with the manager
            in writing.

            7. Data Security While Remote
            Remote and hybrid employees must comply with the IT & Data Security Policy
            (HR-012) at all times, including use of company VPN for accessing internal
            systems, locking devices when unattended, and prohibition on public/unsecured
            Wi-Fi for handling confidential or client data.

            8. Working From Another Country
            Employees wishing to work remotely from a country other than their contracted
            work location for more than 10 consecutive calendar days must obtain prior
            approval from HR and Legal due to tax, immigration, and data-residency
            implications. Unapproved cross-border remote work may result in loss of
            company-provided insurance coverage while abroad.

            9. Performance Standards
            Remote and hybrid employees are held to the same performance, availability,
            and output standards as office-based employees. Managers should set clear,
            outcome-based expectations rather than monitoring hours online.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-004",
        "category": "Attendance & Timekeeping",
        "title": "Attendance, Punctuality and Timekeeping Policy",
        "version": "1.5",
        "effective_date": "2025-01-01",
        "owner": "Human Resources",
        "content": textwrap.dedent("""
            1. Standard Working Hours
            Standard working hours are 9 hours per day (including a 1-hour unpaid lunch
            break), 5 days a week, unless a different schedule is specified in the
            employment contract or a shift roster (for operations/support roles).

            2. Grace Period and Late Marks
            A grace period of 15 minutes is provided for login/badge-in each day. More
            than 3 late marks (beyond the grace period) in a calendar month will trigger
            an automated notification to the employee and manager. More than 6 late marks
            in a rolling 3-month period may result in a formal counseling conversation
            under the Performance Improvement process.

            3. Time Tracking
            All employees must record attendance via the HRMS/biometric system (office-
            based) or the time-tracking tool (remote/client-billed roles). Employees on
            client-billable projects must additionally log hours in the applicable
            project timesheet by end of day, and timesheets must be approved by the
            project lead weekly.

            4. Half-Day and Short Leave
            Departures of more than 2 hours before the standard end time, or arrivals
            more than 2 hours after the standard start time, without prior approval, are
            recorded as a half-day and deducted from the casual/earned leave balance.

            5. Compensatory Off
            Employees required to work on a company holiday or weekend due to business
            need are entitled to a compensatory day off, to be availed within 30 days of
            the worked day, subject to manager approval.

            6. Overtime
            Where local law mandates overtime pay for non-exempt employees, overtime is
            paid at 1.5x the standard hourly rate for hours worked beyond the standard
            workday, and must be pre-approved by the manager. Exempt/managerial employees
            are generally not eligible for overtime pay.

            7. Attendance Irregularities
            Patterns of unexplained absenteeism, chronic tardiness, or timesheet
            discrepancies will be addressed through the Performance Improvement Plan (PIP)
            process and, if unresolved, the Disciplinary Action Policy (HR-014).
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-005",
        "category": "Compensation & Benefits",
        "title": "Expense Reimbursement Policy",
        "version": "2.3",
        "effective_date": "2025-02-01",
        "owner": "Finance / Human Resources",
        "content": textwrap.dedent("""
            1. General Principle
            Employees will be reimbursed for reasonable, necessary, and pre-approved
            business expenses incurred in the course of company duties. Expenses must be
            submitted within 30 days of being incurred; claims submitted after 60 days
            may be rejected without exception approval from Finance.

            2. Categories of Reimbursable Expense
            - Travel: Economy class airfare, train fare, or standard taxi/ride-share for
              business travel. Business class air travel is permitted only for flights
              exceeding 6 hours, subject to Director-level approval.
            - Accommodation: Actual hotel cost up to the city-tier cap defined in the
              Travel Policy (HR-010).
            - Meals: Per-diem meal allowance while traveling on business, at rates
              published annually by Finance, varying by city/country tier.
            - Client Entertainment: Reasonable client meals/entertainment with prior
              manager approval and a business justification noting attendees and purpose.
            - Communication: Mobile/internet reimbursement for employees required to use
              personal devices for work, up to a monthly cap.
            - Training & Certification: Approved courses, certification exams, and
              related study materials directly relevant to the employee's role.

            3. Non-Reimbursable Expenses
            Personal entertainment, alcohol (except pre-approved client entertainment
            within policy limits), traffic/parking fines, personal grooming, mini-bar
            charges, spa services, and expenses for a traveling companion are not
            reimbursable.

            4. Submission Process
            All claims must be submitted through the expense management system with
            itemized receipts attached. Claims under the local "no-receipt" threshold
            (typically equivalent to USD 25) may be submitted with a self-certified
            declaration. Claims must be tagged to the correct cost center/project code.

            5. Approval Workflow
            Expenses are approved by the direct manager and, above defined thresholds,
            require additional approval from the department head or Finance. Approved
            claims are reimbursed with the next payroll cycle or via direct bank transfer
            within 10 business days, whichever is applicable locally.

            6. Corporate Card
            Employees issued a corporate card must use it exclusively for business
            expenses and reconcile all transactions in the expense system monthly.
            Personal use of the corporate card, even if later reimbursed, is a policy
            violation and may result in card revocation.

            7. Audit
            Finance reserves the right to audit any expense claim. Fraudulent claims will
            be treated as a serious violation of the Code of Conduct (HR-002) and may
            result in termination and recovery of amounts paid.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-006",
        "category": "Workplace Conduct",
        "title": "Anti-Harassment, Anti-Discrimination and Equal Opportunity Policy",
        "version": "3.0",
        "effective_date": "2025-01-01",
        "owner": "Human Resources / Internal Committee",
        "content": textwrap.dedent("""
            1. Policy Statement
            The company is committed to providing a work environment free from
            discrimination, harassment, and retaliation. This applies to all employees,
            contractors, interns, vendors, and visitors, and covers conduct in the office,
            at client sites, at company-sponsored events, and in virtual/remote
            interactions (chat, video calls, email).

            2. Protected Grounds
            Discrimination or harassment on the basis of race, color, religion, gender,
            gender identity or expression, sexual orientation, national origin, age,
            disability, marital status, pregnancy, veteran status, or any other
            characteristic protected by applicable law is strictly prohibited in hiring,
            promotion, compensation, training, and termination decisions.

            3. Sexual Harassment (Prevention of Sexual Harassment / POSH)
            Sexual harassment includes unwelcome sexual advances, requests for sexual
            favors, and other verbal, non-verbal, or physical conduct of a sexual nature
            that creates an intimidating, hostile, or offensive work environment, or is
            made an implicit/explicit condition of employment. This includes conduct over
            digital channels (messages, video calls, social media related to work).

            4. Internal Committee (IC)
            An Internal Committee, constituted per applicable local law and chaired by a
            senior woman employee with an external member from a recognized NGO/legal
            background, is responsible for receiving, investigating, and resolving
            complaints of sexual harassment. Contact details for the IC are published on
            the HR portal and displayed at all office locations.

            5. Complaint Process
            Complaints may be raised verbally or in writing to the IC, HR Business
            Partner, or via the confidential Whistleblower Hotline (HR-016), within 3
            months of the incident (extendable at the IC's discretion). The IC will
            complete its inquiry within 90 days, maintaining confidentiality of all
            parties to the extent possible under law.

            6. Protection Against Retaliation
            Retaliation against anyone who reports a concern in good faith, or who
            participates in an investigation, is strictly prohibited and will itself be
            treated as a serious disciplinary matter.

            7. Consequences
            Substantiated complaints may result in disciplinary action ranging from a
            written warning to immediate termination, depending on severity, and may be
            reported to law enforcement where the conduct constitutes a criminal offense.

            8. Training
            All employees must complete mandatory Prevention of Harassment training
            within 30 days of joining and annually thereafter. Completion is tracked and
            reported to the Board/Audit Committee as required by law.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-007",
        "category": "Performance",
        "title": "Performance Management and Appraisal Policy",
        "version": "2.0",
        "effective_date": "2025-04-01",
        "owner": "Human Resources",
        "content": textwrap.dedent("""
            1. Overview
            The company follows a continuous performance management model combining
            quarterly check-ins with a formal annual review cycle, replacing a purely
            once-a-year evaluation.

            2. Goal Setting
            At the start of each fiscal year (or upon joining/role change), employees and
            managers jointly set 3-5 SMART (Specific, Measurable, Achievable, Relevant,
            Time-bound) objectives aligned to team and company OKRs, recorded in the
            performance management system.

            3. Quarterly Check-Ins
            Managers and employees hold a documented check-in each quarter covering
            progress against goals, feedback, and any support needed. These are informal
            in rating but formal in documentation.

            4. Annual Review Cycle
            - Self-Assessment: Employees complete a self-assessment against their goals
              and competencies.
            - Manager Assessment: Managers rate performance on a 5-point scale
              (Significantly Exceeds / Exceeds / Meets / Partially Meets / Does Not Meet
              Expectations) with narrative justification.
            - Calibration: Ratings are calibrated across teams by function/level to
              ensure consistency and mitigate individual manager bias.
            - 360-Degree Input: For manager and senior roles, peer and, where applicable,
              direct-report feedback is incorporated.

            5. Rating and Rewards Linkage
            Annual ratings inform the merit increase, bonus payout, and promotion
            recommendations for the following cycle, per the Compensation Review Policy.
            Ratings of "Partially Meets" or below in two consecutive cycles trigger a
            mandatory Performance Improvement Plan (PIP).

            6. Performance Improvement Plan (PIP)
            A PIP is a structured, time-bound plan (typically 30-60-90 days) with clearly
            defined, measurable goals, regular check-ins, and documented support from the
            manager and HR. Failure to meet PIP goals may result in termination in
            accordance with local employment law.

            7. Promotions
            Promotions are considered during the annual cycle (and via an off-cycle
            fast-track process for exceptional performers) based on sustained performance,
            demonstrated readiness for the next level's competencies, and business need/
            role availability, subject to promotion committee review.

            8. Right to Appeal
            Employees who disagree with their rating may request a review by their Skip
            Level manager and HR Business Partner within 10 working days of the rating
            being communicated.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-008",
        "category": "Talent Acquisition",
        "title": "Recruitment, Onboarding and Referral Policy",
        "version": "1.8",
        "effective_date": "2025-01-01",
        "owner": "Talent Acquisition / Human Resources",
        "content": textwrap.dedent("""
            1. Recruitment Principles
            Hiring decisions are based solely on qualifications, skills, experience, and
            demonstrated potential relative to the role requirements, in compliance with
            the Equal Opportunity Policy (HR-006). All open roles are posted internally
            for a minimum of 5 working days before external advertisement, except for
            confidential leadership searches.

            2. Interview Process
            Standard interview processes include a recruiter screen, 2-4 technical/
            functional rounds, and a final hiring-manager/leadership round. Structured
            scorecards with pre-defined evaluation criteria must be used and retained for
            audit purposes for 12 months.

            3. Background Verification
            Offers are contingent on successful completion of background verification,
            covering employment history, education credentials, and, for applicable
            roles, criminal record and credit checks (where legally permitted). A
            confirmed instance of misrepresentation is grounds for offer withdrawal or,
            if already onboarded, immediate termination.

            4. Employee Referral Program
            Current employees may refer candidates for open positions via the internal
            referral portal. A referral bonus (amount varies by role level/difficulty,
            published on the HR portal) is paid after the referred candidate completes 90
            days of active employment. Employees may not refer immediate family members
            for roles within their own reporting line.

            5. Onboarding
            New hires undergo a structured onboarding program including: Day 1 orientation
            (policies, systems, IT setup), a 30-60-90 day plan agreed with the manager, a
            designated onboarding buddy, and mandatory compliance training (Code of
            Conduct, POSH, Data Security) to be completed within the first 2 weeks.

            6. Probation Period
            New employees serve a probation period of 3 to 6 months (as specified in the
            offer letter), during which either party may terminate employment with 7 days'
            notice (or as required by local law). Confirmation is subject to a satisfactory
            probation-end review with the manager.

            7. Internal Mobility
            Employees who have completed 12 months in their current role are eligible to
            apply for internal job postings, subject to current manager notification and
            a minimum "meets expectations" performance rating in the last review cycle.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-009",
        "category": "Separation",
        "title": "Resignation, Notice Period and Exit Policy",
        "version": "2.2",
        "effective_date": "2025-01-01",
        "owner": "Human Resources",
        "content": textwrap.dedent("""
            1. Resignation
            Employees wishing to resign must submit a written resignation through the
            HRMS portal, addressed to their reporting manager and copied to HR. The
            resignation date is deemed to be the date of submission unless otherwise
            agreed in writing.

            2. Notice Period
            Standard notice periods are: 30 days for individual contributors, 60 days for
            managers and above, and 90 days for Director level and above, unless the
            employment contract specifies otherwise. The company may, at its discretion,
            waive part or all of the notice period, or require the employee to serve "Paid
            Leave" (Garden Leave) for client/data-sensitive roles.

            3. Buyout of Notice Period
            Where mutually agreed, an employee may buy out the unserved portion of the
            notice period at the applicable gross salary rate, subject to department head
            and HR approval, to enable an earlier last working day.

            4. Knowledge Transfer
            Departing employees are required to complete a documented knowledge transfer
            (KT) plan with their manager and successor/team, covering ongoing work,
            credentials handover (with IT), and client/stakeholder relationship transition.

            5. Exit Interview
            HR conducts a confidential exit interview (in person or via survey) prior to
            the last working day to capture feedback on the employee experience. Feedback
            is aggregated and shared with leadership without individual attribution unless
            the employee consents.

            6. Clearance and Full and Final Settlement
            Departing employees must complete IT, Finance, Admin, and HR clearance
            (return of assets: laptop, ID card, access cards) before the last working day.
            Full and Final (F&F) settlement — including pending salary, leave encashment,
            and any deductions (loans, asset non-return) — is processed within 30-45 days
            of the last working day, per local payroll cycle requirements.

            7. Absconding / Job Abandonment
            An employee who is absent without approved leave or communication for 10
            consecutive working days will be treated as having voluntarily abandoned
            employment, and the separation will be processed as a resignation without
            notice, subject to due process and a final attempt to contact the employee.

            8. Rehire Eligibility
            Former employees who separated in good standing (completed notice period,
              clean clearance) are generally eligible for rehire after a minimum of 6
              months, subject to standard recruitment process. Employees terminated for
              cause or who abandoned their role are typically marked "not eligible for
              rehire."

            9. Post-Employment Obligations
            Confidentiality, non-solicitation, and (where enforceable under local law)
            non-compete obligations in the employment contract survive termination of
            employment for the period specified therein.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-010",
        "category": "Compensation & Benefits",
        "title": "Business Travel Policy",
        "version": "1.6",
        "effective_date": "2025-01-01",
        "owner": "Finance / Human Resources",
        "content": textwrap.dedent("""
            1. Trip Approval
            All domestic and international business travel must be pre-approved by the
            reporting manager via the travel booking system at least 5 working days (14
            days for international) before departure, except genuine urgent client needs.

            2. Booking Channel
            Travel must be booked through the company's designated travel desk/booking
            tool to ensure duty-of-care visibility and negotiated corporate rates.
            Self-booked travel is reimbursed only up to the equivalent designated-channel
            fare, with prior exception approval.

            3. Class of Travel
            - Air (domestic): Economy class for all levels.
            - Air (international, <6 hrs): Economy/Premium Economy.
            - Air (international, >=6 hrs): Business class for Director level and above;
              Premium Economy for others, subject to approval.
            - Rail: AC 2-tier / equivalent standard class or below.

            4. Accommodation
            Hotel stays are booked within city-tier caps published annually by Finance
            (Tier 1 metro / Tier 2 / Tier 3 cities have different caps). Employees may
            upgrade at personal cost; the company will not reimburse the differential.

            5. Ground Transportation
            Airport transfers and local commute during business travel should use
            company-empaneled taxi services where available; ride-share is acceptable
            where no empaneled option exists. Rental cars require Director-level approval.

            6. Travel Insurance and Duty of Care
            All company-booked business travel is automatically covered under the
            corporate travel insurance policy. Employees traveling to locations under a
            government-issued travel advisory must obtain additional Security/HR sign-off
            before booking.

            7. Combining Business and Personal Travel
            Employees may extend a business trip for personal travel with manager
            approval; the company bears only the cost that would have been incurred for
            the business-only itinerary, and personal-day expenses are the employee's
            responsibility.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-011",
        "category": "Legal & Compliance",
        "title": "Confidentiality and Intellectual Property Policy",
        "version": "2.0",
        "effective_date": "2025-01-01",
        "owner": "Legal & Compliance",
        "content": textwrap.dedent("""
            1. Confidential Information
            Confidential Information includes, without limitation: client data, source
            code, product roadmaps, pricing, financial results prior to public disclosure,
            employee personal data, business strategy, and any information marked or
            reasonably understood to be confidential. Employees must not disclose
            Confidential Information to any third party, or use it for any purpose other
            than performing their job duties, during or after employment.

            2. Intellectual Property Assignment
            All work product created by an employee within the scope of their employment
            — including code, designs, inventions, documentation, and creative work — is
            the sole property of the company ("work made for hire"), regardless of whether
            created during standard working hours or using personal equipment, unless
              expressly agreed otherwise in writing.

            3. Third-Party Confidential Information
            Employees must not bring to the company, or use in their work, any
            confidential information or trade secrets belonging to a previous employer.

            4. Data Handling
            Client and company confidential data must be handled per the classification
            levels (Public / Internal / Confidential / Restricted) defined in the Data
            Classification Standard, and stored only in approved, encrypted systems. Data
            must never be transferred via personal email, personal cloud storage, or
            unapproved messaging apps.

            5. Publications and Public Speaking
            Employees wishing to publish articles, give talks, or post on social media
            about company work, products, or research must obtain prior clearance from
              their manager and, where client-related, from Legal/Communications.

            6. Return of Materials
            Upon termination of employment for any reason, the employee must return all
            company property and permanently delete any company/client data retained on
            personal devices or accounts, and certify such deletion if requested.

            7. Survival
            The confidentiality obligations in this policy survive termination of
            employment indefinitely for trade secrets, and for a period of 3-5 years (per
            the employment contract) for other confidential information.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-012",
        "category": "IT & Security",
        "title": "IT Usage and Data Security Policy",
        "version": "3.1",
        "effective_date": "2025-03-01",
        "owner": "Information Security / IT",
        "content": textwrap.dedent("""
            1. Acceptable Use
            Company IT systems, email, and devices are provided for business purposes.
            Incidental personal use is permitted provided it is lawful, does not consume
            significant resources, and does not violate this or any other company policy
            (e.g., accessing illegal, discriminatory, or adult content is prohibited on
            any company system).

            2. Access Control
            Access to systems and data is granted on a least-privilege, role-based basis
            and reviewed quarterly. Employees must not share login credentials, and must
            use multi-factor authentication (MFA) on all systems where it is available.

            3. Device Security
            Company-issued laptops must have disk encryption, endpoint protection, and
            automatic screen lock (maximum 5 minutes of inactivity) enabled at all times.
            Loss or theft of a company device must be reported to IT Security within 2
              hours of discovery.

            4. Password Policy
            Passwords must be a minimum of 12 characters, include a mix of character
            types, and must not be reused across systems. Passwords must be changed
            immediately if compromise is suspected, and rotated per system-specific policy
            (typically every 90 days for privileged accounts).

            5. Software and BYOD
            Only IT-approved software may be installed on company devices. Personal
            devices used to access company email or systems (BYOD) must be enrolled in
            the Mobile Device Management (MDM) system and are subject to remote wipe of
            company data upon termination or loss.

            6. Incident Reporting
            Suspected phishing emails, malware, unauthorized access, or data breaches must
            be reported immediately to the IT Security team via the dedicated hotline/
            email. Employees will not face disciplinary action for promptly reporting a
            genuine mistake (e.g., clicking a phishing link), but delayed or concealed
              reporting will be treated as a policy violation.

            7. Monitoring
            The company reserves the right to monitor use of its IT systems (email,
            internet, endpoint activity) for security, compliance, and legitimate business
            purposes, to the extent permitted by applicable law, with notice provided to
            employees at the time of onboarding.

            8. AI Tool Usage
            Use of external generative AI tools for work must comply with the company's AI
            Acceptable Use guidelines: no Confidential or Restricted data (including client
            data, source code, or personal data) may be entered into any AI tool that has
            not been explicitly approved and configured by IT Security for enterprise use.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-013",
        "category": "Compensation & Benefits",
        "title": "Health Insurance and Employee Benefits Policy",
        "version": "2.4",
        "effective_date": "2025-04-01",
        "owner": "Human Resources / Total Rewards",
        "content": textwrap.dedent("""
            1. Group Medical Insurance
            All full-time employees are covered under the company Group Mediclaim policy
            from Day 1 of employment, with coverage for the employee, spouse, and up to 2
            dependent children (parents may be covered via an optional top-up at
            employee cost). Sum insured and network hospital list are published on the
            benefits portal and reviewed annually at renewal.

            2. Life and Accident Insurance
            Employees are covered under a Group Term Life Insurance policy (typically 3-5x
            annual base salary) and Group Personal Accident insurance, at no cost to the
            employee, effective from date of joining.

            3. Wellness Benefits
            - Annual health check-up voucher for employees above a defined age/tenure.
            - Employee Assistance Program (EAP): confidential counseling (mental health,
              financial, legal) available 24/7 at no cost, for employees and immediate
              family.
            - Gym/fitness reimbursement up to an annual cap, where offered locally.

            4. Retirement Benefits
            The company contributes to statutory retirement schemes as required by local
            law (e.g., provident fund, superannuation, 401(k) matching where applicable),
            at the rates published in the region-specific benefits addendum.

            5. Flexible Benefits / Cafeteria Plan
            Eligible employees may allocate a portion of CTC across benefit options
            (meal cards, fuel/transport allowance, telephone reimbursement) within
            statutory limits, elected annually during the benefits enrollment window.

            6. Parental and Family Benefits
            In addition to statutory maternity/paternity leave (HR-001), the company
            offers a childcare reimbursement allowance and, at select locations, on-site
            or partnered daycare facilities.

            7. Life Event Changes
            Employees must update dependent/beneficiary information within 30 days of a
            qualifying life event (marriage, birth/adoption, divorce) to ensure continuity
            of coverage; changes outside the annual enrollment window are only permitted
              for such qualifying events.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-014",
        "category": "Workplace Conduct",
        "title": "Disciplinary Action and Grievance Redressal Policy",
        "version": "1.9",
        "effective_date": "2025-01-01",
        "owner": "Human Resources",
        "content": textwrap.dedent("""
            1. Purpose
            This policy defines the process for addressing employee misconduct and for
            employees to raise workplace grievances, ensuring fairness and consistency.

            2. Categories of Misconduct
            - Minor: Repeated tardiness, missed deadlines without communication, minor
              policy non-compliance.
            - Major: Insubordination, harassment (see HR-006), data misuse, conflict of
              interest, falsification of records, breach of confidentiality.
            - Gross Misconduct: Theft, fraud, violence, sexual harassment, being under the
              influence of drugs/alcohol at work, serious breach of law.

            3. Disciplinary Process
            - Step 1 — Verbal Counseling: Informal discussion with the manager, documented
              in the HRMS.
            - Step 2 — Written Warning: Formal written warning outlining the issue,
              expected improvement, and timeline, copied to HR and the employee's file.
            - Step 3 — Final Written Warning / Suspension: For repeated or more serious
              issues, may include unpaid suspension pending investigation.
            - Step 4 — Termination: For gross misconduct or failure to improve after prior
              steps, subject to HR and Legal review.
            Gross misconduct may result in immediate termination without progressing
            through Steps 1-3, following a fair investigation and the employee's
            opportunity to respond ("show cause").

            4. Investigation Process
            Allegations of major or gross misconduct are investigated by HR (and, where
            relevant, the Internal Committee or Legal) with confidentiality maintained to
            the extent possible. The employee is informed of the allegation and given a
            reasonable opportunity to present their side before any action is finalized.

            5. Grievance Redressal
            Employees with a concern about their manager, working conditions, pay, or any
            other workplace matter may raise it via: (a) direct discussion with the
            manager, (b) escalation to the HR Business Partner, or (c) the anonymous
            Grievance/Whistleblower Hotline (HR-016). HR will acknowledge a grievance
            within 3 working days and aim to resolve or provide a status update within 15
              working days.

            6. Appeal
            An employee subject to disciplinary action (other than immediate termination
            for gross misconduct) may appeal in writing to the next-level manager and HR
            within 5 working days of the decision being communicated.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-015",
        "category": "Workplace Conduct",
        "title": "Dress Code and Workplace Etiquette Policy",
        "version": "1.2",
        "effective_date": "2025-01-01",
        "owner": "Human Resources",
        "content": textwrap.dedent("""
            1. General Guidance
            The company follows a "business casual" dress code on regular working days,
            and "smart casual" on designated casual/Friday days where locally adopted.
            Employees meeting clients or attending formal business events should dress in
            business formal attire unless the client explicitly indicates otherwise.

            2. Video Call Etiquette
            Employees are expected to be dressed appropriately and maintain a professional
            background (virtual background permitted) for internal and external video
            calls, and to mute microphones when not speaking in group calls.

            3. Workplace Etiquette
            - Maintain a clean and organized workspace; shared spaces (pantry, meeting
              rooms) should be left tidy after use.
            - Meeting rooms should be booked in advance and released promptly if not
              needed.
            - Strong fragrances, loud personal calls in open seating areas, and
              non-work-related noise that disrupts colleagues should be avoided.

            4. Religious and Cultural Accommodation
            The dress code accommodates religious and cultural attire (e.g., turbans,
            hijabs, traditional garments) without restriction, consistent with the
            Equal Opportunity Policy (HR-006).

            5. Exceptions
            Roles with specific safety or client-mandated dress requirements (e.g.,
            factory floor, data center, healthcare client site) follow the additional
            requirements specified for that role/location, which supersede this general
            policy where stricter.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-016",
        "category": "Legal & Compliance",
        "title": "Whistleblower and Anti-Retaliation Policy",
        "version": "1.7",
        "effective_date": "2025-01-01",
        "owner": "Legal & Compliance / Audit Committee",
        "content": textwrap.dedent("""
            1. Purpose
            This policy provides a safe, confidential channel for employees, vendors, and
            other stakeholders to report suspected violations of law, the Code of Conduct
            (HR-002), financial irregularities, or other serious wrongdoing, without fear
            of retaliation.

            2. Reportable Concerns
            Concerns in scope include (but are not limited to): financial fraud or
            accounting irregularities, bribery/corruption, harassment or discrimination,
            data privacy breaches, health and safety violations, and abuse of authority.

            3. Reporting Channels
            Reports may be made through: (a) direct manager, (b) HR Business Partner,
            (c) Legal & Compliance, or (d) the independently-operated Whistleblower
            Hotline (phone and web portal, available 24/7, with an option to report
            anonymously where permitted by local law).

            4. Confidentiality
            The identity of the reporter is kept confidential to the maximum extent
            possible and permitted by law, and shared only on a strict need-to-know basis
            during investigation.

            5. Investigation
            All reports are triaged and, where warranted, investigated by an independent
            function (Internal Audit, Legal, or an external investigator for
            senior-leadership-related concerns), with findings reported to the Audit
              Committee on a periodic basis.

            6. Non-Retaliation
            Retaliation against anyone who raises a concern in good faith — including
            demotion, unfavorable rating, exclusion, or termination — is strictly
            prohibited and is itself grounds for disciplinary action, up to and including
            termination of the retaliating individual, regardless of seniority.

            7. False Reports
            Reports made in good faith are protected even if not ultimately substantiated.
            However, knowingly filing a false report with malicious intent is a violation
            of the Code of Conduct and may result in disciplinary action.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-017",
        "category": "Workplace Conduct",
        "title": "Social Media and External Communications Policy",
        "version": "1.3",
        "effective_date": "2025-01-01",
        "owner": "Human Resources / Corporate Communications",
        "content": textwrap.dedent("""
            1. Personal Social Media Use
            Employees are free to engage on personal social media accounts but must not
            disclose Confidential Information (HR-011), speak on behalf of the company
            without authorization, or post content that is discriminatory, harassing, or
            damaging to the company's reputation or that of clients/colleagues.

            2. Disclosure of Affiliation
            Employees who identify their employer on social media and discuss
            industry/work-related topics should include a disclaimer that views expressed
            are their own and not the company's, where relevant (e.g., LinkedIn posts,
            public forums).

            3. Official Company Channels
            Only designated spokespeople (Corporate Communications, authorized executives)
            may speak to media, publish official company statements, or manage official
            company social media accounts.

            4. Client and Vendor Mentions
            Employees must not name or identify clients, vendors, or partners on personal
            social media, or share details of ongoing projects, without explicit written
            consent, even if the information seems publicly known.

            5. Recruitment-Related Posting
            Employees participating in the Employee Referral Program (HR-008) may share
            approved job postings on personal social media using company-provided
            templates/links.

            6. Consequences
            Violations — including posts that constitute harassment of colleagues, leaks
            of confidential information, or reputational harm to the company — will be
            handled under the Disciplinary Action Policy (HR-014), independent of whether
            the post was made using personal or company accounts/devices.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-018",
        "category": "Health & Safety",
        "title": "Workplace Health, Safety and Substance-Free Workplace Policy",
        "version": "1.4",
        "effective_date": "2025-01-01",
        "owner": "Admin / Human Resources",
        "content": textwrap.dedent("""
            1. General Safety
            The company maintains all office premises in compliance with applicable
            occupational health and safety regulations, including fire safety
            certification, emergency evacuation plans (displayed on each floor), and
            first-aid facilities staffed by trained personnel during working hours.

            2. Incident Reporting
            Any workplace injury, near-miss, or unsafe condition must be reported
            immediately to the Admin/Facilities team and logged in the safety incident
            register, regardless of severity.

            3. Emergency Procedures
            Fire drills are conducted at least twice a year at each office location.
            Employees must familiarize themselves with the nearest emergency exit and
            assembly point upon joining, as covered in Day 1 onboarding.

            4. Substance-Free Workplace
            Employees must not report to work, or be present at work, under the influence
            of alcohol or illegal drugs. Consumption of alcohol on company premises is
            prohibited except at pre-approved, company-sanctioned events. Employees taking
            prescribed medication that may affect their ability to safely perform their
            job should inform their manager or HR confidentially.

            5. Violence-Free Workplace
            The company has zero tolerance for threats or acts of violence, or possession
            of weapons, on company premises or at company-sponsored events. Any such
            incident should be reported immediately to Security/HR and, where there is
            imminent danger, to local law enforcement.

            6. Ergonomics
            Employees experiencing discomfort related to their workstation setup (office
            or home) may request an ergonomic assessment through Admin/HR, who will
            recommend adjustments or equipment (e.g., chair, monitor riser) as needed.

            7. Smoking Policy
            Smoking (including e-cigarettes) is permitted only in designated outdoor
            smoking areas, where provided, and is prohibited within 10 meters of any
            building entrance.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-019",
        "category": "Diversity & Inclusion",
        "title": "Diversity, Equity and Inclusion (DEI) Policy",
        "version": "1.5",
        "effective_date": "2025-01-01",
        "owner": "Human Resources / DEI Council",
        "content": textwrap.dedent("""
            1. Commitment
            The company is committed to building a diverse workforce and an inclusive
            culture where employees of all backgrounds can do their best work and advance
            based on merit, free from bias.

            2. Hiring and Promotion
            Structured interview panels are encouraged to reflect diverse perspectives
            where feasible, and job descriptions are reviewed for inclusive language.
            Hiring managers receive unconscious-bias training before participating in
            interview panels.

            3. Pay Equity
            The company conducts an annual pay equity audit across gender and, where
            legally permitted to analyze, other demographic dimensions, for
            same/comparable roles, and remediates identified unexplained gaps.

            4. Employee Resource Groups (ERGs)
            The company supports voluntary Employee Resource Groups (e.g., for women in
            tech, LGBTQ+ employees and allies, employees with disabilities, parents/
            caregivers) with an annual budget and executive sponsorship for each group.

            5. Accessibility
            The company provides reasonable accommodations for employees and candidates
            with disabilities (e.g., accessible facilities, assistive technology,
            flexible scheduling) upon request to HR, evaluated on a case-by-case,
            interactive basis.

            6. Inclusive Benefits
            Benefits (including parental leave and insurance dependent coverage) are
            extended equally to employees regardless of marital status, gender identity,
            or sexual orientation, consistent with applicable local law.

            7. Measurement and Accountability
            Diversity metrics (representation by level, hiring, attrition) are reviewed
            quarterly by the DEI Council and reported to executive leadership, with
            targets published in the annual DEI report.
        """).strip(),
    },

    # -----------------------------------------------------------------
    {
        "doc_id": "HR-020",
        "category": "Learning & Development",
        "title": "Learning, Development and Tuition Reimbursement Policy",
        "version": "1.1",
        "effective_date": "2025-01-01",
        "owner": "Human Resources / Learning & Development",
        "content": textwrap.dedent("""
            1. Learning Philosophy
            The company follows a 70-20-10 development model (70% on-the-job experience,
            20% mentoring/peer learning, 10% formal training) and expects every employee
            to have a development plan agreed with their manager.

            2. Internal Learning Platform
            All employees have access to the internal Learning Management System (LMS)
            with self-paced courses, and a minimum of 24 hours of learning time per year
            is protected/encouraged as part of working hours.

            3. External Certifications
            Employees may request sponsorship for job-relevant external certifications
            (cloud, project management, domain-specific) up to an annual cap per level,
            subject to manager approval. The company covers exam fees and, upon passing,
            may cover a portion of prep-course costs.

            4. Tuition Reimbursement
            Employees with at least 1 year of tenure may apply for tuition reimbursement
            for job-relevant, accredited degree/diploma programs, up to an annual cap, with
            a minimum grade requirement (e.g., B or above) for reimbursement release, and
            a service-commitment (bond) period of 12-24 months post-completion, after
              which any unserved portion must be repaid on a pro-rata basis if the
              employee resigns.

            5. Mentorship Program
            A structured mentorship program pairs employees with senior mentors across
            functions; participation is voluntary and coordinated through the L&D team
            twice a year.

            6. Conference Attendance
            Attendance at external conferences relevant to the employee's role is
            supported subject to budget availability and manager approval, prioritized
            for employees presenting/speaking or in specialized/scarce skill areas.
        """).strip(),
    },
]

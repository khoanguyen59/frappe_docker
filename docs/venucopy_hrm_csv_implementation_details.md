# Venucopy HRM CSV - Implementation Details

## 1) Source Requirement and Target

- Requirement source: `/home/khoanguyen/Downloads/HRM_Feature_Detail.xlsx - HRM Features.csv`
- Target site: `frontend`
- Platform: ERPNext + HRMS (v16 stack in Docker)
- Approach: no custom app runtime logic; only configuration/data via standard DocTypes, Custom Field, Workflow, and seed records.

## 2) Requirement-to-Implementation Mapping

## H06 - Tag phan nhom nhan su

Implemented with custom field:

- `Employee.custom_employee_group`
- Type: `Select`
- Values: `Van phong`, `Thuyen vien`, `CTV`, `Nuoc ngoai`

Seed assignment:

- `HR-EMP-00001` -> `Van phong`
- `HR-EMP-00002` -> `Thuyen vien`
- `HR-EMP-00003` -> `Van phong`

## H18 - Don nghi phep, tang ca, cong tac, docs approve

Implemented via three workflows and custom fields:

1. `Venucopy Leave Approval WF` on `Leave Application`
   - States: `Draft` -> `Pending Manager` -> `Pending HR` -> `Approved` / `Rejected`
   - Roles: `Employee`, `Leave Approver`, `HR Manager`
   - Custom columns used:
     - `custom_request_type`
     - `custom_handover_employee`
     - `custom_reason_detail`

2. `Venucopy Overtime Approval WF` on `Overtime Slip`
   - Same 3-step approval flow
   - Custom column used: `custom_ot_reason`

3. `Venucopy Travel Approval WF` on `Travel Request`
   - Same 3-step approval flow
   - Custom columns used:
     - `custom_trip_category`
     - `custom_expected_outcome`

Seeded demo records:

- Leave: `HR-LAP-2026-00003`
- Overtime: `HR-OT-SLIP-00001`
- Travel: `HR-TRQ-2026-00001`

## H19 - De xuat tuyen dung / ky luat / khen thuong / thay doi luong

Implemented with 3 separate business workflows:

1. `Venucopy Recruitment Proposal WF` on `Job Requisition`
2. `Venucopy Reward Discipline WF` on `Additional Salary`
3. `Venucopy Salary Change WF` on `Employee Promotion`

Custom columns:

- `Job Requisition.custom_request_category`
- `Additional Salary.custom_proposal_type`
- `Additional Salary.custom_reference_note`
- `Employee Promotion.custom_change_reason`

Seeded demo records:

- Job Requisition: `HR-HIREQ-00002`
- Additional Salary: `HR-ADS-26-05-00001`
- Employee Promotion: `HR-EMP-PRO-2026-00001`

## H22 - Checklist offboarding

Implemented using `Employee Separation` workflow:

- Workflow: `Venucopy Offboarding WF`
- States: `Draft` -> `Pending Manager Clearance` -> `Pending HR Clearance` -> `Completed`
- Roles: `HR User`, `Leave Approver`, `HR Manager`

Custom columns:

- `Employee Separation.custom_offboarding_status`
- `Employee Separation.custom_asset_return_note`

Seeded demo record:

- `HR-EMP-SEP-2026-00001`

## 3) Technical Objects Added

## Custom Field

- `Additional Salary-custom_proposal_type`
- `Additional Salary-custom_reference_note`
- `Employee-custom_employee_group`
- `Employee Promotion-custom_change_reason`
- `Employee Separation-custom_asset_return_note`
- `Employee Separation-custom_offboarding_status`
- `Job Requisition-custom_request_category`
- `Leave Application-custom_request_type`
- `Leave Application-custom_handover_employee`
- `Leave Application-custom_reason_detail`
- `Overtime Slip-custom_ot_reason`
- `Travel Request-custom_trip_category`
- `Travel Request-custom_expected_outcome`

## Workflow

- `Venucopy Leave Approval WF`
- `Venucopy Overtime Approval WF`
- `Venucopy Travel Approval WF`
- `Venucopy Recruitment Proposal WF`
- `Venucopy Reward Discipline WF`
- `Venucopy Salary Change WF`
- `Venucopy Offboarding WF`

## Workflow State and Action Masters

Added reusable masters needed by transitions/states:

- States include: `Pending Manager`, `Pending HR`, `Pending Manager Clearance`, `Pending HR Clearance`, `Completed` (and standard states reused)
- Actions include submit/approve/reject variants and offboarding actions (`Start Offboarding`, `Manager Cleared`, `Close Checklist`)

## Supporting Master Data

- `Purpose of Travel`: `Warehouse Audit`
- `Salary Component`: `Overtime VNC`
- `Overtime Type`: `Weekday OT 150`

## 4) Validation Snapshot

Verified present on site:

- 7 active `Venucopy*` workflows
- custom columns available on all configured doctypes
- seeded records visible and initialized in `Draft` workflow state for approval-path testing

## 5) How to Test the Flow

1. Login as a user with role `Employee` and open one seeded draft request.
2. Execute first transition (`Submit ...`) to `Pending Manager`.
3. Login as role `Leave Approver` (or mapped manager role) and approve/reject.
4. Login as `HR Manager` and complete final HR decision.
5. Confirm final workflow state and downstream status field changes.

## 6) Known Gaps vs Full CSV

Not implemented in this pass (requires broader module work/custom app UI):

- Internal feed/news channels (`H01-H04`)
- Full custom profile engine/template runtime (`H11` beyond field-level extension)
- Calendar conflict engine/Gantt planning (`H14-H16`)
- Payroll email automation/export to Misa (`H24-H26` future phase)
- Advanced RBAC matrix/scope preview engine (`H30-H37` platform-level)
- Popup notification platform requirement (`H00`/supplement)

This pass delivers a compatible HR workflow/data foundation that follows CSV business process intent while staying native to ERPNext/HRMS configuration.

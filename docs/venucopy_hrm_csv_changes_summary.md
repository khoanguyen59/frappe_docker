# Venucopy HRM CSV - Change Summary

## Scope

Seeded and configured data on site `frontend` to align with Vietnamese requirements in:

- `/home/khoanguyen/Downloads/HRM_Feature_Detail.xlsx - HRM Features.csv`

Focus was on workflow-heavy Must items (`H18`, `H19`, `H22`) and custom profile/workflow fields (`H06`, `H07-H11` partial support via custom columns).

## Applied Custom Columns

- `Employee.custom_employee_group` (Select): `Van phong`, `Thuyen vien`, `CTV`, `Nuoc ngoai`
- `Leave Application.custom_request_type` (Select)
- `Leave Application.custom_handover_employee` (Link Employee)
- `Leave Application.custom_reason_detail` (Small Text)
- `Travel Request.custom_trip_category` (Select)
- `Travel Request.custom_expected_outcome` (Small Text)
- `Overtime Slip.custom_ot_reason` (Small Text)
- `Job Requisition.custom_request_category` (Select)
- `Additional Salary.custom_proposal_type` (Select)
- `Additional Salary.custom_reference_note` (Data)
- `Employee Promotion.custom_change_reason` (Small Text)
- `Employee Separation.custom_offboarding_status` (Select)
- `Employee Separation.custom_asset_return_note` (Small Text)

## Configured Workflows

All workflows below are active (`is_active = 1`):

- `Venucopy Leave Approval WF` on `Leave Application`
- `Venucopy Overtime Approval WF` on `Overtime Slip`
- `Venucopy Travel Approval WF` on `Travel Request`
- `Venucopy Recruitment Proposal WF` on `Job Requisition`
- `Venucopy Reward Discipline WF` on `Additional Salary`
- `Venucopy Salary Change WF` on `Employee Promotion`
- `Venucopy Offboarding WF` on `Employee Separation`

Added workflow master data to support transitions:

- New `Workflow State`: `Draft`, `Pending Manager`, `Pending HR`, `Pending Manager Clearance`, `Pending HR Clearance`, `Completed` (and reused existing states like `Approved`, `Rejected`)
- New `Workflow Action Master`: submit/approve/reject and offboarding actions used in the workflows

## Seeded Demo Records

- Leave: `HR-LAP-2026-00003` (plus existing seeded records)
- Travel request: `HR-TRQ-2026-00001`
- Overtime: `HR-OT-SLIP-00001`
- Recruitment proposal: `HR-HIREQ-00002`
- Reward/discipline proposal: `HR-ADS-26-05-00001`
- Salary change proposal: `HR-EMP-PRO-2026-00001`
- Offboarding checklist: `HR-EMP-SEP-2026-00001`

Supporting masters seeded:

- `Purpose of Travel`: `Warehouse Audit`
- `Salary Component`: `Overtime VNC`
- `Overtime Type`: `Weekday OT 150`

## Notes

- All new transactional seed records are currently in `Draft` workflow state (ready for role-based transition testing).
- This implementation intentionally keeps ERPNext/HRMS standard doctypes and extends by custom fields/workflow only.
- CSV items in other domains (internal feed, advanced RBAC engine, dashboard builder, popup notification platform) were not custom-developed here.

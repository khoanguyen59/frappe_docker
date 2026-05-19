import frappe
from frappe.model.document import Document


class ShipmentTracking(Document):
    def validate(self):
        if not self.tracking_id:
            self.tracking_id = f"TRK-{frappe.generate_hash(length=8).upper()}"

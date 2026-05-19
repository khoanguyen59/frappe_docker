import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class LogisticsJob(Document):
    def validate(self):
        self._compute_totals()
        self._validate_parties()

    def on_submit(self):
        self._create_selling_document()
        self._create_buying_document()

    def _compute_totals(self):
        total_buy = 0.0
        total_sell = 0.0

        for row in self.services or []:
            qty = flt(row.qty or 0)
            buy_rate = flt(row.buy_rate or 0)
            sell_rate = flt(row.sell_rate or 0)

            row.buy_amount = qty * buy_rate
            row.sell_amount = qty * sell_rate
            row.margin_amount = row.sell_amount - row.buy_amount

            total_buy += row.buy_amount
            total_sell += row.sell_amount

        self.total_buy_amount = total_buy
        self.total_sell_amount = total_sell
        self.total_margin = total_sell - total_buy
        self.margin_percent = (self.total_margin / total_sell * 100.0) if total_sell else 0.0

    def _validate_parties(self):
        if not self.customer and not self.supplier:
            frappe.throw(_("Set at least a Customer or Supplier."))

    def _create_selling_document(self):
        if self.sales_order or not self.customer:
            return

        items = [
            {
                "item_code": row.item_code,
                "qty": row.qty,
                "uom": row.uom,
                "rate": row.sell_rate,
                "description": row.description,
                "schedule_date": self.planned_departure or nowdate(),
            }
            for row in self.services or []
            if row.item_code and flt(row.qty) > 0
        ]

        if not items:
            return

        sales_order = frappe.get_doc(
            {
                "doctype": "Sales Order",
                "company": self.company,
                "customer": self.customer,
                "transaction_date": nowdate(),
                "delivery_date": self.planned_departure or nowdate(),
                "currency": self.currency,
                "items": items,
            }
        )
        sales_order.insert(ignore_permissions=True)
        self.db_set("sales_order", sales_order.name)

    def _create_buying_document(self):
        if self.purchase_order or not self.supplier:
            return

        items = [
            {
                "item_code": row.item_code,
                "qty": row.qty,
                "uom": row.uom,
                "rate": row.buy_rate,
                "description": row.description,
                "schedule_date": self.planned_departure or nowdate(),
            }
            for row in self.services or []
            if row.item_code and flt(row.qty) > 0
        ]

        if not items:
            return

        purchase_order = frappe.get_doc(
            {
                "doctype": "Purchase Order",
                "company": self.company,
                "supplier": self.supplier,
                "transaction_date": nowdate(),
                "schedule_date": self.planned_departure or nowdate(),
                "currency": self.currency,
                "items": items,
            }
        )
        purchase_order.insert(ignore_permissions=True)
        self.db_set("purchase_order", purchase_order.name)


@frappe.whitelist()
def create_linked_invoices(job_name):
    job = frappe.get_doc("Logistics Job", job_name)

    created = {}
    if not job.sales_invoice and job.customer:
        sales_items = [
            {
                "item_code": row.item_code,
                "qty": row.qty,
                "uom": row.uom,
                "rate": row.sell_rate,
                "description": row.description,
            }
            for row in job.services or []
            if row.item_code and flt(row.qty) > 0
        ]

        if sales_items:
            sales_invoice = frappe.get_doc(
                {
                    "doctype": "Sales Invoice",
                    "company": job.company,
                    "customer": job.customer,
                    "posting_date": nowdate(),
                    "due_date": nowdate(),
                    "currency": job.currency,
                    "items": sales_items,
                }
            )
            sales_invoice.insert(ignore_permissions=True)
            job.db_set("sales_invoice", sales_invoice.name)
            created["sales_invoice"] = sales_invoice.name

    if not job.purchase_invoice and job.supplier:
        purchase_items = [
            {
                "item_code": row.item_code,
                "qty": row.qty,
                "uom": row.uom,
                "rate": row.buy_rate,
                "description": row.description,
            }
            for row in job.services or []
            if row.item_code and flt(row.qty) > 0
        ]

        if purchase_items:
            purchase_invoice = frappe.get_doc(
                {
                    "doctype": "Purchase Invoice",
                    "company": job.company,
                    "supplier": job.supplier,
                    "posting_date": nowdate(),
                    "due_date": nowdate(),
                    "currency": job.currency,
                    "items": purchase_items,
                }
            )
            purchase_invoice.insert(ignore_permissions=True)
            job.db_set("purchase_invoice", purchase_invoice.name)
            created["purchase_invoice"] = purchase_invoice.name

    return {
        "job": job.name,
        "created": created,
    }

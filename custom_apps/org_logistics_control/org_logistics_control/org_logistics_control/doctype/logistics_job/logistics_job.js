frappe.ui.form.on("Logistics Job", {
  refresh(frm) {
    if (frm.doc.docstatus !== 1) return;

    if (!frm.doc.sales_invoice || !frm.doc.purchase_invoice) {
      frm.add_custom_button("Create Accounting Docs", () => {
        frappe.call({
          method:
            "org_logistics_control.org_logistics_control.doctype.logistics_job.logistics_job.create_linked_invoices",
          args: { job_name: frm.doc.name },
          freeze: true,
          freeze_message: "Creating Sales/Purchase Invoice...",
          callback() {
            frm.reload_doc();
          },
        });
      });
    }
  },
});

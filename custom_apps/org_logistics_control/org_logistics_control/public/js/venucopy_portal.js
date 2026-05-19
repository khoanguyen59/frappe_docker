(function initVenucopyPortal() {
  const kpiEl = document.getElementById("venucopy-kpis");
  const tableBody = document.querySelector("#venucopy-jobs-table tbody");
  const companyTag = document.getElementById("venucopy-company-tag");
  if (!kpiEl || !tableBody) return;

  fetch("/api/method/org_logistics_control.venucopy_portal.get_dashboard_data", {
    credentials: "same-origin",
  })
    .then((r) => r.json())
    .then((payload) => {
      const data = payload && payload.message ? payload.message : {};
      renderKpis(kpiEl, data.kpis || {});
      renderRows(tableBody, data.recent_jobs || []);
      if (companyTag) {
        companyTag.textContent = data.company ? `Company: ${data.company}` : "";
      }
    })
    .catch(() => {
      kpiEl.innerHTML = "<div class='venucopy-kpi'><div class='venucopy-kpi-label'>Error</div><div class='venucopy-kpi-value'>Unable to load</div></div>";
    });
})();

function renderKpis(container, kpis) {
  const blocks = [
    ["Total Jobs", kpis.jobs_total || 0],
    ["Payment Stage", kpis.jobs_payment || 0],
    ["Pending Delivery", kpis.jobs_pending_delivery || 0],
  ];

  container.innerHTML = blocks
    .map(
      ([label, value]) =>
        `<div class="venucopy-kpi"><div class="venucopy-kpi-label">${label}</div><div class="venucopy-kpi-value">${value}</div></div>`
    )
    .join("");
}

function renderRows(tbody, rows) {
  if (!rows.length) {
    tbody.innerHTML = "<tr><td colspan='7'>No jobs found</td></tr>";
    return;
  }

  tbody.innerHTML = rows
    .map((row) => {
      const ref = row.cargo_reference || "-";
      const customer = row.customer || row.supplier || "-";
      const margin = toMoney(row.total_margin);
      const url = `/app/logistics-job/${encodeURIComponent(row.name)}`;
      return `<tr>
        <td><a href="${url}">${escapeHtml(row.name)}</a></td>
        <td>${escapeHtml(ref)}</td>
        <td>${escapeHtml(customer)}</td>
        <td>${escapeHtml(row.order_status || "-")}</td>
        <td>${escapeHtml(row.payment_status || "-")}</td>
        <td>${escapeHtml(row.delivery_status || "-")}</td>
        <td>${margin}</td>
      </tr>`;
    })
    .join("");
}

function toMoney(value) {
  const n = Number(value || 0);
  return n.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

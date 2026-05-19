(function startOrgUIControl() {
  let initialized = false;

  const init = () => {
    if (initialized || !window.frappe || !frappe.boot) return;
    initialized = true;

    const p = frappe.boot.org_ui_profile || {};
    const theme = frappe.boot.org_ui_theme || {};
    if (!Object.keys(p).length) {
      renderProfileBadge({ company: "No active profile" }, true);
      return;
    }

    renderProfileBadge(p, false);
    applyTheme(theme);
    applyProfile(p);

    const observer = new MutationObserver(() => applyProfile(p));
    observer.observe(document.body, { childList: true, subtree: true });

    if (frappe.router && frappe.router.on) {
      frappe.router.on("change", () => applyProfile(p));
    }

    // Keep default desk routing stable; do not force homepage client-side.
  };

  const waitForBoot = () => {
    if (window.frappe && frappe.boot) {
      init();
      return;
    }
    setTimeout(waitForBoot, 500);
  };

  waitForBoot();
})();

function applyProfile(profile) {
  const hidden = [...(profile.hide_workspaces || []), ...(profile.hide_modules || [])];
  hideCards(hidden);
  hideSidebarEntries(hidden);
  hideNavbarEntries(hidden);
  hideByRouteSlug(hidden);

  if (normalizeName(profile.company) === "venucopy") {
    enforceVenucopyAllowlist();
  }
}

function applyTheme(theme) {
  const t = {
    font_family: "'Satoshi', 'Manrope', 'Segoe UI', sans-serif",
    color_bg: "#f8f9ff",
    color_surface: "#ffffff",
    color_text: "#111827",
    color_muted: "#6b7280",
    color_primary: "#5055a5",
    color_primary_contrast: "#ffffff",
    color_accent: "#6c63ff",
    radius: "12px",
    ...theme,
  };

  const root = document.documentElement;
  root.style.setProperty("--org-font", t.font_family);
  root.style.setProperty("--org-bg", t.color_bg);
  root.style.setProperty("--org-surface", t.color_surface);
  root.style.setProperty("--org-text", t.color_text);
  root.style.setProperty("--org-muted", t.color_muted);
  root.style.setProperty("--org-primary", t.color_primary);
  root.style.setProperty("--org-primary-contrast", t.color_primary_contrast);
  root.style.setProperty("--org-accent", t.color_accent);
  root.style.setProperty("--org-radius", t.radius);

  if (!document.getElementById("org-ui-theme-style")) {
    const style = document.createElement("style");
    style.id = "org-ui-theme-style";
    style.textContent = `
      body {
        font-family: var(--org-font) !important;
        background: linear-gradient(123.49deg, #e3e8fe 4.93%, #faf3eb 105.81%) !important;
        color: var(--org-text) !important;
      }
      .page-container,
      .layout-main-section,
      .widget,
      .module-card,
      .workspace-card,
      .desk-sidebar,
      .section-head {
        border-radius: var(--org-radius) !important;
      }
      .page-title .title-text,
      .layout-main-section h3,
      .layout-main-section h4 {
        color: var(--org-text) !important;
      }
      .btn-primary {
        background: var(--org-primary) !important;
        border-color: var(--org-primary) !important;
        color: var(--org-primary-contrast) !important;
      }
      .navbar,
      .desk-sidebar {
        background: var(--org-surface) !important;
      }
      .indicator-pill,
      .indicator,
      .standard-sidebar-label {
        color: var(--org-muted) !important;
      }
      .widget.links-widget-box,
      .module-card,
      .workspace-card {
        border: 1px solid color-mix(in srgb, var(--org-primary) 16%, #d1d5db) !important;
      }
      .icon-sm,
      .text-primary {
        color: var(--org-primary) !important;
      }
    `;
    document.head.appendChild(style);
  }
}

function renderProfileBadge(profile, muted) {
  if (document.getElementById("org-ui-profile-badge")) return;

  const badge = document.createElement("div");
  badge.id = "org-ui-profile-badge";
  badge.textContent = `UI Profile: ${profile.company || "default"}`;
  badge.style.position = "fixed";
  badge.style.right = "16px";
  badge.style.bottom = "16px";
  badge.style.zIndex = "2147483647";
  badge.style.background = muted ? "#6b7280" : "#5055a5";
  badge.style.color = "#ffffff";
  badge.style.padding = "6px 10px";
  badge.style.borderRadius = "8px";
  badge.style.fontSize = "12px";
  badge.style.boxShadow = "0 8px 20px rgba(0, 0, 0, 0.2)";
  badge.style.cursor = "pointer";
  badge.title = "Open your user defaults";
  badge.onclick = () => {
    const user = window.frappe?.session?.user;
    if (!user || user === "Guest") return;
    if (window.frappe?.set_route) {
      frappe.set_route("Form", "User", user);
      return;
    }
    window.location.hash = `#Form/User/${encodeURIComponent(user)}`;
    setTimeout(() => {
      if (!window.location.hash.includes("#Form/User/")) {
        window.location.href = `/desk#Form/User/${encodeURIComponent(user)}`;
      }
    }, 250);
  };
  document.body.appendChild(badge);
}

function hideCards(values) {
  if (!Array.isArray(values) || !values.length) return;

  const hidden = values.map((x) => normalizeName(x)).filter(Boolean);
  document
    .querySelectorAll(
      ".module-card, .workspace-card, .widget.links-widget-box, [data-module-name]"
    )
    .forEach((node) => {
      const text = normalizeName(
        node.getAttribute("data-module-name") ||
          node.querySelector(".module-title, .title-text, .widget-title, .h4")?.textContent ||
          ""
      );

      if (matchesHidden(text, hidden)) {
        node.style.display = "none";
      }
    });
}

function hideSidebarEntries(values) {
  if (!Array.isArray(values) || !values.length) return;
  const hidden = values.map((x) => normalizeName(x)).filter(Boolean);

  document
    .querySelectorAll(
      ".desk-sidebar .standard-sidebar-item, .desk-sidebar .desk-sidebar-item, .layout-side-section a, .standard-sidebar-item"
    )
    .forEach((node) => {
      const text = normalizeName(node.textContent || "");
      if (matchesHidden(text, hidden)) {
        node.style.display = "none";
      }
    });
}

function hideNavbarEntries(values) {
  if (!Array.isArray(values) || !values.length) return;
  const hidden = values.map((x) => normalizeName(x)).filter(Boolean);

  document.querySelectorAll(".navbar a, .dropdown-menu a").forEach((node) => {
    const text = normalizeName(node.textContent || "");
    const href = normalizeName(node.getAttribute("href") || "");
    if (!text) return;
    if (matchesHidden(text, hidden) || matchesHidden(href, hidden)) {
      node.style.display = "none";
    }
  });
}

function matchesHidden(value, hiddenList) {
  if (!value || !hiddenList.length) return false;
  for (const token of hiddenList) {
    if (!token) continue;
    if (value === token || value.includes(token) || token.includes(value)) {
      return true;
    }
  }
  return false;
}

function hideByRouteSlug(values) {
  if (!Array.isArray(values) || !values.length) return;

  const slugs = values
    .map((v) => normalizeName(v))
    .filter(Boolean)
    .map((v) => v.replace(/\s+/g, "-").replace(/[^a-z0-9-]/g, ""));

  if (!slugs.length) return;

  document.querySelectorAll("a[href], [data-route], [data-link-to], [data-module-name]").forEach((node) => {
    const href = String(node.getAttribute("href") || "").toLowerCase();
    const dataRoute = String(node.getAttribute("data-route") || "").toLowerCase();
    const dataLinkTo = String(node.getAttribute("data-link-to") || "").toLowerCase();
    const dataModule = normalizeName(node.getAttribute("data-module-name") || "").replace(/\s+/g, "-");

    const hit = slugs.some(
      (slug) =>
        href.includes(`/app/${slug}`) ||
        href.includes(`/desk#workspace/${slug}`) ||
        dataRoute.includes(slug) ||
        dataLinkTo.includes(slug) ||
        dataModule.includes(slug)
    );

    if (!hit) return;
    const container = node.closest("li, .standard-sidebar-item, .workspace-card, .module-card, .widget, .dropdown-item") || node;
    container.style.display = "none";
  });
}

function enforceVenucopyAllowlist() {
  const allowed = ["selling", "buying", "accounting", "venucopy", "logistics"];

  document
    .querySelectorAll(
      ".module-card, .workspace-card, .widget.links-widget-box, .standard-sidebar-item, .desk-sidebar-item"
    )
    .forEach((node) => {
      const text = normalizeName(node.textContent || "");
      const route = normalizeName(
        node.getAttribute("data-route") ||
          node.getAttribute("data-link-to") ||
          node.getAttribute("data-module-name") ||
          ""
      );
      const href = normalizeName(node.getAttribute("href") || "");
      const hay = `${text} ${route} ${href}`;
      const keep = allowed.some((key) => hay.includes(key));
      if (!keep) node.style.display = "none";
    });
}

function normalizeName(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\s+/g, " ");
}

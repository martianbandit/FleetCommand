const loadingOverlay = document.getElementById("loadingOverlay");
const syncButton = document.getElementById("syncButton");
const activityLog = document.getElementById("activityLog");

const logActivity = (message) => {
  const entry = document.createElement("p");
  entry.textContent = `${new Date().toLocaleTimeString()} · ${message}`;
  activityLog.prepend(entry);
};

const toggleLoading = (isActive) => {
  if (isActive) {
    loadingOverlay.classList.add("active");
    loadingOverlay.setAttribute("aria-hidden", "false");
  } else {
    loadingOverlay.classList.remove("active");
    loadingOverlay.setAttribute("aria-hidden", "true");
  }
};

const simulateRequest = (label) => {
  toggleLoading(true);
  logActivity(`${label} - requête en cours`);
  window.setTimeout(() => {
    toggleLoading(false);
    logActivity(`${label} - réponse 200 OK`);
  }, 1400);
};

syncButton?.addEventListener("click", () => {
  simulateRequest("Synchronisation globale");
});

const actionButtons = document.querySelectorAll("[data-action]");
actionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    simulateRequest(button.dataset.action.replace("-", " "));
  });
});

const forms = document.querySelectorAll(".panel-form");
forms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const endpoint = form.dataset.endpoint;
    simulateRequest(`POST ${endpoint}`);
    form.reset();
  });
});

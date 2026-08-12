const TAB_IDS = [
  "setup",
  "intro",
  "how-it-works",
  "landmarks",
  "gesture",
  "images",
  "challenge",
  "wrapup",
];

async function loadTabs() {
  const stage = document.getElementById("stage");
  const sources = await Promise.all(
    TAB_IDS.map((id) => fetch(`tabs/${id}.html`).then((res) => res.text()))
  );
  stage.innerHTML = sources.join("\n");

  initTabNav();
  initOsPicker();
  if (window.initPixelLab) window.initPixelLab();
  if (window.initStepViewer) window.initStepViewer();
}

function initTabNav() {
  const buttons = document.querySelectorAll(".tab-btn");
  const panels = document.querySelectorAll(".panel");

  function showPanel(id) {
    panels.forEach((panel) => panel.classList.toggle("active", panel.id === id));
    buttons.forEach((btn) => btn.classList.toggle("active", btn.dataset.target === id));
  }

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => showPanel(btn.dataset.target));
  });
}

function initOsPicker() {
  const osButtons = document.querySelectorAll(".os-btn");
  const osPanels = document.querySelectorAll(".os-panel");

  function showOS(id) {
    osPanels.forEach((panel) => panel.classList.toggle("active", panel.id === id));
    osButtons.forEach((btn) => btn.classList.toggle("active", btn.dataset.os === id));
  }

  osButtons.forEach((btn) => {
    btn.addEventListener("click", () => showOS(btn.dataset.os));
  });
}

function initEntryScreen() {
  const entryScreen = document.getElementById("entry-screen");
  const enterButton = document.getElementById("enter-workshop");

  if (!entryScreen || !enterButton) return;

  enterButton.addEventListener("click", () => {
    entryScreen.classList.add("hidden");
    enterButton.focus();
    setTimeout(() => entryScreen.remove(), 300);
  });
}

initEntryScreen();
loadTabs();

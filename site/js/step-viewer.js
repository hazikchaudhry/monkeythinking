window.initStepViewer = function initStepViewer() {
  document.querySelectorAll(".step-viewer").forEach((viewer) => {
    const scenes = viewer.querySelectorAll(".step-scene");
    if (!scenes.length) return;

    const backBtn = viewer.querySelector(".step-back");
    const nextBtn = viewer.querySelector(".step-next");
    const counterEl = viewer.querySelector(".step-counter");
    const titleEl = viewer.querySelector(".step-title");
    const captionEl = viewer.querySelector(".step-caption");
    const steps = JSON.parse(viewer.dataset.steps);

    let current = 0;

    function render() {
      scenes.forEach((scene) => {
        scene.classList.toggle("active", Number(scene.dataset.step) === current);
      });
      counterEl.textContent = `Step ${current + 1} of ${steps.length}`;
      titleEl.textContent = steps[current].title;
      captionEl.textContent = steps[current].caption;
      backBtn.disabled = current === 0;
      nextBtn.disabled = current === steps.length - 1;
    }

    backBtn.addEventListener("click", () => {
      if (current > 0) {
        current -= 1;
        render();
      }
    });

    nextBtn.addEventListener("click", () => {
      if (current < steps.length - 1) {
        current += 1;
        render();
      }
    });

    render();
  });
};

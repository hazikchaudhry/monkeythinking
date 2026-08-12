window.initPixelLab = function initPixelLab() {
  const canvas = document.getElementById("pixelLabCanvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const rSlider = document.getElementById("pixelLabR");
  const gSlider = document.getElementById("pixelLabG");
  const bSlider = document.getElementById("pixelLabB");
  const resetBtn = document.getElementById("pixelLabReset");

  let original = null;

  function render() {
    if (!original) return;
    const out = ctx.createImageData(original.width, original.height);
    const rMul = rSlider.value / 100;
    const gMul = gSlider.value / 100;
    const bMul = bSlider.value / 100;

    for (let i = 0; i < original.data.length; i += 4) {
      out.data[i] = Math.min(255, original.data[i] * rMul);
      out.data[i + 1] = Math.min(255, original.data[i + 1] * gMul);
      out.data[i + 2] = Math.min(255, original.data[i + 2] * bMul);
      out.data[i + 3] = original.data[i + 3];
    }
    ctx.putImageData(out, 0, 0);
  }

  const img = new Image();
  img.onload = () => {
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    ctx.drawImage(img, 0, 0);
    original = ctx.getImageData(0, 0, canvas.width, canvas.height);
    render();
  };
  img.src = "assets/deva.png";

  [rSlider, gSlider, bSlider].forEach((slider) => {
    slider.addEventListener("input", render);
  });

  resetBtn.addEventListener("click", () => {
    rSlider.value = 100;
    gSlider.value = 100;
    bSlider.value = 100;
    render();
  });
};

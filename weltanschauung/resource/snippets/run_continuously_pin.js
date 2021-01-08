window.setInterval(() => {
  const sel = ".jp-LinkedOutputView .jp-OutputArea-output";
  const outputElement = document.querySelector(sel);
  outputElement.scrollTop = outputElement.scrollHeight;
}, 500);
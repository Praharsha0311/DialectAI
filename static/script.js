// static/script.js

const micButton = document.getElementById('voice-input');
const translateBtn = document.getElementById('translate-btn');
const inputField = document.getElementById('telugu-input');
const stdOutput = document.getElementById('standard-output');
const engOutput = document.getElementById('english-output');
const dialectOutput = document.getElementById('dialect-output');
const listenBtn = document.getElementById('listen-btn');
const copyBtn = document.getElementById('copy-btn');
const saveBtn = document.getElementById('save-btn');

// Voice Input Handling
micButton.addEventListener('click', () => {
  fetch('/voice-input')
    .then((res) => res.json())
    .then((data) => {
      inputField.value = data.text;
    })
    .catch((err) => {
      console.error('Error:', err);
      alert('Voice recognition failed');
    });
});

// Translation Handling
translateBtn.addEventListener('click', () => {
  const inputText = inputField.value.trim();
  if (!inputText) {
    alert('Please enter some text.');
    return;
  }

  fetch('/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: inputText }),
  })
    .then((res) => res.json())
    .then((data) => {
      stdOutput.textContent = data.standard_telugu;
      engOutput.textContent = data.english_translation;
      dialectOutput.textContent = data.detected_dialect;
    })
    .catch((err) => console.error('Translation error:', err));
});

// Listen Button
listenBtn.addEventListener('click', () => {
  const text = engOutput.textContent;
  if (!text) return;
  const speech = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(speech);
});

// Copy Button
copyBtn.addEventListener('click', () => {
  const text = engOutput.textContent;
  navigator.clipboard.writeText(text);
  alert('Translation copied to clipboard!');
});

// Save Button
saveBtn.addEventListener('click', () => {
  const data = {
    input: inputField.value,
    standard: stdOutput.textContent,
    english: engOutput.textContent,
    dialect: dialectOutput.textContent,
  };
  fetch('/save-translation', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((response) => {
      alert('Translation saved successfully!');
    })
    .catch((err) => console.error('Save error:', err));
});

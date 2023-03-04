const speechRecognition =
  window.webkitSpeechRecognition || //Google Chrome
  window.SpeechRecognition; //Firefox

function startListening() {
  const recong = new speechRecognition();
  recong.start();
  recong.onstart = null;
  recong.onresult = function (data) {
    handleResults(data);
  };
  recong.onend = function () {
    recong.start();
  };
}
async function handleResults(data) {
  let text = data.results[0][0].transcript;
  text = text.toLowerCase();
  const resp = await axios.post("http://localhost:5000", { message: text });
  //the text i am asking
  console.log(text);
  console.log(resp);
  Speak(resp.data);
}

function Speak(TEXT) {
  const utter = new SpeechSynthesisUtterance();
  let counter = 0;

  utter.text = TEXT;
  utter.lang = "en-IN";
  utter.voice = window.speechSynthesis.getVoices()[1];

  // console.log(utter.voice);
  utter.lang = "en-IN";
  window.speechSynthesis.speak(utter);
  // window.speechSynthesis.getVoices().forEach((i) => {
  //   console.log(`${counter++}. ${i.voiceURI}`);
  // });
}

startListening();

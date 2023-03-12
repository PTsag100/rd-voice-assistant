const item = document.querySelector(".item");
let todos = null;
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
  Speak(resp.data[0]);
  if (resp.data[0] === "Goodbye sir") {
    setTimeout(() => window.close(), 3000);
  }
  if (resp.data.length > 1) {
    if (resp.data[1][0].type === "weather") {
      Panel(
        "weather",
        `<h1>Weather in ${resp.data[1][1]}</h1>
      <img src="https://openweathermap.org/img/wn/${resp.data[1][2]}@2x.png" alt="" />
      <h1>${resp.data[1][4]}&#176;F</h1>
    
      <h3>Humidity:${resp.data[1][5]}</h3>
      <h3>Wind speed:${resp.data[1][6]}</h3>`,
        500
      );
    } else if (resp.data[1][0].type === "close") {
      closePanel();
    } else if (resp.data[1][0].type === "speak") {
      Speak(resp.data[1][1]);
    } else if (resp.data[1][0].type === "time") {
      Panel("time", `<h1>${resp.data[1][1]}</h1>`, 500);
      Speak(resp.data[1][1]);
    } else if (resp.data[1][0].type === "date") {
      Speak(resp.data[1][1]);
      Panel("date", `<h1>${resp.data[1][1]}</h1>`, 500);
    } else if (resp.data[1][0].type === "internet") {
      Panel(
        "internet-speed-loading",
        ` <div class="loader">
      <svg class="circular-loader" viewBox="25 25 50 50">
        <circle
          class="loader-path"
          cx="50"
          cy="50"
          r="20"
          fill="none"
          stroke="#667fd8"
          stroke-width="1"
        />
      </svg>
      <h1>Checking Speed...</h1>
    </div>`,
        1000
      );
      const speed = await axios.get("http://localhost:5000/internet");
      Speak(
        `Your download speed is ${speed.data[0]}  Megabyte per second and your upload speed is ${speed.data[1]} Megabyte per second`
      );
      Panel(
        "internet-speed-loaded",
        `
      <h1>Download: <span>${speed.data[0]} Mbps</span></h1>
      <h1>Upload: <span>${speed.data[1]} Mbps</span></h1>`,
        500
      );
    } else if (resp.data[1][0].type === "todo") {
      let id = 0;
      let todoHTML = ``;
      todos = resp.data[1][1];
      todos.forEach((todo) => {
        id += 1;
        todoHTML += `<div class="checkbox-wrapper-15" onclick="changeTodo()">
        <input
          class="inp-cbx"
          id="cbx-${id}"
          type="checkbox"
          style="display: none"
         ${todo.completed ? "checked" : ""}
        />
        <label class="cbx" for="cbx-${id}">
          <span>
            <svg width="12px" height="9px" viewbox="0 0 12 9">
              <polyline points="1 5 4 8 11 1"></polyline>
            </svg>
          </span>
          <span>${todo.todo}</span>
        </label>
      </div>`;
      });
      Panel("todo-list", todoHTML, 500);
    }
  }
}

function Panel(type, content, delay = 500) {
  item.className = "item";
  item.classList.add(type);
  item.innerHTML = ``;
  setTimeout(() => {
    item.innerHTML = content;
  }, delay);
}

function closePanel() {
  item.className = "";
  item.classList.add("item");
  item.innerHTML = `<h1>RD</h1>`;
}

function Speak(TEXT) {
  const utter = new SpeechSynthesisUtterance();

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

async function changeTodo() {
  const inputs = document.querySelectorAll(".checkbox-wrapper-15 input");
  inputs.forEach((input, index) => {
    todos[index].completed = input.checked;
  });
  await axios.post("http://localhost:5000/changetodo", { todos });
}

startListening();

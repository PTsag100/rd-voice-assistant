import "./App.css";
import { useEffect } from "react";
function App() {
  const SpeechRecognition =
    window.webkitSpeechRecognition || //Google Chrome
    window.SpeechRecognition; //Firefox
  console.log("mic found");
  const recong = new SpeechRecognition();
  function startListening() {
    try {
      console.log("listening");
      recong.start();
      recong.onstart = null;
      recong.onresult = function (data) {
        if (data != null) {
          console.log("data");
          handleResults(data);
        }
      };
      recong.onend = function () {
        console.log("stoped");
        recong.start();
        console.log("started again");
      };
    } catch (error) {
      console.log(error);
    }
  }
  function handleResults(data) {
    let text = data.results[0][0].transcript;
    text = text.toLowerCase();
    //the text i am asking
    console.log(text);
  }

  useEffect(() => {
    startListening();
  }, []);
  return <div className="App">sdf</div>;
}

export default App;

// const Dictaphone = () => {
//   const {
//     transcript,
//     listening,
//     resetTranscript,
//     browserSupportsSpeechRecognition,
//   } = useSpeechRecognition();

//   if (!browserSupportsSpeechRecognition) {
//     return <span>Browser doesn't support speech recognition.</span>;
//   }

//   return (
//     <div>
//       <p>Microphone: {listening ? "on" : "off"}</p>
//       <button
//         onClick={() => {
//           SpeechRecognition.startListening();
//         }}
//       >
//         Start
//       </button>
//       <button
//         onClick={() => {
//           SpeechRecognition.stopListening();
//           console.log(transcript);
//         }}
//       >
//         Stop
//       </button>
//       <button onClick={resetTranscript}>Reset</button>
//       <p>{transcript}</p>
//     </div>
//   );
// };
// export default Dictaphone;

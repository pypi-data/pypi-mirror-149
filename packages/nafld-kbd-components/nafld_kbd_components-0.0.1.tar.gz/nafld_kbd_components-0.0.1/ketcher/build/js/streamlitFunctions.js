function sendMessageToStreamlitClient(type, data) {
  var outData = Object.assign(
    {
      isStreamlitMessage: true,
      type: type,
    },
    data
  );
  window.parent.postMessage(outData, "*");
}

function init() {
  sendMessageToStreamlitClient("streamlit:componentReady", { apiVersion: 1 });
}

function setFrameHeight(height) {
  sendMessageToStreamlitClient("streamlit:setFrameHeight", { height: height });
}

// The `data` argument can be any JSON-serializable value.
const sendDataToPython = (data) => {
  sendMessageToStreamlitClient("streamlit:setComponentValue", data);
}

// data is any JSON-serializable value you sent from Python,
// and it's already deserialized for you.
function onDataFromPython(event) {
  if (event.data.type !== "streamlit:render") return;
  // pass
}

window.addEventListener("message", onDataFromPython);
init();

// Hack to autoset the iframe height.
window.addEventListener("load", function () {
  window.setTimeout(function () {
    setFrameHeight(document.documentElement.clientHeight);
  }, 0);
});

setFrameHeight(660);

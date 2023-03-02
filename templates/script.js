const cOutput = document.getElementById("output");
const cSensor = document.getElementById("sensor");
const cTrigger = document.getElementById("trigger");
const video = document.getElementById("video");
// Start Cam function
const startCam = () => {
  //Initialize video
  

  // validate video element
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        video.srcObject = stream;
      })
      .catch(function (error) {
        console.log("Something went wrong!");
      });
  }
};

// Stop the webcam function
const stopCam = () => {
  let stream = video.srcObject;
  let tracks = stream.getTracks();
  tracks.forEach((track) => track.stop());
  video.srcObject = null;
};
// Take a picture when cameraTrigger is tapped
cTrigger.onclick = function() {
  cSensor.width = video.videoWidth;
  cSensor.height = video.videoHeight;
  cSensor.getContext("2d").drawImage(video, 0, 0);
  cOutput.src = cSensor.toDataURL("image/webp");
  cOutput.classList.add("taken");
};

$(() => {
  startCam();
});

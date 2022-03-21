$(document).ready(function(){
  let namespace = "/test";

  let userInput = document.querySelector("#userInput");
  let submitButton = document.querySelector("#submit")
  submitButton.onclick = function() {sendInput()};
  var localMediaStream = null;

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }
  }

  socket.on('connect', function() {
    console.log('Connected!');
    const sessionID = socket.id;
    console.log(sessionID)
    var imageElement = document.getElementById("imageElement");
    var userID = sessionID.replace("/test#", "")
    console.log(userID);
    
    var tempp = '/video_feed/'.concat(userID);
    console.log(tempp);  
    // console.log(imageElement.src);
    // imageElement.src = (imageElement.src).concat(tempp)
    // console.log(imageElement.src);

  });

  socket.on('classified', function(prediction){
    console.log("Text classified!");
    var result = document.getElementById("result");
    result.innerHTML = "Predicted: " + prediction;;  
  });
  

  var constraints = {
    // video: {
    //   width: { min: 640 },
    //   height: { min: 480 }
    // }
  };

  // navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
  //   video.srcObject = stream;
  //   localMediaStream = stream;

  //   setInterval(function () {
  //     sendSnapshot();
  //   }, 500);
  // }).catch(function(error) {
  //   console.log(error);
  // });



  function sendInput() {
    socket.emit('input image', userInput.value);
  }

});


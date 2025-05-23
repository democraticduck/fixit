const btn = document.getElementById("locBtn");
btn.addEventListener("click", function () {
  console.log("hii");
  navigator.geolocation.getCurrentPosition(success, error);
});

function success(pos) {
  console.log(position.coords.latitude, " ", position.coords.longitude);
}

function error() {
  alert("Sorry, no position available.");
}

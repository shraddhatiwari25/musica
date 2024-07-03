const movie = document.getElementById("movies");
const songs = document.getElementById("songs");
const btn = document.getElementById("btn-switch");
const load = document.getElementById("loadMore");

var retrievedObject = localStorage.getItem('state');
if(retrievedObject == 'songs'){
    recSongs();
}

function recMovie() {
  btn.style.left = "0";
  movie.style.display = "block";
  songs.style.display = "none";
  localStorage.clear();
}

function recSongs() {
  btn.style.left = "48%";
  songs.style.display = "block";
  movie.style.display = "none";
  localStorage.setItem('state', 'songs');
}


var keysToMove = document.getElementsByClassName("key_2");
var keys = document.getElementsByClassName("key_1");
var distances = [28, 65, 139, 175, 212, 287, 324, 398, 434, 471, 546, 583, 657, 694, 732, 805, 842, 915, 953, 990, 1064, 1101, 1174, 1212, 1249];
var pianoMenuItem = document.getElementsByClassName("piano_menu_bottom_item");
var headerMenuImages = document.getElementsByClassName("menu_item_img");
var headerMenuTitles = document.getElementsByClassName("piano_menu_bottom_item_title");

for (let i = 0; i < keysToMove.length; i++) {

    moveDistance = distances[i] + 301 + "px";
    keysToMove[i].style.left = moveDistance;

}

for (let i = 0; i < pianoMenuItem.length; i++) {

    pianoMenuItem[i].addEventListener("mouseover", event => {

        headerMenuImages[i].style.display = "block";
        headerMenuTitles[i].style.color = "#fff";

    })

        pianoMenuItem[i].addEventListener("mouseout", event => {

        headerMenuImages[i].style.display = "none";
        headerMenuTitles[i].style.color = "#939393";

    })

}

console.log(keyboardNotes);
document.addEventListener("keydown", event => {

    note = keyboardNotes[event.key];
    sound = keyboardSounds[event.key];
    if (!(typeof(note) === 'undefined')) {
        console.log(note);
        console.log(sound);
        var fileLocation = "../static/keys_mp3/" + sound + ".mp3"
        var audio = new Audio(fileLocation);
        console.log(audio);
        console.log(fileLocation);
        audio.play();

    }

})

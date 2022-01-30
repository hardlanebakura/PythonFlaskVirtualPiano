var musicSheetsElementButton = document.getElementsByClassName("music_sheets_element_button");
var musicSheetsArtistLink = document.getElementsByClassName("music_sheets_link");
var genreNames = document.getElementsByClassName("genre_name");
var genreLinks = document.getElementsByClassName("genre_link");
var themeNames = document.getElementsByClassName("theme_name");
var artistNames = document.getElementsByClassName("artist_name")
genreNames = Array.from(genreNames).concat(Array.from(themeNames).concat(Array.from(artistNames)));

for (let i = 0; i < musicSheetsElementButton.length; i++) {

    console.log(musicSheetsArtistLink[i].getAttribute("href"));
    console.log(musicSheetsElementButton[i].innerText);
    musicSheetsArtistLink[i].setAttribute("href", `/music/sheets?letter=${musicSheetsElementButton[i].innerText}`);
    musicSheetsElementButton[i].addEventListener("click", event => {

        console.log("1");

    })

}

for (let i = 0; i < genreLinks.length; i++) {

    console.log(genreNames[i].innerText);
    genreLinks[i].href =  `/music/genres/${genreNames[i].innerText}`;

}
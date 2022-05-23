var artistsElementButton = document.getElementsByClassName("artists_element_button");
var musicSheetsElementButton = document.getElementsByClassName("music_sheets_element_button");
var artistsLink = document.getElementsByClassName("artists_link");
var musicSheetsLink = document.getElementsByClassName("music_sheets_link");
var genreNames = document.getElementsByClassName("genre_name");
var genreLinks = document.getElementsByClassName("genre_link");
var themeNames = document.getElementsByClassName("theme_name");
var artistNames = document.getElementsByClassName("artist_name");
genreNames = Array.from(genreNames).concat(Array.from(themeNames).concat(Array.from(artistNames)));

for (let i = 0; i < artistsElementButton.length; i++) {

    artistsLink[i].setAttribute("href", `/music/artists?letter=${artistsElementButton[i].innerText}`);
    artistsElementButton[i].addEventListener("click", event => {

        console.log("1");

    })

}

for (let i = 0; i < musicSheetsElementButton.length; i++) {

    musicSheetsLink[i].setAttribute("href", `/music/sheets?letter=${musicSheetsElementButton[i].innerText}`);
    musicSheetsElementButton[i].addEventListener("click", event => {

        console.log("1");

    })

}

for (let i = 0; i < genreLinks.length; i++) {

    console.log(genreNames[i].innerText);
    genreLinks[i].href =  `/music/genres/${genreNames[i].innerText}`;

}
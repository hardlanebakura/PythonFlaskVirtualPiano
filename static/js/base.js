var changeHover = document.getElementsByClassName("changetodoonhover");
var registerLoginLink = document.getElementById("registerloginlink");
var darkOrange = "#ff8300";

for (let i = 0; i < changeHover.length; i++) {

    changeHover[i].addEventListener("mouseover", event => {

        changeHover[i].style.backgroundColor = darkOrange;
        changeHover[i].style.color = "#000";
        (changeHover[i].innerText == "Register / Login") ? registerLoginLink.style.color = "#000" : {};

    })

    changeHover[i].addEventListener("mouseout", event => {

        changeHover[i].style.backgroundColor = "#000";
        changeHover[i].style.color = darkOrange;
        (changeHover[i].innerText == "Register / Login") ? registerLoginLink.style.color = darkOrange : {};

    })

}

var linkSocials = document.getElementsByClassName("link_socials");
var imgOriginalSources = [];
var imgOriginalNames = [];
var imgOriginalExtensions = [];
for (let i = 0; i < linkSocials.length; i++) {

    imgOriginalSources.push(linkSocials[i].getAttribute("src"));
    imgOriginalNames.push(linkSocials[i].getAttribute("src").split(".")[0]);
    imgOriginalExtensions.push("." + linkSocials[i].getAttribute("src").split(".")[1]);

    linkSocials[i].addEventListener("mouseover", event => {

        linkSocials[i].setAttribute("src", imgOriginalNames[i] + "-orange" + imgOriginalExtensions[i]);

    })

    linkSocials[i].addEventListener("mouseout", event => {

        linkSocials[i].setAttribute("src", imgOriginalSources[i]);

    })

}


var linkPlayElement = document.getElementById("link_play");
var linkPlay = linkPlayElement.childNodes[1];
var linkHowElement = document.getElementById("link_how");
var linkHow = linkHowElement.childNodes[1];
var linkAboutElement = document.getElementById("link_about");
var linkAbout = linkAboutElement.childNodes[1];
var isIndex = window.location.href === "http://127.0.0.1:5000/";
if (isIndex) {

    linkPlay.href = "#piano";
    linkHow.href = "#piano_hints";
    linkAbout.href = "#piano_info_title";

}

else {

    linkPlay.href = "/#piano";
    linkHow.href = "/#piano_hints";
    linkAbout.href = "/#piano_info_title";

}


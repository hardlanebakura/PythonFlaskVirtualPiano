musicSheetContent = document.getElementsByClassName("music_sheet_content_content")[0];

function editMusicSheet(sheet) {

    console.log(musicSheet[musicSheet.length - 1]);
    musicSheet = musicSheet.substr(2, musicSheet.length - 3);
    musicSheet = musicSheet.replace(/\\r\\n/g, "<br>");
    return musicSheet;

}

    musicSheetContent.innerHTML = editMusicSheet(musicSheet);
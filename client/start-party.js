var partyOn;
var songsUrl;
var partyNumber;
function startParty() {
    songsUrl = document.getElementById("url").value;
    //alert("Starting a new party.\r\n Will be pulling songs from the following url:\r\n" + songsUrl);
    partyNumber = getPartyNumber();
    
    partyOn = true;
}

function setUrl() {
    songsUrl = document.getElementById("url").value;
}

function getPartyNumber() {
    var numberUrl = 'http://173.204.223.99/cgi-bin/get_twilio_number.py?callback='
    jQuery.ajax(
    {
        url: numberUrl,
        success: partyNumberCallback,
        error: hmmm
    });
}

function hmmm(ach, t, e) {
    alert('damn '+t);
}

function partyNumberCallback(data) {
    var n;
    if (data.Number.length == 11) {
        n = ('+' + data.Number.substr(0, 1) + '-' + data.Number.substr(1, 3) + '-' + data.Number.substr(4, 3) + '-' + data.Number.substr(7));
    } else {
        n = data.Number;
    }
    document.getElementById("party_number").innerHTML = n+"<img src='sms.jpg' width=80 height=80 />";
    partyOn = true;
}

function playTrack(uri) {
    var sp = getSpotifyApi(1);
    var models = sp.require('sp://import/scripts/api/models');
    var player = models.player;
    player.playTrack(uri);
}



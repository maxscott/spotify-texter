var sp = getSpotifyApi(1);
var models = sp.require('sp://import/scripts/api/models');
var player = models.player;
var songsUrl = 'http://qwertyfest.99k.org/test.php?callback=';
var playlist = getTemporaryPlaylist();
exports.init = init;
exports.pullSongs = pullSongs;
var playing = false;
var songs = new Array();
//var timeSeries = new TimeSeries();

function init() {
	//sp.trackPlayer.playTrackFromContext(playlist.uri, 0, "", {
    //            onSuccess: nothing,
    //            onError: nothing,
    //            onComplete: nothing
    //        });

    player.observe(models.EVENT.CHANGE, function (e) {

        // Only update the page if the track changed
        if (e.data.curtrack == true) {
            updatePageWithTrackDetails();
        }
    });

    var drop = document.querySelector('#drop');
    //addEvent(drop, 'dragover', cancel);
    //addEvent(drop, 'dragenter', cancel);
	partyOn = true;
	//setInterval(pullSongs, 2000);
	pullSongs();
	//createTimeline();
}

function nothing(){}

function addSong(track, fromNumber) {
    if(!songs[track]){
        songs[track] = { from: fromNumber };
    }
}

var songsCallback = function (data) {

    var numberOfNewSongs = data.Songs.length;
    var newSongsContainer = document.getElementById("new_songs");
    newSongsContainer.innerHTML = "Received " + numberOfNewSongs + " new songs at " + (new Date).toLocaleTimeString() + "<br>Received " + playlist.length + " in total.";
    //timeSeries.append(new Date().getTime(), numberOfNewSongs);

    $(data.Songs).each(function (index) {
        var parts = data.Songs[index].split(',');
        var q = parts[1];
        var from = parts[0];
        console.log("test: " + q);
        var search = new models.Search(q);
        search.pageSize = 1;
        console.log("just: " + search.query);
        //search.localResults = models.LOCALSEARCHRESULTS.APPEND; //include local files        
        search.observe(models.EVENT.CHANGE, function () {
            var picked = false;
            console.log("searched for: " + search.query);
            for (var j in search.tracks) {
                var track = search.tracks[j];
                if (!picked && track.playable) {
                    $('#songs_table tr:last').after('<tr><td>' + '<img width=25 height=25 src="' + track.image + '"/>' + '</td><td>' + track.name + '</td><td>' + track.artists + '</td><td>' + track.album.name + '</td><td>' + dhm(track.duration) + '</td><td>' + from + '</td><td><img class=\'delete\' src=\'delete.png\'></img></td></tr>');//<a href="#" onClick="playTrack(\'' + track.uri + '\');">Play</a></td></tr>');
                    $('table td img.delete').click(function () {
                        $(this).parent().parent().remove();
                    });
                    picked = true;
                    playlist.add(track.uri);
                    break;
                }                
            }
            //make sure something is playing...

        });
        search.appendNext();
    });
}

function pullSongs() {
    console.log("pull");
    if (partyOn) {
        query(songsUrl, songsCallback);
    } else {
        console.log("party off");
    }
}

function query(url, callback){
	jQuery.ajax(
	{
		url: url, 
		success: callback
	});
}

function temporaryName() {
    return (Date.now() * Math.random()).toFixed();
}

function getTemporaryPlaylist() {
    var temporaryPlaylist = sp.core.getTemporaryPlaylist(temporaryName());
    sp.trackPlayer.setContextCanSkipPrev(temporaryPlaylist.uri, false);
    sp.trackPlayer.setContextCanRepeat(temporaryPlaylist.uri, false);
    sp.trackPlayer.setContextCanShuffle(temporaryPlaylist.uri, false);
    return temporaryPlaylist;
}

function dhm(t) {
    var ch = 60 * 60 * 1000,
        cm = 60 * 60 * 60 * 1000,
        h = Math.floor(t / ch),
        m = '0' + Math.round((t - h * ch) / 60000),
        s = '0' + Math.round((t - h * ch - m * cm) / 1000);
    return[h, m.substr(-2), s.substr(-2)].join(':');
}

//function createTimeline() {
//    var chart = new SmoothieChart();
//    chart.addTimeSeries(timeSeries, { strokeStyle: 'rgba(0, 255, 0, 1)', fillStyle: 'rgba(0, 255, 0, 0.2)', lineWidth: 4 });
//    chart.streamTo(document.getElementById("chart"), 2000);
//}

function updatePageWithTrackDetails() {

    //var header = document.getElementById("header");

    //// This will be null if nothing is playing.
    //var playerTrackInfo = player.track;

    //if (playerTrackInfo == null) {
    //    header.innerText = "Nothing playing!";
    //} else {
    //    var track = playerTrackInfo.data;
    //    header.innerHTML = track.name + " on the album " + track.album.name + " by " + track.album.artist.name + ".";
    //}
}
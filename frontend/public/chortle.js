const PORT = 5000;
const QUERY_ADDRESS = `http://localhost:${PORT}/query`;
//const POLL_FREQUENCY_SECONDS = 0.5;
const POLL_FREQUENCY_SECONDS = 4;
const MAX_CHORE_DISPLAY_TIME = 3*60*60;
var CHORE_DATA = [];

const TABLE_HEADERS = ["Chore", "Status", "Time Remaining"];
const TABLE_DATA_FIELDS = ["chore-name", "chore-status", "chore-time"];
const TABLE_DATA_FUNCTIONS = {
    "chore-name": function (choreRow) {
        var data = document.createElement("TD");
        data.innerText = choreRow.chore_name.S;
        return data;
    },

    "chore-status": function (choreRow) {
        var data = document.createElement("TD");
        if (getTimeRemaining(choreRow) < 0 && choreRow.active.BOOL) data.className = "status_bad";
        else data.className = "status_good";
        return data;
    },

    "chore-time": function (choreRow) {
        var data = document.createElement("TD");
        var timeRemaining = getTimeRemaining(choreRow)
        if (timeRemaining === null) {
            return data;
        } else if (!choreRow.active.BOOL || timeRemaining > MAX_CHORE_DISPLAY_TIME) {
            return data;
        } else {
            data.innerText = getStringFromTime(getTimeRemaining(choreRow));
            return data;
        }
    }
}

function getTimeRemaining(choreRow) {
    if ('last_pressed_time' in choreRow) {
        var choreExpireTime = parseInt(choreRow.last_pressed_time.N) + parseInt(choreRow.reset_time_seconds.N);
        var now = Math.floor(new Date().getTime() / 1000);
        var timeRemaining = choreExpireTime - now;
        return timeRemaining;
    } else {
        return null
    }
}

function getStringFromTime(timeValueSeconds) {
    var neg = timeValueSeconds < 0;
    if (neg) timeValueSeconds *= -1;
    var hours = Math.floor(timeValueSeconds / 3600);
    var minutes = Math.floor((timeValueSeconds % 3600) / 60);
    var seconds = Math.floor(timeValueSeconds % 60);
    var timeString = hours + ":" + ("0"+minutes).slice(-2) + ":" + ("0"+seconds).slice(-2);
    if (neg) timeString = "-"+timeString;
    return timeString;
}

function clearTable(table) {
    while (table.hasChildNodes()) {
        table.removeChild(table.firstChild)
    }
}

function buildTableHeader(table) {
    var headerRow = document.createElement("TR");
    for (var i = 0; i < TABLE_HEADERS.length; i++) {
        var headerElement = document.createElement("TH");
        headerElement.innerText = TABLE_HEADERS[i];
        headerRow.appendChild(headerElement);
    }
    table.appendChild(headerRow);
}

function buildTable() {
    var table = document.getElementById("chore-chart");
    clearTable(table);
    buildTableHeader(table);
    for (var i = 0; i < CHORE_DATA.length; i++) {
        var choreRow = CHORE_DATA[i];
        var rowElement = document.createElement("TR");
        for (var j = 0; j < TABLE_DATA_FIELDS.length; j++) {
            var field = TABLE_DATA_FIELDS[j];
            rowElement.appendChild(TABLE_DATA_FUNCTIONS[field](choreRow));
        }
        table.appendChild(rowElement);
    }
}

function queryServer() {
    request = new XMLHttpRequest();
    request.open("GET", QUERY_ADDRESS, true);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            CHORE_DATA = JSON.parse(request.responseText);
        }
    };
    request.send();
}

setInterval(queryServer, POLL_FREQUENCY_SECONDS*1000);
setInterval(buildTable, 1000);

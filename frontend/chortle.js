const POLL_FREQUENCY_SECONDS = 0.5;
const MAX_CHORE_DISPLAY_TIME = 3*60*60;

const TABLE_HEADERS = ["Chore", "Status", "Time Remaining"];
const TABLE_DATA_FIELDS = ["chore-name", "chore-status", "chore-time"];
const TABLE_DATA_FUNCTIONS = {
    "chore-name": function (choreRow) {
        var data = document.createElement("TD");
        data.innerText = choreRow.chore.S;
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
        if (!choreRow.active.BOOL || timeRemaining > MAX_CHORE_DISPLAY_TIME) return data;
        data.innerText = getStringFromTime(getTimeRemaining(choreRow));
        return data;
    }
}

function getTimeRemaining(choreRow) {
    var choreExpireTime = parseInt(choreRow.last_pressed_time.N) + parseInt(choreRow.reset_time_seconds.N);
    var now = Math.floor(new Date().getTime() / 1000);
    var timeRemaining = choreExpireTime - now;
    return timeRemaining;
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

var CHORE_DATA = [];
function pollDynamo(dynamodb) {
    dynamodb.scan({TableName: "chortle-model"}, function (err, data) {
        if (err) console.log(err, err.stack);
        else CHORE_DATA = data.Items;
    });
}

function setupAWSConfig() {
    AWS.config.update({
        region: 'us-east-2',
        credentials: new AWS.CognitoIdentityCredentials({
            IdentityPoolId: 'us-east-2:23c381d2-a8c3-4448-96f6-753b6cb4e374'
        })
    });
}

setupAWSConfig();
var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
setInterval(pollDynamo, POLL_FREQUENCY_SECONDS*1000, dynamodb);
setInterval(buildTable, 1000);

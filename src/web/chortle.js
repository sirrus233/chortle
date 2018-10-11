const POLL_FREQUENCY_SECONDS = 2;
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
        var status = choreRow.status_ok.BOOL;
        var active = choreRow.active.BOOL;
        if (status || !active) data.className = "status_good";
        else data.className = "status_bad";
        return data;
    },

    "chore-time": function (choreRow) {
        var data = document.createElement("TD");
        if (!choreRow.active.BOOL) return data;
        var choreExpireTime = parseInt(choreRow.last_pressed_time.N) + parseInt(choreRow.reset_time_seconds.N);
        var now = Math.floor(new Date().getTime() / 1000);
        var timeRemaining = choreExpireTime - now;
        data.innerText = getStringFromTime(timeRemaining);
        data.className = "timer";
        return data;
    }
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

function buildTable(choreList) {
    var table = document.getElementById("chore-chart");
    clearTable(table);
    buildTableHeader(table);
    for (var i = 0; i < choreList.length; i++) {
        var row = document.createElement("TR");
        for (var j = 0; j < TABLE_DATA_FIELDS.length; j++) {
            row.appendChild(TABLE_DATA_FUNCTIONS[TABLE_DATA_FIELDS[j]](choreList[i]));
        }
        table.appendChild(row);
    }
}

function getStringFromTime(timeValueSeconds) {
    var neg = timeValueSeconds < 0;
    if (neg) timeValueSeconds *= -1;
    var minutes = Math.floor(timeValueSeconds / 60);
    var seconds = Math.floor(timeValueSeconds % 60);
    var timeString = minutes + ":" + ("0"+seconds).slice(-2);
    if (neg) timeString = "-"+timeString;
    return timeString;
}

function getTimeFromString(timeString) {
    var neg = timeString.startsWith("-");
    if (neg) timeString = timeString.slice(1);
    var timeStringArray = timeString.split(":");
    var minutes = parseInt(timeStringArray[0]);
    var seconds = parseInt(timeStringArray[1]);
    var timeVal = 60*minutes + seconds;
    if (neg) timeVal *= -1;
    return timeVal;
}

function tickTimers() {
    var timers = document.getElementsByClassName("timer");
    for (var i = 0; i < timers.length; i++) {
        var timer = timers[i];
        timer.innerText = getStringFromTime(getTimeFromString(timer.innerText) - 1);
    }
}

function pollDynamo(dynamodb) {
    dynamodb.scan({TableName: "chortle-model"}, function (err, data) {
        if (err) console.log(err, err.stack);
        else buildTable(data.Items);
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
setInterval(tickTimers, 1000)

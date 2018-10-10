const POLL_FREQUENCY_SECONDS = 5;
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
        data.innerText = choreRow.status_ok.BOOL;
        return data;
    },

    "chore-time": function (choreRow) {
        var data = document.createElement("TD");
        var choreExpireTime = parseInt(choreRow.last_pressed_time.N) + parseInt(choreRow.reset_time_seconds.N);
        var now = Math.floor(new Date().getTime() / 1000);
        var timeRemaining = choreExpireTime - now;
        var neg = timeRemaining < 0;
        if (neg) timeRemaining *= -1;
        var minutes = Math.floor(timeRemaining / 60);
        var seconds = Math.floor(timeRemaining % 60);
        var choreTime = ("0"+minutes).slice(-2) + ":" + ("0"+seconds).slice(-2);
        if (neg) choreTime = "-"+choreTime;
        data.innerText = choreTime;
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
    TABLE_HEADERS.forEach(function(header) {
        var headerElement = document.createElement("TH");
        headerElement.innerText = header;
        headerRow.appendChild(headerElement);
    });
    table.appendChild(headerRow);
}

function buildTable(choreList) {
    var table = document.getElementById("chore-chart");
    clearTable(table);
    buildTableHeader(table);
    choreList.forEach(function(choreRow) {
        var row = document.createElement("TR");
        TABLE_DATA_FIELDS.forEach(function(field) {
            row.appendChild(TABLE_DATA_FUNCTIONS[field](choreRow));
        });
        table.appendChild(row);
    });
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

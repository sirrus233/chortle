function clearTable() {
    var table = document.getElementById("chore-chart");
    while (table.hasChildNodes()) {
        table.removeChild(table.firstChild)
    }
}

function buildTableHeader() {
    var choreHeader = document.createElement("TH");
    choreHeader.innerText = "Chore";

    var statusHeader = document.createElement("TH");
    statusHeader.innerText = "Status";

    var headerRow = document.createElement("TR");
    headerRow.appendChild(choreHeader)
    headerRow.appendChild(statusHeader)

    document.getElementById("chore-chart").appendChild(headerRow);
}

function buildTable(choreList) {
    clearTable();
    buildTableHeader();
    choreList.forEach(function(choreRow) {
        var choreName = choreRow.chore.S;
        var choreNameTd = document.createElement("TD");
        choreNameTd.innerText = choreName
    
        var choreStatus = choreRow.status_ok.BOOL;
        var choreStatusTd = document.createElement("TD");
        choreStatusTd.innerText = choreStatus

        var tr = document.createElement("TR");
        tr.appendChild(choreNameTd)
        tr.appendChild(choreStatusTd)
        document.getElementById("chore-chart").appendChild(tr);
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function pollDynamoLoop() {
    var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
    while (true) {
        dynamodb.scan({TableName: "chortle-model"}, function (err, data) {
            if (err) console.log(err, err.stack);
            else buildTable(data.Items);
        });
        await sleep(60*1000);
    }
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
pollDynamoLoop();

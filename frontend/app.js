const PORT = 5000

// Load and configure AWS
const aws = require('aws-sdk');
aws.config.update({
    region: 'us-west-2',
    credentials: new aws.SharedIniFileCredentials({profile: 'chortle'}),
})
const dynamoDB = new aws.DynamoDB({apiVersion: '2012-08-10'});

// Create basic Express app
const express = require('express')
const app = express()

// Configure behavior for GET endpoint(s)
app.get('/query', (req, res) => {
    dynamoDB.scan({TableName: "chortle"}, function (err, data) {
        if (err) console.log(err, err.stack);
        else res.send(data.Items);
    });
})

// Allow app to serve static pages
app.use(express.static('public'))

// Start app
app.listen(PORT, () => console.log(`Chortle is listening at http://localhost:${PORT}`))

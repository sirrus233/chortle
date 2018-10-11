import React from 'react';
import AWS from "https://sdk.amazonaws.com/js/aws-sdk-2.329.0.min.js";

// get data from AWS
var credentials = new AWS.Credentials(); // TODO Load credentials from AWS identity pool
var dynamodb = new AWS.DynamoDB({
	apiVersion: '2012-08-10', 
	region: 'us-east-2', 
	credentials: credentials});

dynamodb.scan({TableName: "chortle-model"}, function(err, data) {
	if (err) console.log(err, err.stack);
	else     console.log(data);
})

// create table using data
const Table = {data} = (
  <table>
    {data.map(row => {
      <TableRow row={row} />
    })}
  </table>
)

const TableRow = ({row}) => (
  <tr>
	<td key= "row.chore"> {row.Chore} </td>
	<td key="row.status"> {row.Status} </td>
	<td key="row.DueDate"> {row.DueDate}</td>
  </tr>
)

const ChoreTable = ({data}) => (
  <table>
    {data.map(row => {
      <TableRow row={row} />
    })}
  </table>
)



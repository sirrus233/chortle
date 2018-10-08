import React, { Component } from 'react';
import chortleLogo from './chortleLogo.gif';
import './App.css';
import ChoreTable from './tableCreation.js'
		
class App extends Component {
  render() {
    return (
	
      <div className="App">
        <header className="App-header">
		<img src={chortleLogo} alt="logo" />
          <a
            className="App-link"
            href="https://github.com/sirrus233/chortle"
          >
			<h1>Chortle</h1>
			<p>A Chore applet for the IoT</p>
          </a>
        </header>
		<body>
			<table>
				<th>
				<td><h3>Chores</h3></td>
				<td><h3>Status</h3></td>
				<td><h3>Due Date</h3></td>
				</th>
				<tbody>
				<tr>
				<td className="Chore"> Row for chores </td>
				<td className="Status"> Status </td>
				<td className="DueDate"> time </td>
				</tr>
				</tbody>
			</table>
			<div className="ChoreTable"/>
		</body>
      </div>
    );
  }
}

export default App;

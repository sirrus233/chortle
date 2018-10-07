import React, { Component } from 'react';
import chortleLogo from './chortleLogo.gif';
import './App.css';

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
			<table className="ChoreDisplay">
				<th>
				<td><h3>Chores</h3></td>
				<td><h3>Status</h3></td>
				<td><h3>Due Date </h3></td>
				</th>
				<tbody>
				<td className="Chore"> Row for chores </td>
				<td className="Status"> Status </td>
				<td className="DueDate"> time </td>
				</tbody>
			</table>
		</body>
      </div>
    );
  }
}

export default App;

// create table rows using data

const Table = ({data}) = (
  <table>
    {data.map(row => {
      <TableRow row={row} />
    })}
  </table>
)

const TableRow = ({row}) => (
  <tr>
	<td key=row.chore"> {row.Chore} </td>
	<td key=row.status"> {row.Status} </td>
	<td key=row.DueDate"> {row.DueDate}</td>
  </tr>
)

const Table = ({data}) => (
  <table>
    {data.map(row => {
      <TableRow row={row} />
    })}
  </table>
)



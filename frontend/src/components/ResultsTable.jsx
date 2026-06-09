function ResultsTable({ rows }) {

  if (!rows?.length) {
    return (
      <div className="
        bg-white
        p-6
        rounded-xl
      ">
        No records found
      </div>
    );
  }

  const columns =
    Object.keys(rows[0]);

  return (
    <div className="
      overflow-auto
      bg-white
      rounded-xl
      border
      border-sky-100
    ">

      <table className="w-full">

        <thead>

          <tr className="bg-sky-50">

            {columns.map((col) => (
              <th
                key={col}
                className="
                  px-4
                  py-3
                  text-left
                "
              >
                {col}
              </th>
            ))}

          </tr>

        </thead>

        <tbody>

          {rows.map((row, i) => (
            <tr
              key={i}
              className="
                border-t
                border-sky-100
              "
            >

              {columns.map((col) => (
                <td
                  key={col}
                  className="
                    px-4
                    py-3
                  "
                >
                  {String(row[col])}
                </td>
              ))}

            </tr>
          ))}

        </tbody>

      </table>

    </div>
  );
}

export default ResultsTable;
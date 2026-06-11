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
      bg-white
      rounded-xl
      border
      border-sky-100
      max-h-96
      overflow-auto
    ">

      <table className="
        w-full
        text-sm
      ">

        <thead className="sticky top-0 bg-sky-50">

          <tr>

            {columns.map((col) => (
              <th
                key={col}
                className="
                  px-4
                  py-3
                  text-left
                  font-semibold
                  whitespace-nowrap
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
                hover:bg-sky-50
              "
            >

              {columns.map((col) => (
                <td
                  key={col}
                  className="
                    px-4
                    py-3
                    whitespace-nowrap
                    overflow-hidden
                    text-ellipsis
                  "
                  title={String(row[col])}
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
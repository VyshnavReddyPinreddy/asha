function SqlCard({ sql }) {
  return (
    <div className="
      bg-white
      rounded-2xl
      shadow-sm
      p-6
      mb-6
      border
    ">
      <h2 className="
        font-semibold
        mb-4
      ">
        Generated SQL
      </h2>

      <pre
        className="
          bg-slate-900
          text-green-400
          p-4
          rounded-xl
          overflow-x-auto
          text-sm
        "
      >
        {sql}
      </pre>
    </div>
  );
}

export default SqlCard;
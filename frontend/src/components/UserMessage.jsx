function UserMessage({ query }) {
  return (
    <div className="flex justify-end mb-6">

      <div className="
        bg-sky-500
        text-white
        px-5
        py-3
        rounded-2xl
        max-w-xl
      ">
        {query}
      </div>

    </div>
  );
}

export default UserMessage;
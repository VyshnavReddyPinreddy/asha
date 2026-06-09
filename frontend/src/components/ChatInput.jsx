import {
  Plus,
  Mic,
  ArrowUp
} from "lucide-react";

import { useState } from "react";

function ChatInput({ onSubmit }) {

  const [query, setQuery] = useState("");

  const send = () => {

    if (!query.trim()) return;

    onSubmit(query);

    setQuery("");
  };

  return (
    <div className="
      border-t
      border-sky-100
      bg-white
      p-4
    ">

      <div className="
        max-w-4xl
        mx-auto
      ">

        <div className="
          rounded-3xl
          border
          border-sky-200
          px-5
          py-2.5
          flex
          items-center
          gap-4
          shadow-sm
        ">

          <Plus
            size={20}
            className="text-sky-500"
          />

          <input
            value={query}
            onChange={(e) =>
              setQuery(e.target.value)
            }
            onKeyDown={(e) =>
              e.key === "Enter" && send()
            }
            placeholder="Ask anything"
            className="
              flex-1
              outline-none
            "
          />

          <Mic
            size={20}
            className="text-sky-500"
          />

          <button
            onClick={send}
            className="
              h-9
              w-9
              rounded-full
              bg-sky-500
              text-white
              px-2
            "
          >
            <ArrowUp size={19} />
          </button>

        </div>

      </div>

    </div>
  );
}

export default ChatInput;
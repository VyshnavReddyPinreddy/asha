import { useState } from "react";
import { ChevronDown } from "lucide-react";

function ErrorResponse({ error }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const statusCode = error.statusCode || "Unknown";
  const message = error.message || "An error occurred";
  const details = error.details || "";

  return (
    <div className="mb-8">
      <div className="
        bg-red-50
        border
        border-red-200
        rounded-3xl
        p-6
      ">

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="
            w-full
            flex
            items-center
            justify-between
            text-left
            hover:opacity-75
            transition
          "
        >
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="
                text-sm
                font-semibold
                text-red-600
              ">
                Error ({statusCode})
              </span>
            </div>
            <p className="text-red-700 font-medium">
              {message}
            </p>
          </div>

          <ChevronDown
            size={20}
            className={`
              text-red-600
              transition-transform
              flex-shrink-0
              ml-4
              ${isExpanded ? 'rotate-180' : ''}
            `}
          />
        </button>

        {isExpanded && details && (
          <div className="
            mt-4
            pt-4
            border-t
            border-red-200
          ">
            <pre className="
              bg-white
              p-4
              rounded-xl
              text-sm
              text-red-700
              overflow-x-auto
              border
              border-red-100
            ">
              {details}
            </pre>
          </div>
        )}

      </div>
    </div>
  );
}

export default ErrorResponse;

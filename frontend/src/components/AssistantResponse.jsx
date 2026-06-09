import { Heart } from "lucide-react";
import ResultsTable from "./ResultsTable";

function AssistantResponse({ response }) {

  return (
    <div className="mb-8">

      <div className="
        bg-sky-50
        border
        border-sky-100
        rounded-3xl
        p-6
      ">

        <div className="
          flex
          justify-between
          mb-4
        ">
          <h3 className="font-semibold">
            Generated SQL
          </h3>

          <Heart
            className="
              text-sky-500
              cursor-pointer
            "
          />
        </div>

        <pre className="
          bg-white
          p-4
          rounded-xl
          overflow-x-auto
          text-sm
          border
          border-sky-100
        ">
          {response.generated_sql}
        </pre>

        <div className="mt-6">

          <h3 className="
            font-semibold
            mb-3
          ">
            Results
          </h3>

          <ResultsTable
            rows={response.results}
          />

        </div>

      </div>

    </div>
  );
}

export default AssistantResponse;
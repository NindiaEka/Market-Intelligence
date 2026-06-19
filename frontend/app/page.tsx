"use client";

import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Home() {

  const steps = [
    "Resolving company",
    "Searching sources",
    "Crawling website",
    "Extracting company facts",
    "Detecting capabilities",
    "Generating report"
  ];

  const [currentStep, setCurrentStep] = useState(0);
  const [companyName, setCompanyName] = useState("");
  const [history, setHistory] = useState<{company: string; report: string;}[]>([]);
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);
  useEffect(() => {

  const saved = localStorage.getItem(
    "report_history"
  );

  if (saved) {

    setHistory(
      JSON.parse(saved)
    );

  }

}, []);

  const handleAnalyze = async () => {

    let interval: NodeJS.Timeout;

    try {

      setLoading(true);
      setReport("");
      setCurrentStep(0);

      interval = setInterval(() => {

        setCurrentStep(prev => {

          if (prev < steps.length - 1) {
            return prev + 1;
          }

          return prev;

        });

      }, 5000);

      const response = await fetch(
        "http://localhost:8000/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            company_name: companyName,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Analyze failed");
      }

      const data = await response.json();

      clearInterval(interval);

      setCurrentStep(steps.length);

      setReport(data.report);
      const newHistory = [

        {
          company: companyName,
          report: data.report
        },

        ...history.filter(
          item =>
            item.company !== companyName
        )

      ];

      setHistory(
        newHistory.slice(0,10)
      );

      localStorage.setItem(
        "report_history",
        JSON.stringify(
          newHistory.slice(0,10)
        )
      );

    }

    catch (err) {

      console.error(err);

      clearInterval(interval!);

    }

    finally {

      setLoading(false);

    }

  };

  const downloadMarkdown = () => {

    const blob = new Blob(
      [report],
      {
        type: "text/markdown",
      }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = `${companyName}.md`;

    a.click();

    URL.revokeObjectURL(url);

  };

  return (

    <main className="min-h-screen bg-black text-white flex">
      <div className="
      w-72
      border-r
      border-zinc-800
      p-6
      ">

        <h2 className="
        text-xl
        font-bold
        mb-6
        ">
          Recent Reports
        </h2>

        <div className="
        flex
        flex-col
        gap-3
        ">

          {

            history.map(

              (item,index)=>(

                <button

                  key={index}

                  className="
                  text-left
                  bg-zinc-900
                  hover:bg-zinc-800
                  p-3
                  rounded-xl
                  "

                  onClick={() => {

                    setCompanyName(
                      item.company
                    );

                    setReport(
                      item.report
                    );

                  }}

                >

                  📄 {item.company}

                </button>

              )

            )

          }

        </div>

      </div>
      <div className="flex-1">

      <div className="max-w-5xl mx-auto pt-16">

        <h1 className="text-5xl font-bold text-center mb-10">
          Market Intelligence AI
        </h1>

        <div className="flex flex-col items-center gap-5">

          <input
            className="w-[500px] rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-4"
            placeholder="PT XL Axiata"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
          />

          <button
            className="bg-blue-600 hover:bg-blue-700 px-8 py-3 rounded-xl"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {
            loading && (

              <div className="mt-8 flex flex-col gap-3">

                {
                  steps.map((step, index) => (

                    <div
                      key={index}
                      className="flex items-center gap-3 text-zinc-300"
                    >

                      {
                        index < currentStep ? (

                          <span className="text-green-500">
                            ✓
                          </span>

                        ) : index === currentStep ? (

                          <span className="animate-pulse text-blue-400">
                            ⟳
                          </span>

                        ) : (

                          <span className="text-zinc-600">
                            ○
                          </span>

                        )
                      }

                      <span>
                        {step}
                      </span>

                    </div>

                  ))
                }

              </div>

            )
          }

        </div>

      </div>

      {
        report && (

          <div className="max-w-6xl mx-auto mt-20 mb-20">

            <div className="flex justify-between items-center mb-8">

              <h2 className="text-4xl font-bold">
                Company Report
              </h2>

              <button
                onClick={downloadMarkdown}
                className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-xl"
              >
                Download .md
              </button>

            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-12">

              <article
                className="
                prose
                prose-invert
                max-w-none

                prose-headings:text-white
                prose-h1:text-5xl
                prose-h1:mb-10

                prose-h2:text-3xl
                prose-h2:border-b
                prose-h2:border-zinc-700
                prose-h2:pb-3
                prose-h2:mt-12

                prose-h3:text-2xl
                prose-h3:text-blue-400

                prose-p:text-zinc-300
                prose-li:text-zinc-300
                prose-strong:text-white

                prose-table:w-full

                prose-th:border
                prose-th:border-zinc-700
                prose-th:bg-zinc-800
                prose-th:p-3

                prose-td:border
                prose-td:border-zinc-700
                prose-td:p-3
                "
              >

                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {report}
                </ReactMarkdown>

              </article>

            </div>

          </div>

        )
      }

      </div>

    </main>

  );

}
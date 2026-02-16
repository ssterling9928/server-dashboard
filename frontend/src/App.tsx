// App.tsx
import { ServiceGrid } from "./components/ServiceGrid";
import { Modal } from "./components/Modal"
import { useState } from "react";
import { Service } from "./types/services";
import { restartContainer } from "./apis/restartContainer";

function App() {
  const [selected, setSelected] = useState<Service | null>(null);

  return (

    <>
      <div className="min-h-screen bg-gray-900">
        <div className="">
          <ServiceGrid onSelect={setSelected}/>
        </div>
      </div>
      


      {/* Modal OUTSIDE grid */}
      <Modal isOpen={!!selected} onClose={() => setSelected(null)}>
        {selected && (
          console.log("Opened Modal for:", selected),
          <div className="space-y-6 text-gray-900">
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">{selected.name}</h2>

              {/* Status badges */}
              <div className="flex gap-4 text-sm">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium ${selected.service_status === "up"
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800"
                    }`}
                >
                  {selected.service_status}
                </span>
                {selected.url_status && (
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${selected.url_status === "up"
                      ? "bg-green-100 text-green-800"
                      : "bg-red-100 text-red-800"
                      }`}
                  >
                    {selected.url_status}
                  </span>
                )}
              </div>

              {/* Container */}
              {selected.container && (
                <div>
                  <h3 className="font-semibold mb-2">Container</h3>
                  <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-sm">
                    <p>
                      <strong>Name:</strong> {selected.container.name}
                    </p>
                    <p>
                      <strong>ID:</strong> {selected.container.id}
                    </p>
                    <p>
                      <strong>Status:</strong> {selected.container.status}
                    </p>
                  </div>
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-4 pt-4 border-t">
                {selected.url && (
                  <a
                    href={selected.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 bg-blue-500 text-white py-2 px-4 rounded-lg text-center hover:bg-blue-600"
                  >
                    Go to Live Service
                  </a>
                )}
                {selected.is_docker && selected.container && (
                  <button
                    onClick={() => {
                      const container = selected.container;
                      if (!container) return;
                      restartContainer(container.id);
                      setSelected(null);
                    }}
                    className="bg-yellow-500 text-white py-2 px-4 rounded-lg hover:bg-yellow-600"
                  >
                    Restart Container
                  </button>
                )}
              </div>
            </div>
          </div>
        
        )}
      </Modal>
    </>
  );
}

export default App;
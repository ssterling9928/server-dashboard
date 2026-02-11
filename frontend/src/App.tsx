// src/App.tsx
import { ServiceGrid } from './components/ServiceGrid';  // adjust path
import './App.css';  // or remove if empty

function App() {
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Server Dashboard
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Monitor and manage your services with real-time status updates.
          </p>
        </div>

        {/* Service Grid */}
        <ServiceGrid />
      </div>
    </div>
  );
}

export default App;

import { useState, useEffect } from 'react'
import './App.css'
import ServiceGrid from './components/ServiceGrid.jsx';
import ServiceDetail from './components/ServiceDetail.jsx';
import { getServices } from './api.js';



function mapApiService(apiService) {
  return {
    id: apiService.id,
    name: apiService.name,
    group: apiService.group,
    is_docker: apiService.is_docker,
    url: apiService.url || null,
    // interpret strings as booleans for the UI
    is_up: apiService.service_status === "ok",
    url_status: apiService.url_status, // keep raw too if you want
    container: apiService.container
      ? {
          name: apiService.container.name,
          id: apiService.container.id,
          status: apiService.container.status, // e.g. "up" | "down" | "unknown"
        }
      : null,
  };
}


function App() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedService, setSelectedService] = useState(null);

useEffect(() => {
    setLoading(true);
    getServices()
      .then(data => {
        const mappedServices = (data.services || data).map(mapApiService);
        setServices(mappedServices);
        setLoading(false);
      })
      .catch(error => {
        console.error('Failed to fetch services:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className='loading'>Loading services...</div>;
  } 

  return (
    <div className="App">
      <ServiceGrid 
        services={services}
        onSelectedService={setSelectedService}
      />
      {selectedService && ( 
        <ServiceDetail 
          service={selectedService}
          onClose={() => setSelectedService(null)}
        />  
      )}
    </div>
  );
}

export default App

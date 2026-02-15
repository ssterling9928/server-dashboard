import { useState } from "react"
import { Service } from "../types/services";
import '../css/ServiceGrid.css';
import { restartContainer } from "../apis/restartContainer";
import { useServices } from "../hooks/useServices";
import { Interface } from "node:readline";
import { on } from "node:cluster";

interface Props {
  onSelect: (service: Service) => void;  // ← receive from App
}

export function ServiceGrid({ onSelect }: Props) {
  const { services, loading, refetch } = useServices();

  if (loading) {
    return <div className="loading"> Loading...</div>;
  }

  if (!services || !Array.isArray(services)) {
    return <div className="error">No services found or API error</div>;
  }

  return (
      <div className="services-grid">
        {services.map((service) => (
          <div
            key={service.id}
            className="service-card"
            onClick={() => onSelect(service)}
          >
            <div className='row'>
              <div><h3>{service.name}</h3></div>
              <div className="status">{service.service_status ? '🟢 UP' : '🔴 DOWN'}</div>
            </div>
            <div className='row'>
              <div className="group"><strong>Group:</strong> {service.group}</div>
              {service.is_docker && <div className='docker'>Docker: 🐳</div>}
            </div>
          </div>
        ))}
      </div>
  );
}

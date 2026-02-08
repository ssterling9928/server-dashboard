import React from "react";
import "./ServiceDetail.css";



function ServiceDetail({ service }) {

  return (
    <div className="service-detail-overlay">
      <div className="service-detail-card">
        <button
          className="close-btn"
          onClick={() => {/* app handles unselect */ }}
        >
          x
        </button>
        <h2>{service.name}</h2>
        <div className="status">{service.is_up ? '🟢 UP' : '🔴 DOWN'}</div>

        {service.group && <p><strong>Group:</strong> {service.group}</p>}
        {service.is_docker && <p><strong>Docker:</strong> Yes</p>}
        {service.url && (
          <p>
            <strong>URL:</strong>
            <a href={service.url} target="_blank" rel="noopener noreferrer">
              {service.url}
            </a>
          </p>
        )}

        {service.container && (
          <div>
            <strong>Container:</strong>
            <ul>
              {service.containers.map((container, i) => (
                <li key={i}>
                  {container.name} ({container.status})
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ServiceDetail;

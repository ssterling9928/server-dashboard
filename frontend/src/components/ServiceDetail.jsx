import React from "react";
import "./ServiceDetail.css";



function ServiceDetail({ service }) {

  return (
    <div className="service-detail-overlay">
      <div className="detail-panel">
        <button
          className="btn"
          onClick={() => {/* app handles unselect */ }}
        >
          x
        </button>
        <h2 className="detail-header">{service.name}</h2>
        <div className="status">{service.is_up ? '🟢 UP' : '🔴 DOWN'}</div>
        <div className="details">
          <p><strong>Group:</strong> {service.group}</p>
        service.is_docker && <p><strong>Docker:</strong> Yes</p>
        service.url && (
          <p>
            <strong>URL:</strong>
            <a href={service.url} target="_blank" rel="noopener noreferrer">
              {service.url}
            </a>
          </p>
        )
        </div>
        

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

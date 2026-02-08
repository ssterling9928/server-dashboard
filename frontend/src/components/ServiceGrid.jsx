import React from 'react';
import './ServiceGrid.css';

function ServiceGrid({ services, onSelectService }) {

    return (
        <section className="service-grid">
            <h2>Services</h2>
            <div className="services-container">
                {services.map(service => (
                    <div
                        key={service.id}
                        className={`service-card ${service.is_up ? 'up' : 'down'}`}
                        onClick={() => onSelectService(service)}
                        style={{ cursor: 'pointer' }}
                    >
                        <div className="service-content">
                            <h3>{service.name}</h3>
                            <div className="status">{service.is_up ? '🟢 UP' : '🔴 DOWN'}</div>
                            {service.group && <div classname="group">{service.group}</div>}
                            {service.is_docker && <div className='docker'>🐳 Docker</div>}
                            {service.container?.status && <div className='container'>
                                Container: {service.container.status}
                            </div>}
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};
    
export default ServiceGrid;
import React from 'react';
import './ServiceGrid.css';

function ServiceGrid({ services, onSelectService }) {

    return (
        <section className="services-container">
            <h2>Services</h2>
            <div className="services-grid">
                {services.map(service => (
                    <div
                        key={service.id}
                        className={`service-card ${service.is_up ? 'up' : 'down'}`}
                        onClick={() => onSelectService(service)}
                        style={{ cursor: 'pointer' }}
                    >
                        <div className='row'>
                            <div><h3>{service.name}</h3></div>
                            <div className="status">{service.is_up ? '🟢 UP' : '🔴 DOWN'}</div>
                        </div>
                        
                        <div className='row'>
                            <div classname="group"><strong>Group:</strong> {service.group}</div>
                            {service.is_docker && <div className='docker'>Docker: 🐳</div>}
                        </div>

                    </div>
                ))}
            </div>
        </section>
    );
};

function onSelectService() {
    
    
}

export default ServiceGrid;
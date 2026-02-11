import { useState } from "react"
import { Service } from "../types/services";
import '../css/ServiceGrid.css';
import { restartContainer } from "../apis/restartContainer";
import { useServices } from "../hooks/useServices";

export function ServiceGrid() {
  const { services, loading, refetch } = useServices();
  const [selected, setSelected] = useState<Service | null>(null);

    return (
        <>
            {services.map((services) => (
                <div className="service-grid">
                    <div
                        key={services.id}
                        className="service-card"
                        onClick={() => setSelected(services)}
                    >
                        <div className='row'>
                            <div><h3>{services.name}</h3></div>
                            <div className="status">{services.service_status ? '🟢 UP' : '🔴 DOWN'}</div>
                        </div>
                        <div className='row'>
                            <div className="group"><strong>Group:</strong> {services.group}</div>
                            {services.is_docker && <div className='docker'>Docker: 🐳</div>}
                        </div>
                    </div>
                </div>
            ))}
        </>
    )
}
export default ServiceGrid;
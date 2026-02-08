
const API_BASE = '/api';

// Fetch services (backend endpoint)
export async function getServices() {
    const response = await fetch(`${API_BASE}/services`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}


// Restart a container (backend endpoint)
export async function restartContainer(container_id) {
    const response = await fetch(`${API_BASE}/services/${container_id}/restart`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json
}
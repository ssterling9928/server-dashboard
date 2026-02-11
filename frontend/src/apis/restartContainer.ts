
const API_BASE = '/api';

// Restart a container (backend endpoint)
export async function restartContainer(container_id: string) {
    const response = await fetch(`${API_BASE}/services/${container_id}/restart`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json
}
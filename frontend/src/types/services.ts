export interface DockerContainer {
    name: string;
    id: string;
    status: string;
}

export interface Service {
    id: string;
    name: string;
    group: string;
    is_docker: boolean;
    url?: string;
    url_status?: string;
    service_status: string;
    container?: DockerContainer;
}

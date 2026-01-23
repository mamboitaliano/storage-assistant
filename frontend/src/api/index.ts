import axios from 'axios';

const api = axios.create({
    baseURL: "/api",
});

export interface PaginatedResponse<T> {
    data: T[];
    total: number;
    page: number;
    pageSize: number;
}

export interface Item {
    id: number;
    name: string;
    room_id: number;
    container_id: number | null;
    quantity: number;
    created_at: string;
    room: Room;
    container: Container | null;
}

export interface Container {
    id: number;
    name: string | null;
    room_id: number | null;
    qr_code_path: string | null;
    item_count: number;
}

export interface ContainerOption {
    id: number;
    name: string | null;
}

export interface ContainerDetail extends Container {
    items: Item[];
}

export interface Room {
    id: number;
    name: string | null;
    floor_id: number | null;
    created_at: string;
    item_count: number;
    container_count: number;
}

export interface RoomOption {
    id: number;
    name: string | null;
}

export interface RoomDetail extends Room {
    containers: Container[];
    items: Item[];
}

export interface Floor {
    id: number;
    name: string | null;
    floor_number: number | null;
    created_at: string;
    room_count: number;
}

export interface FloorDetail extends Floor {
    rooms: Room[];
}

export interface SearchResult {
    items: Item[];
    containers: Container[];
    rooms: Room[];
    floors: Floor[];
}

export const containersApi = {
    list: async (page: number = 1) => {
        const { data } = await api.get<PaginatedResponse<Container>>(`/containers/?page=${page}`);
        return data;
    },
    get: async (id: number) => {
        const { data } = await api.get<ContainerDetail>(`/containers/${id}`);
        return data;
    },
    create: async (data: { name?: string; room_id?: string }) => {
        const response = await api.post<Container>('/containers/', data);
        return response.data;
    },
    delete: async (id: number) => {
        const { data } = await api.delete(`/containers/${id}`);
        return data;
    },
    addItem: async (containerId: number, data: { name: string; quantity?: number}) => {
        const response = await api.post<Item>(`/containers/${containerId}/items/`, data);
        return response.data;
    },
};

export const roomsApi = {
    list: async (page: number = 1) => {
        const { data } = await api.get<PaginatedResponse<Room>>(`/rooms/?page=${page}`);
        return data;
    },
    listContainers: async (roomId: number) => {
        const { data } = await api.get<ContainerOption[]>(`/rooms/${roomId}/containers`);
        return data;
    },
    get: async (id: number) => {
        const { data } = await api.get<Room>(`/rooms/${id}`);
        return data;
    },
    create: async (data: { name?: string; floor_id?: number }) => {
        const response = await api.post<Room>('/rooms/', data);
        return response.data;
    },
    addItem: async (roomId: number, data: { name?: string, quantity?: number }) => {
        const response = await api.post<Item>(`/rooms/${roomId}/items/`, data);
        return response.data;
    },
    delete: async (id: number) => {
        const { data } = await api.delete(`/rooms/${id}`);
        return data;
    },
};

export const floorsApi = {
    list: async (page: number = 1) => {
        const { data } = await api.get<PaginatedResponse<Floor>>(`/floors/?page=${page}`);
        return data;
    },
    listRooms: async (floorId: number) => {
        const { data } = await api.get<RoomOption[]>(`/floors/${floorId}/rooms`);
        return data;
    },
    get: async (id: number) => {
        const { data } = await api.get<FloorDetail>(`/floors/${id}`);
        return data;
    },
    create: async (data: { name?: string, floor_number?: number }) => {
        const response = await api.post<Floor>('/floors/', data);
        return response.data;
    },
    delete: async (id: number) => {
        const { data } = await api.delete(`/floors/${id}`);
        return data;
    },
};

export const itemsApi = {
    list: async (page: number = 1) => {
        const { data } = await api.get<PaginatedResponse<Item>>(`/items/?page=${page}`);
        return data;
    },
    create: async (data: { name: string, room_id: number, container_id?: number | null }) => {
        const response = await api.post<Item>(`/items/`, {
            name: data.name,
            room_id: data.room_id,
            container_id: data.container_id,
        });
        return response.data;
    },
    update: async (id: number, data: { name?: string, quantity?: number }) => {
        const response = await api.put<Item>(`/items/${id}/`, data);
        return response.data;
    },
    delete: async (id: number, quantity?: number) => {
        const { data } = await api.delete(`/items/${id}`, { params: quantity ? { quantity } : undefined });
        return data;
    },
};
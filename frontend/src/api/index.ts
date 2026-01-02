import axios from 'axios';

const api = axios.create({
    baseURL: "/",
});

export interface Item {
    id: number;
    name: string;
    room_id: number;
    container_id: number | null;
    quantity: number;
    created_at: string;
}

export interface Container {
    id: number;
    name: string | null;
    room_id: number | null;
    qr_code_path: string | null;
    item_count: number;
}

export interface ContainerDetail extends Container {
    items: Item[];
}

export interface Room {
    id: number;
    name: string | null;
    floor_id: number | null;
    created_at: string;
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
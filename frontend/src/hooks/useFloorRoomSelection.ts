/**
 * Custom reusable hook to remove repetition from ItemCreate and ContainerCreate components.
 * Contains functions for loading floors and, based on those, loading the rooms belonging to
 * a given floor when the floor selection changes.
 */

import { useState, useCallback, useEffect } from "react";
import { floorsApi, type Floor, type RoomOption } from "@/api";

interface UseFloorRoomSelectionOptions {
    onRoomSelected?: (roomId: number) => void;
}

export function useFloorRoomSelection(options: UseFloorRoomSelectionOptions = {}) {
    const [showFloorsDropdown, setShowFloorsDropdown] = useState(false);
    const [showRoomsDropdown, setShowRoomsDropdown] = useState(false);
    const [floors, setFloors] = useState<Floor[] | null>(null);
    const [rooms, setRooms] = useState<RoomOption[] | null>(null);
    const [selectedRoomId, setSelectedRoomId] = useState<number | null>(null);
    const [error, setError] = useState<Error | null>(null);

    const loadRooms = useCallback(async (floorId: number) => {
        try {
            const data = await floorsApi.listRooms(floorId);
            setRooms(data || []);

            if (data && data.length > 1) {
                setSelectedRoomId(null);
                setShowRoomsDropdown(true);
            } else if (data && data.length === 1) {
                setSelectedRoomId(data[0].id);
                options.onRoomSelected?.(data[0].id);
            }
        } catch (e) {
            setError(e as Error);
        }
    }, [options.onRoomSelected]);

    const loadFloors = useCallback(async () => {
        try {
            const { data } = await floorsApi.list();
            setFloors(data || []);
            setSelectedRoomId(null);

            if (data && data.length > 1) {
                setShowFloorsDropdown(true);
            } else if (data && data.length === 1) {
                loadRooms(data[0].id);
            }
        } catch (e) {
            setError(e as Error);
        }
    }, [loadRooms]);

    const handleFloorChange = useCallback((value: string) => {
        setSelectedRoomId(null);
        setShowRoomsDropdown(false);
        setRooms(null);
        loadRooms(parseInt(value));
    }, [loadRooms]);

    const handleRoomChange = useCallback((value: string) => {
        const roomId = parseInt(value);
        setSelectedRoomId(roomId);
        options.onRoomSelected?.(roomId);
    }, [options.onRoomSelected]);

    const reset = useCallback(() => {
        setSelectedRoomId(null);
        setShowFloorsDropdown(false);
        setShowRoomsDropdown(false);
        setFloors(null);
        setRooms(null);
    }, []);

    useEffect(() => {
        loadFloors();
    }, [loadFloors]);

    return {
        floors,
        rooms,
        selectedRoomId,
        showFloorsDropdown,
        showRoomsDropdown,
        error,
        handleFloorChange,
        handleRoomChange,
        reset,
    };
}
import { useCallback } from "react";
import { useLoadableOptions } from "./useLoadableOptions";
import { roomsApi } from "@/api";
import type { SelectOption } from "@/components/AsyncMultiSelect";

/**
 * Hook that encapsulates all room filter logic for reuse across filter components.
 * Handles loading all rooms, search functions, and computed state flags.
 */
export function useRoomFilter() {
    // Fetch function for loading all rooms
    const fetchAllRooms = useCallback(async () => {
        return await roomsApi.listAll(200);
    }, []);

    const {
        options: allRooms,
        loading: loadingAllRooms,
        error: loadRoomsError,
        isLoaded: roomsLoaded,
        total: totalRooms,
        hasMore: hasMoreRooms,
        loadAll: handleLoadAllRooms,
    } = useLoadableOptions(fetchAllRooms);

    // Search function for async room search
    const searchRooms = useCallback(async (query: string): Promise<SelectOption[]> => {
        const results = await roomsApi.search(query);
        return results.map(r => ({ id: r.id, name: r.name }));
    }, []);

    // Local search function filters pre-loaded rooms by query
    const searchLocalRooms = useCallback(async (query: string): Promise<SelectOption[]> => {
        const lowerQuery = query.toLowerCase();
        return allRooms.filter(r => 
            r.name?.toLowerCase().includes(lowerQuery)
        );
    }, [allRooms]);

    // Hybrid search: show pre-loaded items when empty, use API search when typing
    const searchRoomsHybrid = useCallback(async (query: string): Promise<SelectOption[]> => {
        if (!query.trim()) {
            // No query - return pre-loaded items
            return allRooms;
        }
        // Has query - use API to search beyond pre-loaded items
        const results = await roomsApi.search(query);
        return results.map(r => ({ id: r.id, name: r.name }));
    }, [allRooms]);

    // Determine which search mode to use
    const useLocalRoomSearch = roomsLoaded && !hasMoreRooms;
    const useHybridRoomSearch = roomsLoaded && hasMoreRooms;

    // Convenience: get the appropriate search function based on state
    const roomSearchFn = useLocalRoomSearch 
        ? searchLocalRooms 
        : useHybridRoomSearch 
            ? searchRoomsHybrid 
            : searchRooms;

    // Convenience: get appropriate debounce (0 for local, 300 for async)
    const roomDebounceMs = useLocalRoomSearch ? 0 : 300;

    // Convenience: get appropriate min search length (0 for loaded, 1 for async)
    const roomMinSearchLength = roomsLoaded ? 0 : 1;

    // Convenience: get appropriate placeholder
    const roomPlaceholder = roomsLoaded ? "Select rooms..." : "Search rooms...";

    return {
        // State from useLoadableOptions
        allRooms,
        loadingAllRooms,
        loadRoomsError,
        roomsLoaded,
        totalRooms,
        hasMoreRooms,
        handleLoadAllRooms,

        // Individual search functions (if needed)
        searchRooms,
        searchLocalRooms,
        searchRoomsHybrid,

        // Computed flags
        useLocalRoomSearch,
        useHybridRoomSearch,

        // Convenience values for AsyncMultiSelect props
        roomSearchFn,
        roomDebounceMs,
        roomMinSearchLength,
        roomPlaceholder,
    };
}

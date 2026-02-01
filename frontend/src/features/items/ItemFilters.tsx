import { useCallback, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AsyncMultiSelect, { type SelectOption } from "@/components/AsyncMultiSelect";
import { useLoadableOptions } from "@/hooks/useLoadableOptions";
import { filtersAreEqual } from "@/utils/filters";
import { roomsApi, containersApi, type ItemFilters as ItemFiltersType } from "@/api";

interface ItemFiltersProps {
    filters: ItemFiltersType;
    appliedFilters: ItemFiltersType | undefined;
    onFiltersChange: (filters: ItemFiltersType) => void;
    onApply: () => void;
    onClear: () => void;
}

export default function ItemFilters({ 
    filters, 
    appliedFilters,
    onFiltersChange, 
    onApply, 
    onClear,
}: ItemFiltersProps) {
    // Track previous rooms to detect changes
    const prevRoomsRef = useRef<number[] | undefined>(filters.rooms);

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

    // Fetch function for loading all containers (scoped to selected rooms)
    const fetchAllContainers = useCallback(async () => {
        return await containersApi.listAll(200, filters.rooms);
    }, [filters.rooms]);

    const {
        options: allContainers,
        loading: loadingAllContainers,
        error: loadContainersError,
        isLoaded: containersLoaded,
        total: totalContainers,
        hasMore: hasMoreContainers,
        loadAll: handleLoadAllContainers,
    } = useLoadableOptions(fetchAllContainers);

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onFiltersChange({ ...filters, name: e.target.value });
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            onApply();
        }
    };

    const handleRoomsChange = (roomIds: number[]) => {
        // When rooms change, reset container selection
        onFiltersChange({ ...filters, rooms: roomIds, containers: [] });
    };

    const handleContainersChange = (containerIds: number[]) => {
        onFiltersChange({ ...filters, containers: containerIds });
    };

    // Reset containers when rooms change (after initial render)
    useEffect(() => {
        const prevRooms = prevRoomsRef.current;
        const currentRooms = filters.rooms;
        
        // Check if rooms actually changed (not just on mount)
        const roomsChanged = JSON.stringify(prevRooms) !== JSON.stringify(currentRooms);
        
        if (roomsChanged && prevRooms !== undefined) {
            // Rooms changed - container selection is already cleared in handleRoomsChange
        }
        
        prevRoomsRef.current = currentRooms;
    }, [filters.rooms]);

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

    // Search function for async container search (scoped to selected rooms)
    const searchContainers = useCallback(async (query: string): Promise<SelectOption[]> => {
        const results = await containersApi.search(query, filters.rooms);
        return results.map(c => ({ id: c.id, name: c.name }));
    }, [filters.rooms]);

    // Helper to filter containers by selected rooms
    const filterContainersByRooms = useCallback((containers: typeof allContainers) => {
        if (!filters.rooms || filters.rooms.length === 0) {
            return containers;
        }
        return containers.filter(c => c.room_id && filters.rooms!.includes(c.room_id));
    }, [filters.rooms]);

    // Local search function filters pre-loaded containers by query and selected rooms
    const searchLocalContainers = useCallback(async (query: string): Promise<SelectOption[]> => {
        const lowerQuery = query.toLowerCase();
        const roomFiltered = filterContainersByRooms(allContainers);
        return roomFiltered.filter(c => 
            c.name?.toLowerCase().includes(lowerQuery)
        );
    }, [allContainers, filterContainersByRooms]);

    // Hybrid search: show pre-loaded items when empty, use API search when typing
    const searchContainersHybrid = useCallback(async (query: string): Promise<SelectOption[]> => {
        if (!query.trim()) {
            // No query - return pre-loaded items filtered by selected rooms
            return filterContainersByRooms(allContainers);
        }
        // Has query - use API to search beyond pre-loaded items
        const results = await containersApi.search(query, filters.rooms);
        return results.map(c => ({ id: c.id, name: c.name }));
    }, [allContainers, filters.rooms, filterContainersByRooms]);

    // Determine which search function to use:
    // - Not loaded: async search (requires typing)
    // - Loaded with no more: local search (fast filtering)
    // - Loaded with more: hybrid (show pre-loaded, search API when typing)
    const useLocalRoomSearch = roomsLoaded && !hasMoreRooms;
    const useHybridRoomSearch = roomsLoaded && hasMoreRooms;
    const useLocalContainerSearch = containersLoaded && !hasMoreContainers;
    const useHybridContainerSearch = containersLoaded && hasMoreContainers;

    // Check if pending filters differ from applied filters
    const filtersHaveChanged = !filtersAreEqual(filters, appliedFilters);
    
    // Check if there are any applied filters (for Clear button)
    const hasAppliedFilters = Boolean(
        appliedFilters?.name || 
        (appliedFilters?.rooms && appliedFilters.rooms.length > 0) ||
        (appliedFilters?.containers && appliedFilters.containers.length > 0)
    );
    
    // Check if there are any pending filters (for Clear button when nothing applied yet)
    const hasPendingFilters = Boolean(
        filters.name || 
        (filters.rooms && filters.rooms.length > 0) ||
        (filters.containers && filters.containers.length > 0)
    );

    return (
        <div className="flex items-start gap-4 py-4 flex-wrap">
            {/* Name filter */}
            <div className="flex flex-col gap-1.5">
                <Label htmlFor="name-filter" className="text-sm text-muted-foreground">
                    Name
                </Label>
                <Input
                    id="name-filter"
                    type="text"
                    placeholder="Search by name..."
                    value={filters.name || ''}
                    onChange={handleNameChange}
                    onKeyDown={handleKeyDown}
                    className="w-64"
                />
            </div>

            {/* Room filter */}
            <div className="flex flex-col gap-1.5">
                <div className="flex items-center gap-2">
                    <Label className="text-sm text-muted-foreground">Room</Label>
                    {!roomsLoaded && (
                        loadingAllRooms ? (
                            <span className="text-xs text-muted-foreground">Loading...</span>
                        ) : loadRoomsError ? (
                            <span className="text-xs text-red-500">
                                Failed to load rooms.{" "}
                                <button
                                    type="button"
                                    onClick={handleLoadAllRooms}
                                    className="underline hover:text-red-400"
                                >
                                    Retry
                                </button>
                            </span>
                        ) : (
                            <button
                                type="button"
                                onClick={handleLoadAllRooms}
                                className="text-xs text-muted-foreground hover:text-foreground underline"
                            >
                                Show all
                            </button>
                        )
                    )}
                    {roomsLoaded && hasMoreRooms && (
                        <span className="text-xs text-amber-600">
                            Showing {allRooms.length} of {totalRooms}. Use search for more.
                        </span>
                    )}
                </div>
                <AsyncMultiSelect
                    searchFn={
                        useLocalRoomSearch ? searchLocalRooms : 
                        useHybridRoomSearch ? searchRoomsHybrid : 
                        searchRooms
                    }
                    value={filters.rooms || []}
                    onChange={handleRoomsChange}
                    placeholder={roomsLoaded ? "Select rooms..." : "Search rooms..."}
                    disabled={loadingAllRooms}
                    debounceMs={useLocalRoomSearch ? 0 : 300}
                    minSearchLength={roomsLoaded ? 0 : 1}
                />
            </div>

            {/* Container filter */}
            <div className="flex flex-col gap-1.5">
                <div className="flex items-center gap-2">
                    <Label className="text-sm text-muted-foreground">Container</Label>
                    {!containersLoaded && (
                        loadingAllContainers ? (
                            <span className="text-xs text-muted-foreground">Loading...</span>
                        ) : loadContainersError ? (
                            <span className="text-xs text-red-500">
                                Failed to load containers.{" "}
                                <button
                                    type="button"
                                    onClick={handleLoadAllContainers}
                                    className="underline hover:text-red-400"
                                >
                                    Retry
                                </button>
                            </span>
                        ) : (
                            <button
                                type="button"
                                onClick={handleLoadAllContainers}
                                className="text-xs text-muted-foreground hover:text-foreground underline"
                            >
                                Show all
                            </button>
                        )
                    )}
                    {containersLoaded && hasMoreContainers && (
                        <span className="text-xs text-amber-600">
                            Showing {allContainers.length} of {totalContainers}. Use search for more.
                        </span>
                    )}
                </div>
                <AsyncMultiSelect
                    searchFn={
                        useLocalContainerSearch ? searchLocalContainers : 
                        useHybridContainerSearch ? searchContainersHybrid : 
                        searchContainers
                    }
                    value={filters.containers || []}
                    onChange={handleContainersChange}
                    placeholder={containersLoaded ? "Select containers..." : "Search containers..."}
                    disabled={loadingAllContainers}
                    debounceMs={useLocalContainerSearch ? 0 : 300}
                    minSearchLength={containersLoaded ? 0 : 1}
                />
            </div>

            {/* Apply/Clear buttons - ml-auto keeps them right-aligned */}
            <div className="flex flex-col gap-1.5 ml-auto">
                <div className="text-sm invisible">spacer</div>
                <div className="flex gap-2">
                    <Button 
                        onClick={onApply} 
                        disabled={!filtersHaveChanged}
                        size="sm"
                    >
                        Apply
                    </Button>
                    <Button 
                        onClick={onClear} 
                        variant="outline" 
                        disabled={!hasAppliedFilters && !hasPendingFilters}
                        size="sm"
                    >
                        Clear
                    </Button>
                </div>
            </div>
        </div>
    );
}

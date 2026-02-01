import { useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AsyncMultiSelect, { type SelectOption } from "@/components/AsyncMultiSelect";
import { useLoadableOptions } from "@/hooks/useLoadableOptions";
import { filtersAreEqual } from "@/utils/filters";
import { roomsApi, type ItemFilters as ItemFiltersType } from "@/api";

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
    // Fetch function for loading all rooms
    const fetchAllRooms = useCallback(async () => {
        const response = await roomsApi.list(1);
        return response.data.map(r => ({ id: r.id, name: r.name }));
    }, []);

    const {
        options: allRooms,
        loading: loadingAllRooms,
        error: loadRoomsError,
        isLoaded: roomsLoaded,
        loadAll: handleLoadAllRooms,
    } = useLoadableOptions(fetchAllRooms);

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onFiltersChange({ ...filters, name: e.target.value });
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            onApply();
        }
    };

    const handleRoomsChange = (roomIds: number[]) => {
        onFiltersChange({ ...filters, rooms: roomIds });
    };

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
        <div className="flex items-end gap-4 py-4 flex-wrap">
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
                </div>
                <AsyncMultiSelect
                    searchFn={roomsLoaded ? searchLocalRooms : searchRooms}
                    value={filters.rooms || []}
                    onChange={handleRoomsChange}
                    placeholder={roomsLoaded ? "Select rooms..." : "Search rooms..."}
                    disabled={loadingAllRooms}
                    debounceMs={roomsLoaded ? 0 : 300}
                    minSearchLength={roomsLoaded ? 0 : 1}
                />
            </div>

            {/* Apply/Clear buttons */}
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
    );
}

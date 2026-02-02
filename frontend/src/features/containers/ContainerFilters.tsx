import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AsyncMultiSelect from "@/components/AsyncMultiSelect";
import FilterButtons from "@/components/FilterButtons";
import { useRoomFilter } from "@/hooks/useRoomFilter";
import { containerFiltersAreEqual } from "@/utils/filters";
import { type ContainerFilters as ContainerFiltersType } from "@/api";

interface ContainerFiltersProps {
    filters: ContainerFiltersType;
    appliedFilters: ContainerFiltersType | undefined;
    onFiltersChange: (filters: ContainerFiltersType) => void;
    onApply: () => void;
    onClear: () => void;
}

export default function ContainerFilters({ 
    filters, 
    appliedFilters,
    onFiltersChange, 
    onApply, 
    onClear,
}: ContainerFiltersProps) {
    // Room filter logic from shared hook
    const {
        allRooms,
        loadingAllRooms,
        loadRoomsError,
        roomsLoaded,
        totalRooms,
        hasMoreRooms,
        handleLoadAllRooms,
        roomSearchFn,
        roomDebounceMs,
        roomMinSearchLength,
        roomPlaceholder,
    } = useRoomFilter();

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

    // Check if pending filters differ from applied filters
    const filtersHaveChanged = !containerFiltersAreEqual(filters, appliedFilters);
    
    // Check if there are any applied filters (for Clear button)
    const hasAppliedFilters = Boolean(
        appliedFilters?.name || 
        (appliedFilters?.rooms && appliedFilters.rooms.length > 0)
    );
    
    // Check if there are any pending filters (for Clear button when nothing applied yet)
    const hasPendingFilters = Boolean(
        filters.name || 
        (filters.rooms && filters.rooms.length > 0)
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
                    searchFn={roomSearchFn}
                    value={filters.rooms || []}
                    onChange={handleRoomsChange}
                    placeholder={roomPlaceholder}
                    disabled={loadingAllRooms}
                    debounceMs={roomDebounceMs}
                    minSearchLength={roomMinSearchLength}
                />
            </div>

            <FilterButtons
                onApply={onApply}
                onClear={onClear}
                applyDisabled={!filtersHaveChanged}
                clearDisabled={!hasAppliedFilters && !hasPendingFilters}
            />
        </div>
    );
}

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { ItemFilters as ItemFiltersType } from "@/api";

interface ItemFiltersProps {
    filters: ItemFiltersType;
    onFiltersChange: (filters: ItemFiltersType) => void;
    onApply: () => void;
    onClear: () => void;
    hasAppliedFilters: boolean;
}

export default function ItemFilters({ 
    filters, 
    onFiltersChange, 
    onApply, 
    onClear,
    hasAppliedFilters 
}: ItemFiltersProps) {
    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onFiltersChange({ ...filters, name: e.target.value });
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            onApply();
        }
    };

    const hasFilters = Boolean(filters.name);

    return (
        <div className="flex items-end gap-4 py-4">
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

            <div className="flex gap-2">
                <Button 
                    onClick={onApply} 
                    disabled={!hasFilters}
                    size="sm"
                >
                    Apply
                </Button>
                <Button 
                    onClick={onClear} 
                    variant="outline" 
                    disabled={!hasAppliedFilters && !hasFilters}
                    size="sm"
                >
                    Clear
                </Button>
            </div>
        </div>
    );
}

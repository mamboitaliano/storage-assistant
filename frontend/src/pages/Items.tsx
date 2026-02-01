import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePaginatedApi } from "../hooks/usePaginatedApi";
import { itemsApi, type Item, type ItemFilters as ItemFiltersType } from "../api";
import Paginator from "@/components/Paginator";
import PageHeader from "@/components/PageHeader";
import ItemsTable from "@/features/items/ItemsTable";
import ItemFilters from "@/features/items/ItemFilters";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "lucide-react";

export default function Items() {
    const navigate = useNavigate();
    const [pendingFilters, setPendingFilters] = useState<ItemFiltersType>({});
    
    const { 
        data, 
        loading, 
        error, 
        page, 
        setPage, 
        totalPages, 
        hasMultiplePages,
        appliedFilters,
        applyFilters,
        clearFilters,
    } = usePaginatedApi<Item, ItemFiltersType>(itemsApi.list);

    const handleApplyFilters = () => {
        applyFilters(pendingFilters);
    };

    const handleClearFilters = () => {
        setPendingFilters({});
        clearFilters();
    };

    const hasAppliedFilters = Boolean(
        appliedFilters?.name || 
        (appliedFilters?.rooms && appliedFilters.rooms.length > 0) ||
        (appliedFilters?.containers && appliedFilters.containers.length > 0)
    );

    const newItemBtn = () => {
        return (
            <Button size="sm" onClick={() => {
                navigate("/items/create");
            }}><PlusIcon /> Add Item</Button>
        )
    }

    return (
        <div className="flex flex-col h-full">
            <PageHeader title="Items" action={newItemBtn()} />
            <ItemFilters 
                filters={pendingFilters}
                onFiltersChange={setPendingFilters}
                onApply={handleApplyFilters}
                onClear={handleClearFilters}
                hasAppliedFilters={hasAppliedFilters}
            />
            {loading ? (
                <div className="flex-1 flex items-center justify-center">Loading...</div>
            ) : error ? (
                <div className="flex-1 flex items-center justify-center text-red-500">Error: {error.message}</div>
            ) : (
                <>
                    <div className="flex-1 min-h-0 overflow-auto">
                        <ItemsTable data={data} />
                    </div>
                    {hasMultiplePages && (
                        <div className="flex-shrink-0 py-4">
                            <Paginator page={page} totalPages={totalPages} onPageChange={setPage} />
                        </div>
                    )}
                </>
            )}
        </div>
    )
}
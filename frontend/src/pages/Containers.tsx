import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePaginatedApi } from "@/hooks/usePaginatedApi";
import { containersApi, type Container, type ContainerFilters as ContainerFiltersType } from "@/api";
import Paginator from "@/components/Paginator";
import PageHeader from "@/components/PageHeader";
import ContainersTable from "@/features/containers/ContainersTable";
import ContainerFilters from "@/features/containers/ContainerFilters";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "lucide-react";

export default function Containers() {
    const navigate = useNavigate();
    const [pendingFilters, setPendingFilters] = useState<ContainerFiltersType>({});

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
    } = usePaginatedApi<Container, ContainerFiltersType>(containersApi.list);

    const handleApplyFilters = () => {
        applyFilters(pendingFilters);
    };

    const handleClearFilters = () => {
        setPendingFilters({});
        clearFilters();
    };

    return (
        <div className="flex flex-col h-full">
            <PageHeader
                title="Containers"
                action={
                    <Button size="sm" onClick={() => navigate("/containers/create")}>
                        <PlusIcon /> Add Container
                    </Button>
                }
            />
            <ContainerFilters 
                filters={pendingFilters}
                appliedFilters={appliedFilters}
                onFiltersChange={setPendingFilters}
                onApply={handleApplyFilters}
                onClear={handleClearFilters}
            />
            {loading ? (
                <div className="flex-1 flex items-center justify-center">Loading...</div>
            ) : error ? (
                <div className="flex-1 flex items-center justify-center text-red-500">Error: {error.message}</div>
            ) : (
                <>
                    <div className="flex-1 min-h-0 overflow-auto">
                        <ContainersTable data={data} />
                    </div>
                    {hasMultiplePages && (
                        <div className="flex-shrink-0 py-4">
                            <Paginator page={page} totalPages={totalPages} onPageChange={setPage} />
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
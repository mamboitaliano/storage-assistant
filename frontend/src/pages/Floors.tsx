import { useNavigate } from "react-router-dom";
import { usePaginatedApi } from "../hooks/usePaginatedApi";
import { floorsApi } from "../api";
import Paginator from "@/components/Paginator";
import PageHeader from "@/components/PageHeader";
import FloorsTable from "@/features/floors/FloorsTable";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "lucide-react";

export default function Floors() {
    const navigate = useNavigate();
    const { 
        data, 
        loading, 
        error, 
        page, 
        setPage, 
        totalPages, 
        hasMultiplePages 
      } = usePaginatedApi(floorsApi.list);

    if (loading) {
        return <div>Loading...</div>;
    }
    
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    if (!data) {
        return <div>No data</div>;
    }

    return (
        <div className="flex flex-col h-full">
            <PageHeader 
                title="Floors" 
                action={
                    <Button size="sm" onClick={() => navigate("/floors/create")}>
                        <PlusIcon /> Add Floor
                    </Button>
                } 
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto">
                <FloorsTable data={data} />
            </div>
            {hasMultiplePages && (
                <div className="flex-shrink-0 py-4">
                    <Paginator page={page} totalPages={totalPages} onPageChange={setPage} />
                </div>
            )}
        </div>
    )
};

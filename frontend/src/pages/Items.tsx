import { useNavigate } from "react-router-dom";
import { usePaginatedApi } from "../hooks/usePaginatedApi";
import { itemsApi } from "../api";
import Paginator from "@/components/Paginator";
import PageHeader from "@/components/PageHeader";
import ItemsTable from "@/features/items/ItemsTable";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "lucide-react";

export default function Items() {
    const navigate = useNavigate();
    const { 
        data, 
        loading, 
        error, 
        page, 
        setPage, 
        totalPages, 
        hasMultiplePages 
      } = usePaginatedApi(itemsApi.list);

    if (loading) {
        return <div>Loading...</div>;
    }
    
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    if (!data) {
        return <div>No data</div>;
    }

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
            <div className="flex-1 min-h-0 mt-6 overflow-auto">
                <ItemsTable data={data} />
            </div>
            {hasMultiplePages && (
                <div className="flex-shrink-0 py-4">
                    <Paginator page={page} totalPages={totalPages} onPageChange={setPage} />
                </div>
            )}
        </div>
    )
};
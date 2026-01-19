import { usePaginatedApi } from "../hooks/usePaginatedApi";
import { itemsApi } from "../api";
import Paginator from "@/components/Paginator";
import PageHeader from "../components/PageHeader";
import ItemsTable from "@/features/items/ItemsTable";

export default function Items() {
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

    return (
        <div className="flex flex-col h-full">
            <PageHeader title="Items" />
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
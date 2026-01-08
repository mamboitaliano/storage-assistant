import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { itemsApi } from "../api";
import ItemsTable from "@/features/items/ItemsTable";

export default function Items() {
    const { data, loading, error } = useApi(itemsApi.list);

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
        <div className="space-y-6">
            <PageHeader title="Items" />
            <ItemsTable data={data} />
        </div>
    )
};
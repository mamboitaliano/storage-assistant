import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { floorsApi } from "../api";
import { FloorsTable } from "../features/floors/FloorsTable";

export default function Floors() {
    const { data, loading, error } = useApi(floorsApi.list);

    if (loading) {
        return <div className="text-sm text-muted-foreground">Loading floors...</div>;
    }
    
    if (error) {
        return <div className="text-sm text-red-400">Error: {error.message}</div>;
    }

    if (!data) {
        return <div className="text-sm text-muted-foreground">No floors found.</div>;
    }

    return (
        <div className="space-y-6">
            <PageHeader title="Floors" />
            <FloorsTable data={data} />
        </div>
    )
};

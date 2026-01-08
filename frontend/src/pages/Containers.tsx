import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { containersApi } from "../api";
import ContainersTable from "@/features/containers/ContainersTable";

export default function Containers() {
    const { data, loading, error } = useApi(containersApi.list);

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
            <PageHeader title="Containers" />
            <ContainersTable data={data} />
        </div>
    )
};
import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { containersApi } from "../api";

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
        <>
            <PageHeader title="Containers" />
            <div className="flex flex-col gap-4">
                {data.map(container => (
                    <div key={container.id}>{container.name}</div>
                ))}
            </div>
        </>
    )
};
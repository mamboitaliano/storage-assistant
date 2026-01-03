import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { floorsApi } from "../api";

export default function Floors() {
    const { data, loading, error } = useApi(floorsApi.list);

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
            <PageHeader title="Floors" />
            <div className="flex flex-col gap-4">
                {data.map(floor => (
                    <div key={floor.id}>{floor.name}</div>
                ))}
            </div>
        </>
    )
};
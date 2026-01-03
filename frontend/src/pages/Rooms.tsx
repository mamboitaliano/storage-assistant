import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { roomsApi } from "../api";

export default function Rooms() {
    const { data, loading, error } = useApi(roomsApi.list);

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
            <PageHeader title="Rooms" />
            <div className="flex flex-col gap-4">
                {data.map(room => (
                    <div key={room.id}>{room.name}</div>
                ))}
            </div>
        </>
    )
};
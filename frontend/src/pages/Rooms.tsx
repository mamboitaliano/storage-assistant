import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { roomsApi } from "../api";
import RoomsTable from "../features/rooms/RoomsTable";

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
        <div className="space-y-6">
            <PageHeader title="Rooms" />
            <RoomsTable data={data} />
        </div>
    )
};
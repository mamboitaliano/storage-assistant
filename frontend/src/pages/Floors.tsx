import PageHeader from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import { floorsApi } from "../api";
import { useNavigate } from "react-router-dom";

export default function Floors() {
    const { data, loading, error } = useApi(floorsApi.list);
    const navigate = useNavigate();

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
            <div className="flex flex-row">
                <div className="flex flex-col gap-2 w-4/4">
                    {data.map(floor => (
                        <div key={floor.id} className="flex flex-row">
                            <div className="flex flex-col gap-2 p-4 rounded-md border border-gunmetal-600 w-4/4">
                                <div className="flex flex-row gap-2 justify-between">
                                    <div className="flex flex-col gap-2">
                                        <div className="text-md font-bold">Floor {floor.floor_number}: {floor.name}</div>
                                    </div>
                                    <div className="flex flex-col gap-2">
                                        <button 
                                            className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 text-sm"
                                            onClick={(() => navigate(`/floors/${floor.id}`))}
                                        >
                                            View Details
                                        </button>
                                    </div>
                                </div>
                                <div className="flex flex-row gap-2">
                                    <div className="text-sm text-gray-500">{floor.room_count} rooms</div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </>
    )
};
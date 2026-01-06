import PageHeader from "../components/PageHeader";
import { useParams } from "react-router-dom";
import { useApi } from '../hooks/useApi';
import { floorsApi } from '../api';

export default function FloorDetail() {
    const { id } = useParams();

    const { data, loading, error } = useApi(() => floorsApi.get(Number(id)));
    console.log(data);

    if (loading) {
        return <div>Loading...</div>;
    }
    
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <>
            <PageHeader title={`Floor ${data?.floor_number}: ${data?.name}`} />
            <div className="flex flex-row">
                <div className="flex flex-col gap-2">

                </div>
            </div>
        </>
    )
};
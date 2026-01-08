import { DataTable } from "@/components/DataTable";
import { useRoomStore } from "@/stores/roomsStore";
import { roomColumns } from "./columns";
import type { Room } from "@/api";

interface RoomsTableProps {
    data: Room[] | undefined;
}

export default function RoomsTable({ data }: RoomsTableProps) {
    const { rowSelection, setRowSelection } = useRoomStore();

    return (
        <DataTable
            columns={roomColumns}
            data={data || []}
            selection={{
                rowSelection,
                onRowSelectionChange: setRowSelection,
            }}
            emptyMessage="No rooms found."
        />
    );
}
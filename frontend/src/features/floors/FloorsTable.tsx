import { DataTable } from "@/components/DataTable";
import { useFloorStore } from "@/stores/floorsStore";
import { floorColumns } from "./columns";
import type { Floor } from "@/api";

interface FloorsTableProps {
    data: Floor[] | undefined;
}

export default function FloorsTable({ data }: FloorsTableProps) {
    const { rowSelection, setRowSelection } = useFloorStore();

    return (
        <DataTable
            columns={floorColumns}
            data={data || []}
            selection={{
                rowSelection,
                onRowSelectionChange: setRowSelection,
            }}
            emptyMessage="No floors found."
        />
    );
}
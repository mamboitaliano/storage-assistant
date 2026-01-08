import { DataTable } from "@/components/DataTable";
import { useContainerStore } from "@/stores/containerStore";
import { containerColumns } from "./columns";
import type { Container } from "@/api";

interface ContainersTableProps {
    data: Container[] | undefined;
}

export default function ContainersTable({ data }: ContainersTableProps) {
    const { rowSelection, setRowSelection } = useContainerStore();

    return (
        <DataTable
            columns={containerColumns}
            data={data || []}
            selection={{
                rowSelection,
                onRowSelectionChange: setRowSelection,
            }}
            emptyMessage="No containers found."
        />
    );  
}
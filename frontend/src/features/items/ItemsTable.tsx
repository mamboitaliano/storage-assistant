import { DataTable } from "@/components/DataTable";
import { useItemStore } from "@/stores/itemsStore";
import { itemColumns } from "./columns";
import type { Item } from "@/api";

interface ItemsTableProps {
    data: Item[] | undefined;
}

export default function ItemsTable({ data }: ItemsTableProps) {
    const { rowSelection, setRowSelection } = useItemStore();

    return (
        <DataTable
            columns={itemColumns}
            data={data || []}
            selection={{
                rowSelection,
                onRowSelectionChange: setRowSelection,
            }}
            emptyMessage="No items found."
        />
    );
}
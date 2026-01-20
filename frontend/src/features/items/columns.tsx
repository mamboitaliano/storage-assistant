import type { ColumnDef, Row, Table } from "@tanstack/react-table";
import type { Item } from "@/api";
import ItemDropdown from "@/features/items/ItemDropdown";
import { Checkbox } from "@/components/ui/checkbox";

export const itemColumns: ColumnDef<Item>[] = [
  {
    accessorKey: "select",
    header: ({ table }: { table: Table<Item> }) => (
      <Checkbox
        checked={table.getIsAllPageRowsSelected()}
        onCheckedChange={(value: boolean) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }: { row: Row<Item> }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value: boolean) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
  },
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => row.original.name ?? "Untitled",
  },
  {
    accessorKey: "quantity",
    header: "Quantity",
    cell: ({ row }) => row.original.quantity,
  },
  {
    accessorKey: "room",
    header: "Room",
    cell: ({ row }) => row.original.room.name ?? "Untitled",
  },
  {
    accessorKey: "container",
    header: "Container",
    cell: ({ row }) => row.original.container?.name ?? "Untitled",
  },
  {
    id: "actions",
    cell: ({ row }: { row: Row<Item> }) => {
      const item = row.original;

      return (
          <ItemDropdown item={item} />
    )},
  },
];
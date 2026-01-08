import type { ColumnDef, Row, Table } from "@tanstack/react-table";
import type { Room } from "@/api";
import RoomDropdown from "./RoomDropdown";
import { Checkbox } from "@/components/ui/checkbox";

export const roomColumns: ColumnDef<Room>[] = [
  {
    accessorKey: "select",
    header: ({ table }: { table: Table<Room> }) => (
      <Checkbox
        checked={table.getIsAllPageRowsSelected()}
        onCheckedChange={(value: boolean) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }: { row: Row<Room> }) => (
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
    accessorKey: "item_count",
    header: "Items",
    cell: ({ row }) => row.original.item_count,
  },
  {
    accessorKey: "container_count",
    header: "Containers",
    cell: ({ row }) => row.original.container_count,
  },
  {
    id: "actions",
    cell: ({ row }: { row: Row<Room> }) => {
      const room = row.original;
      return <RoomDropdown room={room} />;
    },
  },
];
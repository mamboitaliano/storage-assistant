import type { ColumnDef, Row } from "@tanstack/react-table";
import type { Room } from "@/api";
import RoomDropdown from "./RoomDropdown";

export const roomColumns: ColumnDef<Room>[] = [
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
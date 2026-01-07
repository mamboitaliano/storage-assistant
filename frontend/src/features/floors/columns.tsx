import type { ColumnDef, Row } from "@tanstack/react-table";
import type { Floor } from "@/api";
import FloorDropdown from "./FloorDropdown";


export const floorColumns: ColumnDef<Floor>[] = [
  {
    accessorKey: "floor_number",
    header: "Floor #",
    cell: ({ row }) => row.original.floor_number ?? "—",
  },
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => row.original.name ?? "Untitled",
  },
  {
    accessorKey: "room_count",
    header: "Rooms",
    cell: ({ row }) => row.original.room_count,
  },
  {
    id: "actions",
    cell: ({ row }: { row: Row<Floor> }) => {
      const floor = row.original;

      return (
          <FloorDropdown floor={floor} />
    )},
  },
]

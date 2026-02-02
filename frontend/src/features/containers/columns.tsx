import type { ColumnDef, Row } from "@tanstack/react-table";
import type { Container } from "@/api";
import ContainerDropdown from "./ContainerDropdown";
import { Checkbox } from "@/components/ui/checkbox";
import type { Table } from "@tanstack/react-table";

export const containerColumns: ColumnDef<Container>[] = [
  {
    accessorKey: "select",
    header: ({ table }: { table: Table<Container> }) => (
        <Checkbox
            checked={table.getIsAllPageRowsSelected()}
            onCheckedChange={(value: boolean) => table.toggleAllPageRowsSelected(!!value)}
            aria-label="Select all"
        />
    ),
    cell: ({ row }: { row: Row<Container> }) => (
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
    accessorKey: "room",
    header: "Room",
    cell: ({ row }) => row.original.room?.name ?? "—",
  },
  {
    accessorKey: "item_count",
    header: "Items",
    cell: ({ row }) => row.original.item_count,
  },
  {
    id: "actions",
    cell: ({ row }: { row: Row<Container> }) => {
      const container = row.original;

      return (
          <ContainerDropdown container={container} />
    )},
  },
]

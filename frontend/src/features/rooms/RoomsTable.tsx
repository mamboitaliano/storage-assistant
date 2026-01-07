import type { Room } from "@/api";
import { DataTable } from "./data-table";
import { roomColumns } from "./columns";

interface RoomsTableProps {
  data: Room[]
}

export default function RoomsTable({ data }: RoomsTableProps) {
  return <DataTable columns={roomColumns} data={data} />
}

import type { Floor } from "@/api"
import { DataTable } from "./data-table"
import { floorColumns } from "./columns"

interface FloorsTableProps {
  data: Floor[]
}

export function FloorsTable({ data }: FloorsTableProps) {
  return <DataTable columns={floorColumns} data={data} />
}

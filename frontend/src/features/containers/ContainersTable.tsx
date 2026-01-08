import type { Container } from "@/api"
import { DataTable } from "./data-table"
import { containerColumns } from "./columns"

interface ContainersTableProps {
  data: Container[]
}

export default function ContainersTable({ data }: ContainersTableProps) {
  return <DataTable columns={containerColumns} data={data} />
}

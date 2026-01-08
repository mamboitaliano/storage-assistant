import type { Item } from "@/api";
import { DataTable } from "./data-table"
import { itemColumns } from "./columns";

interface ItemTableProps {
  data: Item[]
}

export default function ItemsTable({ data }: ItemTableProps) {
  return <DataTable columns={itemColumns} data={data} />
}

import type { ColumnDef, TableOptions } from "@tanstack/react-table";
import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

type SelectionState<TData> = 
    | { rowSelection: Record<string, boolean>; onRowSelectionChange: TableOptions<TData>["onRowSelectionChange"] }
    | { rowSelection: undefined; onRowSelectionChange: undefined };

interface DataTableProps<TData extends { id: number }, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  selection?: SelectionState<TData>;
  emptyMessage?: string;
}

export function DataTable<TData extends { id: number }, TValue>({
  columns,
  data,
  selection,
  emptyMessage = "No data.",
}: DataTableProps<TData, TValue>) {

  const table = useReactTable({
    data,
    columns,
    enableRowSelection: !!selection,
    state: selection ? { rowSelection: selection.rowSelection } : undefined,
    getCoreRowModel: getCoreRowModel(),
    getRowId: row => row.id.toString(),
    onRowSelectionChange: selection?.onRowSelectionChange,
  });

  return (
    <div className="rounded-md border border-border/50 bg-card/40 shadow-sm">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map(headerGroup => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <TableHead key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map(row => (
              <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
                {row.getVisibleCells().map(cell => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center text-sm text-muted-foreground">
                {emptyMessage}
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  )
}

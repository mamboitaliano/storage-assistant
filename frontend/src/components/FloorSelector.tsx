import { Field, FieldLabel } from "@/components/ui/field";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { Floor } from "@/api";

interface FloorSelectorProps{
    floors: Floor[] | null;
    onValueChange: (value: string) => void;
    disabled?: boolean;
}

export function FloorSelector({ floors, onValueChange, disabled }: FloorSelectorProps) {
    return (
        <Field>
            <FieldLabel>Floor</FieldLabel>
            <Select onValueChange={onValueChange} disabled={disabled}>
                <SelectTrigger>
                    <SelectValue placeholder="Select a floor" />
                </SelectTrigger>
                <SelectContent position="item-aligned">
                    {floors?.map(floor => (
                        <SelectItem key={floor.id} value={floor.id.toString()}>{floor.name}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </Field>
    );
}
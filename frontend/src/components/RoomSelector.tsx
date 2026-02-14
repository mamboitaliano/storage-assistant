import { Field, FieldLabel } from "@/components/ui/field";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { RoomOption } from "@/api";

interface RoomSelectionProps{
    rooms: RoomOption[] | null;
    value?: string;
    onValueChange: (value: string) => void;
    disabled?: boolean;
    required?: boolean;
}

export function RoomSelector({ value, rooms, onValueChange, disabled, required }: RoomSelectionProps) {
    return (
        <Field>
            <FieldLabel>Room {required ? "(required)" : ""}</FieldLabel>
            <Select value={value} onValueChange={onValueChange} disabled={disabled}>
                <SelectTrigger>
                    <SelectValue placeholder="Select a room" />
                </SelectTrigger>
                <SelectContent position="item-aligned">
                    {rooms?.map((room) => (
                        <SelectItem key={room.id} value={room.id.toString()}>{room.name}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </Field>
    );
}
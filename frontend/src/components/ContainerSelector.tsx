import { Field, FieldLabel } from "@/components/ui/field";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { ContainerOption } from "@/api";

interface ContainerSelectorProps {
    containers: ContainerOption[] | null;
    onValueChange: (value: string) => void;
    disabled?: boolean;
}

export function ContainerSelector({ containers, onValueChange, disabled }: ContainerSelectorProps) {
    return (
        <Field>
            <FieldLabel>Container (optional)</FieldLabel>
            <Select onValueChange={onValueChange} disabled={disabled}>
                <SelectTrigger>
                    <SelectValue placeholder="Select a container" />
                </SelectTrigger>
                <SelectContent position="item-aligned">
                    {containers?.map((container) => (
                        <SelectItem key={container.id} value={container.id.toString()}>{container.name}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </Field>
    );
}


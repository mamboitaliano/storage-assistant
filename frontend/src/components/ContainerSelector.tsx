import { Field, FieldLabel } from "@/components/ui/field";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface ContainerSelectorOption {
    id: number;
    name: string | null;
}

interface ContainerSelectorProps {
    containers: ContainerSelectorOption[] | null;
    value?: string;
    onValueChange: (value: string) => void;
    disabled?: boolean;
    placeholder?: string;
    label?: string;
}

export function ContainerSelector({ containers, value, onValueChange, disabled, placeholder = "Select a container", label = "Container (optional)" }: ContainerSelectorProps) {
    return (
        <Field>
            <FieldLabel>{label}</FieldLabel>
            <Select value={value ?? ""} onValueChange={onValueChange} disabled={disabled}>
                <SelectTrigger>
                    <SelectValue placeholder={placeholder} />
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


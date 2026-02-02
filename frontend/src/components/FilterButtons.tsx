import { Button } from "@/components/ui/button";

interface FilterButtonsProps {
    onApply: () => void;
    onClear: () => void;
    applyDisabled: boolean;
    clearDisabled: boolean;
}

/**
 * Reusable Apply/Clear buttons for filter components.
 * Includes invisible spacer to align with filter input labels.
 */
export default function FilterButtons({
    onApply,
    onClear,
    applyDisabled,
    clearDisabled,
}: FilterButtonsProps) {
    return (
        <div className="flex flex-col gap-1.5 ml-auto">
            <div className="text-sm invisible">spacer</div>
            <div className="flex gap-2">
                <Button 
                    onClick={onApply} 
                    disabled={applyDisabled}
                    size="sm"
                >
                    Apply
                </Button>
                <Button 
                    onClick={onClear} 
                    variant="outline" 
                    disabled={clearDisabled}
                    size="sm"
                >
                    Clear
                </Button>
            </div>
        </div>
    );
}

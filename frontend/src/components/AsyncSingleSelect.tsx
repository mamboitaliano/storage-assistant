import { useState, useEffect, useRef, useCallback } from "react";
import { Check, ChevronsUpDown, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";

export interface SelectOption {
    id: number;
    name: string | null;
}

interface AsyncSingleSelectProps {
    searchFn: (query: string) => Promise<SelectOption[]>; // async func to search for options
    value: SelectOption | null; // currently selected option
    onChange: (value: SelectOption | null) => void; // cb when selection changes
    placeholder?: string; // placeholder text when nothing selected
    debounceMs?: number; // debounce delay ms
    minSearchLength?: number; // min chars to trigger search
    label?: string; // label for the field
    disabled?: boolean; // whether field is disabled
}

export default function AsyncSingleSelect({
    searchFn,
    value,
    onChange,
    placeholder = "Search...",
    debounceMs = 300,
    minSearchLength = 1,
    label,
    disabled = false,
}: AsyncSingleSelectProps) {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState("");
    const [options, setOptions] = useState<SelectOption[]>([]);
    const [loading, setLoading] = useState(false);
    
    const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    // Fetch options when query changes (debounced)
    useEffect(() => {
        if (debounceTimerRef.current) {
            clearTimeout(debounceTimerRef.current);
        }

        if (query.length < minSearchLength) {
            setOptions([]);
            setLoading(false);
            return;
        }

        setLoading(true);

        debounceTimerRef.current = setTimeout(async () => {
            try {
                const results = await searchFn(query);
                setOptions(results);
            } catch (error) {
                console.error("Search failed:", error);
                setOptions([]);
            } finally {
                setLoading(false);
            }
        }, debounceMs);

        return () => {
            if (debounceTimerRef.current) {
                clearTimeout(debounceTimerRef.current);
            }
        };
    }, [query, searchFn, debounceMs, minSearchLength]);

    // handle selecting/deselecting an option
    const handleSelect = useCallback((option: SelectOption) => {
        if (value?.id === option.id) {
            onChange(null);
        } else {
            onChange(option);
        }

        setOpen(false);
    }, [value, onChange]);

    return (
        <div className="flex flex-col gap-1.5">
            {label && (
                <label className="text-sm text-muted-foreground">{label}</label>
            )}
            
            <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                    <Button
                        variant="outline"
                        role="combobox"
                        aria-expanded={open}
                        disabled={disabled}
                        className="w-full justify-between font-normal"
                    >
                        <span className="truncate text-muted-foreground">
                            {value?.name || placeholder}
                        </span>
                        <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-[--radix-popover-trigger-width] p-0" align="start">
                    <Command shouldFilter={false}>
                        <CommandInput 
                            placeholder={placeholder}
                            value={query}
                            onValueChange={setQuery}
                        />
                        <CommandList>
                            {loading && (
                                <div className="flex items-center justify-center py-6">
                                    <Loader2 className="h-4 w-4 animate-spin" />
                                    <span className="ml-2 text-sm text-muted-foreground">Searching...</span>
                                </div>
                            )}
                            {!loading && query.length >= minSearchLength && options.length === 0 && (
                                <CommandEmpty>No results found.</CommandEmpty>
                            )}
                            {!loading && query.length < minSearchLength && (
                                <div className="py-6 text-center text-sm text-muted-foreground">
                                    Type to search...
                                </div>
                            )}
                            {!loading && options.length > 0 && (
                                <CommandGroup>
                                    {options.map((option, index) => (
                                        <CommandItem
                                            key={`option-${option.id}-${index}`}
                                            value={String(option.id)}
                                            onSelect={() => handleSelect(option)}
                                        >
                                            <Check
                                                className={cn(
                                                    "mr-2 h-4 w-4",
                                                    value?.id === option.id ? "opacity-100" : "opacity-0"
                                                )}
                                            />
                                            {option.name || `(unnamed)`}
                                        </CommandItem>
                                    ))}
                                </CommandGroup>
                            )}
                        </CommandList>
                    </Command>
                </PopoverContent>
            </Popover>
        </div>
    );
}

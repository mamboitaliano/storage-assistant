import { useState, useEffect, useRef, useCallback } from "react";
import { Check, ChevronsUpDown, X, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
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

interface AsyncMultiSelectProps {
    searchFn: (query: string) => Promise<SelectOption[]>; // async func to search for options
    value: number[]; // currently selected option ids
    onChange: (value: number[]) => void; // cb when selection changes
    placeholder?: string; // placeholder text when nothing selected
    debounceMs?: number; // debounce delay ms
    minSearchLength?: number; // min chars to trigger search
    label?: string; // label for the field
    disabled?: boolean; // whether field is disabled
}

export default function AsyncMultiSelect({
    searchFn,
    value,
    onChange,
    placeholder = "Search...",
    debounceMs = 300,
    minSearchLength = 1,
    label,
    disabled = false,
}: AsyncMultiSelectProps) {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState("");
    const [options, setOptions] = useState<SelectOption[]>([]);
    const [loading, setLoading] = useState(false);
    const [selectedOptions, setSelectedOptions] = useState<SelectOption[]>([]);
    
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
        const isSelected = value.includes(option.id);
        
        if (isSelected) {
            // rm from selection
            onChange(value.filter(id => id !== option.id));
            setSelectedOptions(prev => prev.filter(o => o.id !== option.id));
        } else {
            // add to selection
            onChange([...value, option.id]);
            setSelectedOptions(prev => [...prev, option]);
        }
    }, [value, onChange]);

    // rm a selected option via badge X button
    const handleRemove = useCallback((optionId: number) => {
        onChange(value.filter(id => id !== optionId));
        setSelectedOptions(prev => prev.filter(o => o.id !== optionId));
    }, [value, onChange]);

    // clear all selections
    const handleClearAll = useCallback(() => {
        onChange([]);
        setSelectedOptions([]);
    }, [onChange]);

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
                        className="w-64 justify-between font-normal"
                    >
                        <span className="truncate text-muted-foreground">
                            {value.length > 0 
                                ? `${value.length} selected` 
                                : placeholder}
                        </span>
                        <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-64 p-0" align="start">
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
                                    {options.map((option) => (
                                        <CommandItem
                                            key={option.id}
                                            value={String(option.id)}
                                            onSelect={() => handleSelect(option)}
                                        >
                                            <Check
                                                className={cn(
                                                    "mr-2 h-4 w-4",
                                                    value.includes(option.id) ? "opacity-100" : "opacity-0"
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

            {/* Selected items as badges */}
            {selectedOptions.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-1">
                    {selectedOptions.map((option) => (
                        <Badge 
                            key={option.id} 
                            variant="secondary"
                            className="gap-1 pr-1"
                        >
                            {option.name || `(unnamed)`}
                            <button
                                type="button"
                                onClick={() => handleRemove(option.id)}
                                className="ml-1 rounded-full hover:bg-muted p-0.5"
                            >
                                <X className="h-3 w-3" />
                            </button>
                        </Badge>
                    ))}
                    {selectedOptions.length > 1 && (
                        <button
                            type="button"
                            onClick={handleClearAll}
                            className="text-xs text-muted-foreground hover:text-foreground"
                        >
                            Clear all
                        </button>
                    )}
                </div>
            )}
        </div>
    );
}

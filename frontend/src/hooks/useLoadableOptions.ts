import { useState, useCallback } from "react";

interface UseLoadableOptionsReturn<T> {
    options: T[];
    loading: boolean;
    error: boolean;
    isLoaded: boolean;
    loadAll: () => Promise<void>;
}

/**
 * Hook for managing "Show all" / loadable options pattern.
 * Handles loading state, error state, and caches loaded options.
 * 
 * @param fetchFn - Async function that fetches all options
 * @returns Object with options, loading/error states, and loadAll function
 */
export function useLoadableOptions<T>(
    fetchFn: () => Promise<T[]>
): UseLoadableOptionsReturn<T> {
    const [options, setOptions] = useState<T[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(false);

    const loadAll = useCallback(async () => {
        setLoading(true);
        setError(false);
        try {
            const data = await fetchFn();
            setOptions(data);
        } catch (err) {
            console.error("Failed to load options:", err);
            setError(true);
        } finally {
            setLoading(false);
        }
    }, [fetchFn]);

    return {
        options,
        loading,
        error,
        isLoaded: options.length > 0,
        loadAll,
    };
}

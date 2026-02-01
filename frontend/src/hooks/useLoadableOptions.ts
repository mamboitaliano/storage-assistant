import { useState, useCallback } from "react";

interface OptionsResponse<T> {
    data: T[];
    total: number;
    hasMore: boolean;
}

interface UseLoadableOptionsReturn<T> {
    options: T[];
    loading: boolean;
    error: boolean;
    isLoaded: boolean;
    total: number;
    hasMore: boolean;
    loadAll: () => Promise<void>;
}

/**
 * Hook for managing "Show all" / loadable options pattern.
 * Handles loading state, error state, and caches loaded options.
 * 
 * @param fetchFn - Async function that fetches options with total and hasMore
 * @returns Object with options, loading/error states, hasMore indicator, and loadAll function
 */
export function useLoadableOptions<T>(
    fetchFn: () => Promise<OptionsResponse<T>>
): UseLoadableOptionsReturn<T> {
    const [options, setOptions] = useState<T[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(false);
    const [total, setTotal] = useState(0);
    const [hasMore, setHasMore] = useState(false);

    const loadAll = useCallback(async () => {
        setLoading(true);
        setError(false);
        try {
            const response = await fetchFn();
            setOptions(response.data);
            setTotal(response.total);
            setHasMore(response.hasMore);
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
        total,
        hasMore,
        loadAll,
    };
}

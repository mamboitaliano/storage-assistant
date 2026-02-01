import { useState, useEffect, useCallback, useRef } from 'react';
import type { PaginatedResponse } from "../api";

interface UsePaginatedApiOptions<TFilters> {
    initialPage?: number;
    initialFilters?: TFilters;
}

export function usePaginatedApi<T, TFilters = undefined>(
        fetchFn: TFilters extends undefined 
            ? (page: number) => Promise<PaginatedResponse<T>>
            : (page: number, filters?: TFilters) => Promise<PaginatedResponse<T>>,
        options: UsePaginatedApiOptions<TFilters> = {}
    ) {
    const { initialPage = 1, initialFilters } = options;

    const [page, setPage] = useState(initialPage);
    const [appliedFilters, setAppliedFilters] = useState<TFilters | undefined>(initialFilters);
    const [data, setData] = useState<PaginatedResponse<T> | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    
    // Track the current request to allow cancellation
    const abortControllerRef = useRef<AbortController | null>(null);

    const refetch = useCallback(async () => {
        // Cancel any in-flight request
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
        abortControllerRef.current = new AbortController();

        setLoading(true);

        try {
            const result = await (fetchFn as (page: number, filters?: TFilters) => Promise<PaginatedResponse<T>>)(page, appliedFilters);
            setData(result);
            setError(null);
        } catch (e) {
            // Don't set error if request was aborted
            if ((e as Error).name !== 'AbortError') {
                setError(e as Error);
            }
        } finally {
            setLoading(false);
        }
    }, [fetchFn, page, appliedFilters]);

    useEffect(() => {
        refetch();
    }, [refetch]);

    // Apply filters and reset to page 1
    const applyFilters = useCallback((filters: TFilters) => {
        setAppliedFilters(filters);
        setPage(1);
    }, []);

    // Clear filters and reset to page 1
    const clearFilters = useCallback(() => {
        setAppliedFilters(undefined);
        setPage(1);
    }, []);

    const totalPages = data ? Math.ceil(data.total / data.pageSize) : 0;
    const hasMultiplePages = totalPages > 1;

    return {
        data: data?.data ?? [],
        total: data?.total ?? 0,
        page,
        pageSize: data?.pageSize ?? 25,
        totalPages,
        hasMultiplePages,
        setPage,
        loading,
        error,
        refetch,
        appliedFilters,
        applyFilters,
        clearFilters,
    };
}
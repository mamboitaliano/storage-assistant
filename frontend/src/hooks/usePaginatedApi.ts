import { useState, useEffect, useCallback } from 'react';
import type { PaginatedResponse } from "../api";

interface UsePaginatedApiOptions {
    initialPage?: number;
}

export function usePaginatedApi<T>(
    fetchFn: (page: number) => Promise<PaginatedResponse<T>>,
    options: UsePaginatedApiOptions = {}
) {
    const { initialPage = 1 } = options;

    const [page, setPage] = useState(initialPage);
    const [data, setData] = useState<PaginatedResponse<T> | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const refetch = useCallback(async () => {
        setLoading(true);

        try {
            const result = await fetchFn(page);
            setData(result);
            setError(null);
        } catch (e) {
            setError(e as Error);
        } finally {
            setLoading(false);
        }
    }, [fetchFn, page]);

    useEffect(() => {
        refetch();
    }, [refetch]);

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
    };
}
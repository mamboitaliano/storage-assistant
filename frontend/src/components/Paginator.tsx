import { useState } from "react";
import {
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
} from "@/components/ui/pagination"
import { Input } from "@/components/ui/input"

export default function Paginator({
    page,
    totalPages,
    onPageChange
}: {
    page: number,
    totalPages: number,
    onPageChange: (page: number) => void
}) {
    const [goToPage, setGoToPage] = useState("");

    const getPageNumbers = (): (number | 'ellipsis')[] => {
        // If 8 or fewer pages, show all
        if (totalPages <= 8) {
            return Array.from({ length: totalPages }, (_, i) => i + 1);
        }

        const pages: (number | 'ellipsis')[] = [];

        // Near start: show 1-8, ellipsis, last
        if (page <= 4) {
            for (let i = 1; i <= 8; i++) pages.push(i);
            pages.push('ellipsis');
            pages.push(totalPages);
            return pages;
        }

        // Near end: show 1, ellipsis, last 8
        if (page >= totalPages - 3) {
            pages.push(1);
            pages.push('ellipsis');
            for (let i = totalPages - 7; i <= totalPages; i++) pages.push(i);
            return pages;
        }

        // Middle: show 1, ellipsis, 7 pages centered on current, ellipsis, last
        pages.push(1);
        pages.push('ellipsis');
        for (let i = page - 3; i <= page + 3; i++) pages.push(i);
        pages.push('ellipsis');
        pages.push(totalPages);
        return pages;
    };

    const handleGoToPage = () => {
        const targetPage = parseInt(goToPage, 10);
        if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= totalPages) {
            onPageChange(targetPage);
            setGoToPage("");
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            handleGoToPage();
        }
    };

    const pageNumbers = getPageNumbers();
    const isFirstPage = page === 1;
    const isLastPage = page === totalPages;
    const showGoToPage = totalPages > 9;

    return (
        <div className="flex flex-col items-center gap-3">
            <Pagination>
                <PaginationContent>
                    <PaginationItem>
                        <PaginationPrevious 
                            onClick={() => !isFirstPage && onPageChange(page - 1)}
                            className={isFirstPage ? 'pointer-events-none opacity-50' : 'cursor-pointer'}
                        />
                    </PaginationItem>

                    {pageNumbers.map((pageNum, index) => (
                        pageNum === 'ellipsis' ? (
                            <PaginationItem key={`ellipsis-${index}`}>
                                <PaginationEllipsis />
                            </PaginationItem>
                        ) : (
                            <PaginationItem key={pageNum}>
                                <PaginationLink 
                                    onClick={() => onPageChange(pageNum)} 
                                    isActive={pageNum === page}
                                    className="cursor-pointer"
                                >
                                    {pageNum}
                                </PaginationLink>
                            </PaginationItem>
                        )
                    ))}

                    <PaginationItem>
                        <PaginationNext 
                            onClick={() => !isLastPage && onPageChange(page + 1)}
                            className={isLastPage ? 'pointer-events-none opacity-50' : 'cursor-pointer'}
                        />
                    </PaginationItem>
                </PaginationContent>
            </Pagination>

            {showGoToPage && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <span>Go to page</span>
                    <Input
                        type="number"
                        min={1}
                        max={totalPages}
                        value={goToPage}
                        onChange={(e) => setGoToPage(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={`1-${totalPages}`}
                        className="w-20 h-8 text-center"
                    />
                    <button
                        onClick={handleGoToPage}
                        className="px-3 py-1 text-sm rounded border border-border hover:bg-accent hover:text-accent-foreground transition-colors"
                    >
                        Go
                    </button>
                </div>
            )}
        </div>
    );
}

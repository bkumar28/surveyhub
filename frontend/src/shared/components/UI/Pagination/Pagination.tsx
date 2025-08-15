import React from 'react';
import styles from './Pagination.module.scss';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  className?: string;
  showFirstLast?: boolean;
  size?: 'sm' | 'md' | 'lg';
  maxVisiblePages?: number;
  disabled?: boolean;
  ariaLabel?: string;
  testId?: string;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  className = '',
  showFirstLast = true,
  size = 'md',
  maxVisiblePages = 5,
  disabled = false,
  ariaLabel = 'Pagination',
  testId,
}) => {
  // Don't render pagination if there's only one page
  if (totalPages <= 1) {
    return null;
  }

  // Calculate visible page range
  const getVisiblePageRange = () => {
    if (totalPages <= maxVisiblePages) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    // Calculate half of max visible pages (rounded down)
    const halfVisible = Math.floor(maxVisiblePages / 2);

    // Calculate start and end page numbers
    let startPage = Math.max(currentPage - halfVisible, 1);
    let endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

    // Adjust if we're near the end
    if (endPage === totalPages) {
      startPage = Math.max(endPage - maxVisiblePages + 1, 1);
    }

    return Array.from(
      { length: endPage - startPage + 1 },
      (_, i) => startPage + i
    );
  };

  const visiblePages = getVisiblePageRange();

  // Go to a specific page
  const goToPage = (page: number) => {
    if (page !== currentPage && page >= 1 && page <= totalPages && !disabled) {
      onPageChange(page);
    }
  };

  return (
    <nav
      className={`${styles.pagination} ${className}`}
      aria-label={ariaLabel}
      data-testid={testId}
    >
      <ul className={`${styles.paginationList} ${styles[`size-${size}`]}`}>
        {/* First page button */}
        {showFirstLast && (
          <li className={styles.paginationItem}>
            <button
              className={styles.paginationLink}
              onClick={() => goToPage(1)}
              disabled={currentPage === 1 || disabled}
              aria-label="Go to first page"
            >
              &laquo;
            </button>
          </li>
        )}

        {/* Previous page button */}
        <li className={styles.paginationItem}>
          <button
            className={styles.paginationLink}
            onClick={() => goToPage(currentPage - 1)}
            disabled={currentPage === 1 || disabled}
            aria-label="Go to previous page"
          >
            &lsaquo;
          </button>
        </li>

        {/* Show ellipsis if not starting from first page */}
        {visiblePages[0] > 1 && (
          <li className={`${styles.paginationItem} ${styles.ellipsis}`}>
            <span>&hellip;</span>
          </li>
        )}

        {/* Page numbers */}
        {visiblePages.map((page) => (
          <li
            key={page}
            className={`${styles.paginationItem} ${
              currentPage === page ? styles.active : ''
            }`}
          >
            <button
              className={styles.paginationLink}
              onClick={() => goToPage(page)}
              disabled={disabled}
              aria-label={`Page ${page}`}
              aria-current={currentPage === page ? 'page' : undefined}
            >
              {page}
            </button>
          </li>
        ))}

        {/* Show ellipsis if not ending at last page */}
        {visiblePages[visiblePages.length - 1] < totalPages && (
          <li className={`${styles.paginationItem} ${styles.ellipsis}`}>
            <span>&hellip;</span>
          </li>
        )}

        {/* Next page button */}
        <li className={styles.paginationItem}>
          <button
            className={styles.paginationLink}
            onClick={() => goToPage(currentPage + 1)}
            disabled={currentPage === totalPages || disabled}
            aria-label="Go to next page"
          >
            &rsaquo;
          </button>
        </li>

        {/* Last page button */}
        {showFirstLast && (
          <li className={styles.paginationItem}>
            <button
              className={styles.paginationLink}
              onClick={() => goToPage(totalPages)}
              disabled={currentPage === totalPages || disabled}
              aria-label="Go to last page"
            >
              &raquo;
            </button>
          </li>
        )}
      </ul>
    </nav>
  );
};

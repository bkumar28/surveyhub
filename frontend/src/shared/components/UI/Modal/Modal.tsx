import React, { useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import styles from './Modal.module.scss';

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closeOnBackdropClick?: boolean;
  closeOnEsc?: boolean;
  className?: string;
  showCloseButton?: boolean;
  centered?: boolean;
  scrollable?: boolean;
  testId?: string;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = 'md',
  closeOnBackdropClick = true,
  closeOnEsc = true,
  className = '',
  showCloseButton = true,
  centered = false,
  scrollable = false,
  testId,
}) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (closeOnEsc && event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
      document.body.classList.add('modal-open');
    }

    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.classList.remove('modal-open');
    };
  }, [isOpen, closeOnEsc, onClose]);

  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus();
    }
  }, [isOpen]);

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget && closeOnBackdropClick) {
      onClose();
    }
  };

  if (!isOpen) {
    return null;
  }

  const modalContent = (
    <div
      className={`${styles.modalBackdrop} ${isOpen ? styles.show : ''}`}
      onClick={handleBackdropClick}
      data-testid={testId ? `${testId}-backdrop` : 'modal-backdrop'}
    >
      <div
        ref={modalRef}
        className={`
          ${styles.modal}
          ${styles[`modal-${size}`]}
          ${centered ? styles.centered : ''}
          ${scrollable ? styles.scrollable : ''}
          ${className}
        `}
        role="dialog"
        aria-modal="true"
        tabIndex={-1}
        data-testid={testId || 'modal'}
      >
        {(title || showCloseButton) && (
          <div className={styles.modalHeader}>
            {title && <h4 className={styles.modalTitle}>{title}</h4>}
            {showCloseButton && (
              <button
                type="button"
                className={styles.closeButton}
                onClick={onClose}
                aria-label="Close"
                data-testid={testId ? `${testId}-close` : 'modal-close'}
              >
                <span aria-hidden="true">&times;</span>
              </button>
            )}
          </div>
        )}
        <div className={styles.modalBody}>{children}</div>
        {footer && <div className={styles.modalFooter}>{footer}</div>}
      </div>
    </div>
  );

  return ReactDOM.createPortal(modalContent, document.body);
};

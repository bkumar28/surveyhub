// =============================================================================
// GLOBAL LOADING OVERLAY HELPERS
// =============================================================================
window.showLoading = function() {
  if (document.getElementById('globalLoadingOverlay')) return;
  const overlay = document.createElement('div');
  overlay.id = 'globalLoadingOverlay';
  overlay.style.position = 'fixed';
  overlay.style.top = '0';
  overlay.style.left = '0';
  overlay.style.width = '100vw';
  overlay.style.height = '100vh';
  overlay.style.background = 'rgba(255,255,255,0.6)';
  overlay.style.zIndex = '9999';
  overlay.innerHTML = '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:2rem;"><span class="spinner-border text-primary" role="status"></span></div>';
  document.body.appendChild(overlay);
};
window.hideLoading = function() {
  const overlay = document.getElementById('globalLoadingOverlay');
  if (overlay) overlay.remove();
};
// =============================================================================
// GLOBAL FETCH ERROR HANDLER
// =============================================================================
window.handleFetchError = function(error, context = '') {
  let message = 'An error occurred.';
  if (error instanceof Response) {
    if (error.status === 404) {
      message = context ? `${context.charAt(0).toUpperCase() + context.slice(1)} not found.` : 'Resource not found.';
    } else if (error.status === 500) {
      message = 'A server error occurred. Please try again later.';
    } else {
      message = `Request failed (${error.status}).`;
    }
  } else if (error instanceof Error) {
    message = error.message || message;
  } else if (typeof error === 'string') {
    message = error;
  }
  window.showAlert(message, 'danger');
};
// =============================================================================
// GLOBAL CONFIGURATION & UTILITY FUNCTIONS
// =============================================================================
window.API_BASE_URL = window.location.origin || 'http://localhost:8000';
window.getCookie = function(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
// =============================================================================
// GLOBAL ALERT HELPERS
// =============================================================================
// DRY helper for alert container
function getOrCreateAlertContainer() {
  let alertContainer = document.getElementById('alertContainer');
  if (!alertContainer) {
    alertContainer = document.createElement('div');
    alertContainer.id = 'alertContainer';
    alertContainer.style.position = 'fixed';
    alertContainer.style.top = '20px';
    alertContainer.style.right = '20px';
    alertContainer.style.zIndex = '99999';
    document.body.appendChild(alertContainer);
  }
  return alertContainer;
}

/**
 * Show a Bootstrap alert (danger, success, etc.)
 * @param {string} message - The message to display
 * @param {string} type - The alert type ('danger', 'success', etc.)
 */
window.showAlert = function(message, type = 'info') {
  const alertContainer = getOrCreateAlertContainer();
  const alertEl = document.createElement('div');
  alertEl.className = `alert alert-${type} alert-dismissible fade show`;
  alertEl.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  alertContainer.appendChild(alertEl);
  setTimeout(() => {
    const bsAlert = new bootstrap.Alert(alertEl);
    bsAlert.close();
  }, 5000);
};

window.showError = function(message) {
  window.showAlert(message, 'danger');
};

window.showSuccess = function(message) {
  window.showAlert(message, 'success');
};

// =============================================================================
// MAIN APPLICATION MODULE
// =============================================================================
/**
 * SurveyHub Frontend JavaScript
 *
 * Main application JavaScript file providing UI functionality,
 * navigation management, authentication, DataTable configuration,
 * and utility functions.
 *
 * @version 2.0.0
 * @author SurveyHub Team
 */

// Enforce strict mode for better error handling
'use strict';

// =============================================================================
// DATATABLE CONFIGURATION AND UTILITIES
// =============================================================================

/**
 * SurveyHubDataTable - Centralized DataTable configuration and helpers
 */
const SurveyHubDataTable = {
  /**
   * Initialize a DataTable with standard responsive configuration
   * @param {string|object} selector - The table selector or element
   * @param {object} options - Custom options to override defaults
   * @returns {object} DataTable instance
   */
  init: function(selector, options = {}) {
    // Default configuration with best practices for responsive tables
    const defaultConfig = {
      // Basic configuration
      pageLength: 10,
      ordering: true,
      responsive: true,
      autoWidth: false,
      scrollX: true,
      scrollCollapse: true,

      // Language customization
      language: {
        emptyTable: "No data available",
        zeroRecords: "No matching records found",
        info: "Showing _START_ to _END_ of _TOTAL_ entries",
        infoEmpty: "Showing 0 to 0 of 0 entries",
        search: "",
        searchPlaceholder: "Search...",
        lengthMenu: "Show _MENU_ entries per page",
        paginate: {
          next: "Next",
          previous: "Previous"
        }
      },

      // DOM structure for consistent layout
      dom: '<"row g-3 mb-3"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rt<"row g-2 mt-3"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',

      // Enhanced responsive configuration
      responsive: {
        details: {
          type: 'column',
          target: 'tr',
          renderer: function(api, rowIdx, columns) {
            const data = $.map(columns, function(col, i) {
              return col.hidden ?
                '<div class="responsive-item mb-2">' +
                  '<span class="responsive-item-label fw-bold">' + col.title + ':</span> ' +
                  '<span class="responsive-item-value">' + col.data + '</span>' +
                '</div>' : '';
            }).join('');

            return data ?
              $('<div class="p-2"/>').append(data) : false;
          }
        },
        breakpoints: [
          {name: 'desktop', width: Infinity},
          {name: 'laptop', width: 1366},
          {name: 'tablet', width: 1024},
          {name: 'phablet', width: 768},
          {name: 'phone', width: 480}
        ]
      },

      // Add consistent styling for headers and striped rows
      "drawCallback": function() {
        // Add background color to headers
        $('thead tr th').addClass('bg-light');

        // Make sure action buttons are responsive
        $('.btn-group, .dropdown, .action-buttons').addClass('d-flex flex-nowrap');
      },

      // Alternating row colors
      "stripeClasses": ['', 'bg-light-subtle']
    };

    // Merge default config with user options
    const mergedConfig = $.extend(true, {}, defaultConfig, options);

    // Initialize and return the DataTable
    return $(selector).DataTable(mergedConfig);
  },

  /**
   * Add export buttons to a DataTable
   * @param {string} tableId - The DataTable selector
   * @param {string} buttonContainer - The container for export buttons
   */
  addExportButtons: function(tableId, buttonContainer) {
    // This requires DataTables Buttons extension
    // Make sure you have included the necessary libraries
    const buttons = [
      {
        extend: 'csv',
        text: '<i class="bi bi-file-earmark-spreadsheet me-1"></i> CSV',
        className: 'btn btn-sm btn-outline-secondary',
        exportOptions: {
          columns: ':visible:not(.no-export)'
        }
      },
      {
        extend: 'excel',
        text: '<i class="bi bi-file-earmark-excel me-1"></i> Excel',
        className: 'btn btn-sm btn-outline-secondary',
        exportOptions: {
          columns: ':visible:not(.no-export)'
        }
      },
      {
        extend: 'pdf',
        text: '<i class="bi bi-file-earmark-pdf me-1"></i> PDF',
        className: 'btn btn-sm btn-outline-secondary',
        exportOptions: {
          columns: ':visible:not(.no-export)'
        }
      },
      {
        extend: 'print',
        text: '<i class="bi bi-printer me-1"></i> Print',
        className: 'btn btn-sm btn-outline-secondary',
        exportOptions: {
          columns: ':visible:not(.no-export)'
        }
      }
    ];

    // Initialize buttons
    new $.fn.dataTable.Buttons($(tableId).DataTable(), {
      buttons: buttons
    });

    // Add buttons to container
    $(tableId + 'Buttons').append($(tableId).DataTable().buttons().container());
  },

  /**
   * Setup responsive handlers for DataTable
   * @param {string} tableSelector - The DataTable selector
   */
  setupResponsiveHandlers: function(tableSelector) {
    // Add resize listener for responsive adjustments
    window.addEventListener('resize', function() {
      // Debounce the resize event
      if (this.resizeTimeout) clearTimeout(this.resizeTimeout);
      this.resizeTimeout = setTimeout(function() {
        const table = $(tableSelector).DataTable();
        table.columns.adjust().responsive.recalc();
      }, 200);
    });

    // Handle orientation changes specifically for mobile
    window.addEventListener('orientationchange', function() {
      setTimeout(function() {
        const table = $(tableSelector).DataTable();
        table.columns.adjust().responsive.recalc();
      }, 250);
    });

    // Add matchMedia listener for more reliable device-width changes
    const mediaQueryList = window.matchMedia("(max-width: 768px)");
    mediaQueryList.addEventListener("change", function(e) {
      setTimeout(function() {
        const table = $(tableSelector).DataTable();
        table.columns.adjust().responsive.recalc();
      }, 250);
    });
  },

  /**
   * Helper function to update filter indicators
   * @param {object} filters - The filter values
   * @param {object} elements - The filter elements
   */
  updateFilterIndicators: function(filters, elements) {
    // Check if filters exist
    const hasActiveFilters = Object.values(filters).some(val => val);

    // Apply visual feedback for active filters
    for (const [key, element] of Object.entries(elements)) {
      if (element) {
        element.classList.toggle('border-primary', !!filters[key]);
      }
    }

    // Update reset button if provided
    if (elements.resetBtn) {
      elements.resetBtn.classList.toggle('btn-outline-secondary', !hasActiveFilters);
      elements.resetBtn.classList.toggle('btn-secondary', hasActiveFilters);
    }
  },

  /**
   * Helper function for toast notifications
   * @param {string} message - The message to display
   * @param {string} type - The toast type (success, danger, info, etc.)
   */
  showToast: function(message, type = 'info') {
    const toastEl = document.createElement('div');
    toastEl.className = 'position-fixed bottom-0 end-0 p-3';
    toastEl.style.zIndex = '5';
    toastEl.innerHTML = `
      <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body">
            <i class="bi bi-info-circle me-2"></i> ${message}
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    `;
    document.body.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl.querySelector('.toast'));
    toast.show();
    setTimeout(() => toastEl.remove(), 3000);
  },

  /**
   * Make a table responsive for mobile with card view
   * @param {string} tableSelector - The table selector
   */
  applyMobileCardView: function(tableSelector) {
    const table = document.querySelector(tableSelector);
    if (!table) return;

    // Add media query styles for this specific table
    const styleEl = document.createElement('style');
    const tableId = table.id;

    styleEl.innerHTML = `
      @media screen and (max-width: 767px) {
        #${tableId} thead {
          display: none;
        }

        #${tableId} tbody tr {
          display: block;
          margin-bottom: 1rem;
          border: 1px solid #dee2e6;
          border-radius: 0.25rem;
        }

        #${tableId} tbody td {
          display: flex;
          justify-content: space-between;
          text-align: right;
          border-bottom: 1px solid #dee2e6;
          padding: 0.75rem;
        }

        #${tableId} tbody td:last-child {
          border-bottom: none;
        }

        #${tableId} tbody td:before {
          content: attr(data-label);
          font-weight: bold;
          text-align: left;
          margin-right: 1rem;
        }
      }
    `;

    document.head.appendChild(styleEl);

    // Add data-label attributes to cells
    const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());

    table.querySelectorAll('tbody tr').forEach(row => {
      Array.from(row.querySelectorAll('td')).forEach((cell, i) => {
        if (headers[i]) {
          cell.setAttribute('data-label', headers[i]);
        }
      });
    });
  },

  /**
   * Initialize table search with delay to improve performance
   * @param {string} inputSelector - The search input selector
   * @param {object} tableInstance - The DataTable instance
   */
  initializeTableSearch: function(inputSelector, tableInstance) {
    const searchInput = document.querySelector(inputSelector);
    if (!searchInput || !tableInstance) return;

    let searchTimeout;

    searchInput.addEventListener('keyup', function() {
      clearTimeout(searchTimeout);
      const searchTerm = this.value;

      searchTimeout = setTimeout(() => {
        tableInstance.search(searchTerm).draw();
      }, 300); // 300ms delay to reduce processing during typing
    });
  },

  /**
   * Export the current table data to CSV
   * @param {string} tableSelector - The DataTable selector
   * @param {string} filename - The name for the exported file
   */
  exportTableToCSV: function(tableSelector, filename = 'export') {
    const table = $(tableSelector).DataTable();
    const visibleColumns = table.columns().visible().toArray();
    const headers = [];

    // Get headers from visible columns
    table.columns().every(function(index) {
      if (visibleColumns[index]) {
        headers.push($(this.header()).text().trim());
      }
    });

    // Get data from visible columns
    const rows = [];
    table.rows({ search: 'applied' }).every(function() {
      const rowData = this.data();
      const visibleData = [];

      // Only include data from visible columns
      for (let i = 0; i < rowData.length; i++) {
        if (visibleColumns[i]) {
          // Try to extract text from HTML
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = rowData[i];
          visibleData.push(tempDiv.textContent.trim());
        }
      }

      rows.push(visibleData);
    });

    // Create CSV content
    let csvContent = headers.join(',') + '\n';
    rows.forEach(function(row) {
      // Escape quotes and join with commas
      const processedRow = row.map(cell => {
        const cellText = String(cell);
        // If cell contains quotes, commas or newlines, wrap in quotes and escape quotes
        if (cellText.includes('"') || cellText.includes(',') || cellText.includes('\n')) {
          return '"' + cellText.replace(/"/g, '""') + '"';
        }
        return cellText;
      });

      csvContent += processedRow.join(',') + '\n';
    });

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');

    // Create file name
    const date = new Date().toISOString().slice(0, 10);
    const fullFilename = `${filename}_${date}.csv`;

    // Set up download
    if (navigator.msSaveBlob) {
      // IE 10+
      navigator.msSaveBlob(blob, fullFilename);
    } else {
      // Other browsers
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', fullFilename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
};

// =============================================================================
// BOOTSTRAP COMPONENT INITIALIZATION
// =============================================================================

/**
 * Initialize Bootstrap dropdowns and components
 */
function initBootstrap() {
  if (typeof bootstrap !== 'undefined') {
    const dropdownElementList = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));

    const dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
      return new bootstrap.Dropdown(dropdownToggleEl);
    });

  } else {
    console.error('Bootstrap JS not loaded, dropdowns will not work!');
  }
}

/**
 * Setup dropdown enhancement features
 * @param {string} dropdownId - ID of the dropdown element
 */
function setupDropdownEnhancements(dropdownId) {
  const dropdownElement = document.getElementById(dropdownId);
  if (dropdownElement) {
    dropdownElement.addEventListener('shown.bs.dropdown', function(e) {
      // Future enhancement code can go here
    });
  }
}

// =============================================================================
// AUTHENTICATION MANAGEMENT
// =============================================================================

/**
 * Clear authentication data from local storage
 */
function clearAuthData() {
  localStorage.removeItem('authToken');
  localStorage.removeItem('refreshToken');
}

/**
 * Validate a JWT token
 * @param {string} token - The JWT token to validate
 * @returns {boolean} Whether the token is valid
 */
function isValidToken(token) {
  if (!token) return false;

  try {
    const parts = token.split('.');
    if (parts.length !== 3) return false;

    const payload = JSON.parse(atob(parts[1]));
    const now = Math.floor(Date.now() / 1000);

    if (payload.exp && payload.exp < now) return false;
    return true;
  } catch (e) {
    console.error('Token validation error:', e);
    return false;
  }
}

/**
 * Check if user is authenticated for current page
 * @returns {boolean} Authentication status
 */
function checkAuth() {
  const token = localStorage.getItem('authToken');
  const currentPath = window.location.pathname;
  const publicPaths = ['/login/', '/api/'];
  const isPublicPath = publicPaths.some(path => currentPath.includes(path));

  if (!isPublicPath && !isValidToken(token)) {
    clearAuthData();
    window.location.href = '/login/';
    return false;
  }

  return true;
}

/**
 * Update navigation elements based on authentication state
 */
function updateNavAuth() {
  const token = localStorage.getItem('authToken');
  const navLogin = document.getElementById('nav-login');
  const navUserSettings = document.getElementById('nav-user-settings');

  // For development/testing: force show user elements
  if (navLogin) navLogin.style.display = 'none';
  if (navUserSettings) {
    navUserSettings.style.display = 'block';
    navUserSettings.style.visibility = 'visible';
    navUserSettings.classList.remove('d-none');
  }

  // Update home link based on authentication
  const homeLink = document.getElementById('home-link');
  if (homeLink) {
    homeLink.href = token ? '/dashboard/' : '/';
  }

  // Update user information if authenticated
  if (token) {
    setUserInfo();
  }
}

/**
 * Set user information in the UI from the auth token
 */
function setUserInfo() {
  const token = localStorage.getItem('authToken');
  if (!token) return;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));

    // Update user email if element exists
    const userEmail = document.getElementById('user-email');
    if (userEmail && payload.email) {
      userEmail.textContent = payload.email;
    }

    // Update username in dropdown if it exists
    const userDropdownName = document.querySelector('#userDropdown .d-none.d-md-inline-block');
    if (userDropdownName && payload.name) {
      userDropdownName.textContent = payload.name;
    } else if (userDropdownName && payload.email) {
      // If name doesn't exist, use email
      const emailParts = payload.email.split('@');
      userDropdownName.textContent = emailParts[0];
    }
  } catch (e) {
    console.error('Error parsing token:', e);
  }
}

// =============================================================================
// NAVIGATION AND UI MANAGEMENT
// =============================================================================

/**
 * Set the active navigation item based on current URL
 */
function setActiveNavItem() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.sidebar .nav-link');

  navLinks.forEach(link => {
    link.classList.remove('active');
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href) && href !== '/') {
      link.classList.add('active');
    }
  });
}

/**
 * Initialize the sidebar with event listeners
 */
function initSidebar() {
  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebar-toggle');

  // Clean approach: remove any existing event listeners first
  if (sidebarToggle) {
    const newToggle = sidebarToggle.cloneNode(true);
    sidebarToggle.parentNode.replaceChild(newToggle, sidebarToggle);

    // Add proper event listener to the sidebar toggle button
    newToggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();

      // For mobile devices
      if (window.innerWidth < 992) {
        document.querySelector('body').classList.toggle('sidebar-mobile-show');
      }

      toggleSidebar(true);
    });
  }

  // Handle click events for any other sidebar toggle elements
  const toggleElements = document.querySelectorAll('.sidebar-toggle:not(#sidebar-toggle), .js-sidebar-toggle');
  toggleElements.forEach(toggle => {
    const newToggle = toggle.cloneNode(true);
    toggle.parentNode.replaceChild(newToggle, toggle);

    newToggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      toggleSidebar(true);
    });
  });

  // Handle navigation links in the sidebar
  if (sidebar) {
    const newSidebar = sidebar.cloneNode(true);
    sidebar.parentNode.replaceChild(newSidebar, sidebar);

    const updatedSidebar = document.getElementById('sidebar');
    if (updatedSidebar) {
      updatedSidebar.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-link') &&
            !e.target.closest('.sidebar-toggle, .js-sidebar-toggle')) {
          e.stopPropagation();
        }
      });
    }
  }

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', function(event) {
    if (window.innerWidth <= 991.98) {
      const sidebar = document.getElementById('sidebar');
      const isClickInsideSidebar = sidebar && sidebar.contains(event.target);
      const isClickOnToggle = event.target.closest('#sidebar-toggle') ||
                             event.target.closest('.sidebar-toggle') ||
                             event.target.closest('.js-sidebar-toggle');

      if (!isClickInsideSidebar && !isClickOnToggle &&
          sidebar && sidebar.classList.contains('show')) {
        closeSidebar();
      }
    }
  });
}

/**
 * Handle sidebar transition cleanup
 * @param {HTMLElement} sidebar - The sidebar element
 */
function cleanupSidebarTransition(sidebar) {
  setTimeout(() => {
    sidebar.classList.remove('transitioning');
  }, 300);
}

/**
 * Close the sidebar (mobile view)
 */
function closeSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  sidebar.classList.add('transitioning');
  sidebar.classList.remove('show');

  // Remove overlay
  const overlay = document.querySelector('.sidebar-overlay');
  if (overlay) {
    overlay.style.opacity = '0';
    setTimeout(() => {
      if (overlay && overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
      }
    }, 300);
  }

  cleanupSidebarTransition(sidebar);
}

/**
 * Open the sidebar (mobile view)
 */
function openSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  sidebar.classList.add('transitioning');
  sidebar.classList.add('show');

  // Add overlay for mobile
  if (window.innerWidth <= 991.98) {
    const existingOverlay = document.querySelector('.sidebar-overlay');
    if (existingOverlay) {
      existingOverlay.parentNode.removeChild(existingOverlay);
    }

    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.style.opacity = '0';

    overlay.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      closeSidebar();
    });

    document.body.appendChild(overlay);

    setTimeout(() => {
      overlay.style.opacity = '1';
    }, 10);
  }

  cleanupSidebarTransition(sidebar);
}

/**
 * Toggle the sidebar between open/closed states
 * @param {boolean} forceToggle - Whether to force toggle regardless of source
 */
function toggleSidebar(forceToggle = false) {
  const sidebar = document.getElementById('sidebar');
  const content = document.querySelector('.content');

  if (!sidebar || !content) {
    console.error('Sidebar or content element not found');
    return;
  }

  if (forceToggle !== true) {
    const activeElement = document.activeElement;
    const isToggleButton = activeElement && (
      activeElement.classList.contains('sidebar-toggle') ||
      activeElement.classList.contains('js-sidebar-toggle') ||
      activeElement.id === 'sidebar-toggle'
    );

    if (!isToggleButton) {
      return;
    }
  }

  // Different behavior for mobile vs desktop
  if (window.innerWidth <= 991.98) {
    if (sidebar.classList.contains('show')) {
      closeSidebar();
    } else {
      openSidebar();
    }
  } else {
    if (!sidebar.classList.contains('transitioning')) {
      sidebar.classList.add('transitioning');

      sidebar.classList.toggle('collapsed');
      content.classList.toggle('expanded');

      if (sidebar.classList.contains('collapsed')) {
        localStorage.setItem('sidebar-collapsed', 'true');
      } else {
        localStorage.removeItem('sidebar-collapsed');
      }

      cleanupSidebarTransition(sidebar);
    }
  }
}

// =============================================================================
// USER ACTIONS AND UI UTILITIES
// =============================================================================



/**
 * Navigate to user profile page
 * @param {Event} event - The click event
 */
function navigateToProfile(event) {
  event.preventDefault();
  const token = localStorage.getItem('authToken');

  if (token && isValidToken(token)) {
    window.location.href = '/accounts/profile/';
  } else {
    clearAuthData();
    window.location.href = '/login/';
  }
}

/**
 * Log out the current user
 */
function logoutUser() {
  const token = localStorage.getItem('authToken');

  if (token) {
    showLoading();
    fetch('/api/v1/token/logout/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ refresh: token })
    })
    .then(response => {
      clearAuthData();
      updateNavAuth();
      window.location.href = '/login/';
    })
    .catch(error => {
      console.error('Logout error:', error);
      clearAuthData();
      updateNavAuth();
      window.location.href = '/login/';
    })
    .finally(() => {
      hideLoading();
    });
  } else {
    window.location.href = '/login/';
  }
}

/**
 * Show the settings modal/page
 */
function showSettings() {
  alert('Settings functionality coming soon!');
}

// =============================================================================
// API UTILITIES
// =============================================================================

/**
 * Make an authenticated API request
 * @param {string} url - The API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise} The fetch promise
 */
// =============================================================================
// GLOBAL FETCH WRAPPER FOR AUTH HANDLING
// =============================================================================
/**
 * Wrapper for fetch that handles 401/403 errors globally
 * @param {string} url - The API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise<Response>} The fetch promise
 */
function fetchWithAuthHandling(url, options = {}) {
  return fetch(url, options)
    .then(response => {
      if (response.status === 401 || response.status === 403) {
        try { clearAuthData(); } catch (e) { /* ignore */ }
        // Use location.replace to prevent back navigation to protected page
        setTimeout(() => { window.location.replace('/login/'); }, 10);
        // Throw to break any further promise chains
        throw new Error('Unauthorized. Redirecting to login.');
      }
      return response;
    })
    .catch(error => {
      // If fetch itself fails (network error), also redirect
      if (error && (error.message && error.message.includes('Unauthorized'))) {
        // Already handled above
        return Promise.reject(error);
      }
      // Optionally, handle other fetch errors here
      return Promise.reject(error);
    });
}

/**
 * Make an authenticated API request with global unauthorized handling
 * @param {string} url - The API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise<Response>} The fetch promise
 */
function makeAuthenticatedRequest(url, options = {}) {
  const token = localStorage.getItem('authToken');

  if (!token || !isValidToken(token)) {
    try { clearAuthData(); } catch (e) { /* ignore */ }
    setTimeout(() => { window.location.href = '/login/'; }, 10);
    return Promise.reject('No valid token');
  }

  const defaultHeaders = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };

  const requestOptions = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers
    }
  };

  return fetchWithAuthHandling(url, requestOptions);
}

// =============================================================================
// APPLICATION INITIALIZATION
// =============================================================================

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Bootstrap components
  initBootstrap();

  // Setup dropdown enhancements
  setupDropdownEnhancements('notificationsDropdown');
  setupDropdownEnhancements('userDropdown');

  // Update navigation and authentication UI
  updateNavAuth();

  // Initialize sidebar with delay to ensure DOM is fully loaded
  setTimeout(() => {
    const sidebar = document.getElementById('sidebar');
    const content = document.querySelector('.content');

    // Restore sidebar state from localStorage
    if (window.innerWidth > 991.98 && localStorage.getItem('sidebar-collapsed') === 'true') {
      sidebar.classList.add('collapsed');
      content.classList.add('expanded');
    }

    initSidebar();
  }, 100);

  // Set active navigation item based on current URL
  setActiveNavItem();

  // Handle window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 991.98) {
      const sidebar = document.getElementById('sidebar');
      const overlay = document.querySelector('.sidebar-overlay');
      if (sidebar && sidebar.classList.contains('show')) {
        closeSidebar();
      }
      if (overlay) overlay.remove();
    }
  });
});

// =============================================================================
// GLOBAL ERROR HANDLING
// =============================================================================

/**
 * Global error handler for unhandled promise rejections
 */
window.addEventListener('unhandledrejection', function(event) {
  console.error('Unhandled promise rejection:', event.reason);
  hideLoading();
});

// =============================================================================
// GLOBAL EXPORTS
// =============================================================================

// Expose SurveyHubDataTable globally for use in other modules
window.SurveyHubDataTable = SurveyHubDataTable;

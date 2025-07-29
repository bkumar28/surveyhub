// =============================================================================
// SURVEY STATUS MAPPING UTILITY
// =============================================================================
/**
 * Map survey status code to display string or badge class
 * @param {string} status - The status code (e.g., 'A', 'D', 'ACTIVE', 'DRAFT', etc.)
 * @returns {string} The mapped status string (e.g., 'ACTIVE', 'DRAFT', etc.)
 */
function mapSurveyStatus(status) {
  if (!status) return '';
  const normalized = String(status).toUpperCase();
  switch (normalized) {
    case 'A':
    case 'ACTIVE':
      return 'ACTIVE';
    case 'D':
    case 'DRAFT':
      return 'DRAFT';
    case 'C':
    case 'CLOSED':
      return 'CLOSED';
    case 'E':
    case 'EXPIRED':
      return 'EXPIRED';
    case 'P':
    case 'PAUSED':
      return 'PAUSED';
    case 'AR':
    case 'ARCHIVED':
      return 'ARCHIVED';
    case 'COMPLETED':
      return 'COMPLETED';
    default:
      return normalized;
  }
}
  // Defensive renderSurveys utility to avoid forEach errors
  function renderSurveys(surveys) {
    if (!Array.isArray(surveys)) {
      window.handleFetchError('Survey data is not an array.', 'surveys');
      surveys = [];
    }
    // Example: render to table or DOM as needed
    // surveys.forEach(...)
    // (You can replace this with your actual rendering logic)
  }

// surveys-list.js: Handles survey table, modal, and API interactions
// Uses window.getCookie from app.js for CSRF and cookie utilities



document.addEventListener('DOMContentLoaded', function() {
  const token = localStorage.getItem('authToken');

  // Reset form and validation state when modal is closed
  document.getElementById('createSurveyModal').addEventListener('hidden.bs.modal', function () {
    document.getElementById('createSurveyForm').reset();
    document.getElementById('surveyTitle').classList.remove('is-invalid');
  });
  document.getElementById('createSurveyModal').addEventListener('hidden.bs.modal', function () {
    window.resetFormAndValidation(document.getElementById('createSurveyForm'), ['surveyTitle']);
  });


  // Initialize DataTable with server-side processing for API pagination
  const table = $('#surveyTable').DataTable({
    serverSide: true,
    processing: true,
    ajax: function(data, callback, settings) {
      if (!token) {
        window.showError("Authentication required");
        callback({ data: [], recordsTotal: 0, recordsFiltered: 0 });
        return;
      }
      window.showLoading();
      // Calculate page number for API (DataTables uses start/length)
      const page = Math.floor(data.start / data.length) + 1;
      const pageSize = data.length;
      const url = `${window.API_BASE_URL}/api/v1/surveys/?page=${page}&page_size=${pageSize}`;
      fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(response => {
        window.hideLoading();
        if (!response.ok) {
          window.handleFetchError(response, 'surveys');
          callback({ data: [], recordsTotal: 0, recordsFiltered: 0 });
          return null;
        }
        return response.json();
      })
      .then(response => {
        if (!response) return;
        const dataObj = response.data || response;
        const results = Array.isArray(dataObj.results) ? dataObj.results : [];
        const surveyData = results.map(survey => ({
          "id": survey.id,
          "title": survey.title,
          "description": survey.description,
          "created_at": survey.created_at,
          "status": mapSurveyStatus(survey.status),
          "responses": survey.response_count || 0,
          "actions": ""
        }));
        callback({
          data: surveyData,
          recordsTotal: dataObj.count || surveyData.length,
          recordsFiltered: dataObj.count || surveyData.length
        });
      })
      .catch(error => {
        window.hideLoading();
        window.handleFetchError(error, 'surveys');
        callback({ data: [], recordsTotal: 0, recordsFiltered: 0 });
      });
    },
    columns: [
      { data: "title", render: function(data, type, row) {
          if (type === 'display') {
            return `<strong class="text-truncate d-block" style="max-width:200px;"><a href="/surveys/${row.id}/" class="text-dark">${data}</a></strong>
                    ${row.description ? `<div class="small text-muted text-truncate" style="max-width:200px;">${row.description}</div>` : ''}`;
          }
          return data;
        }
      },
      { data: "created_at", render: function(data, type, row) {
          if (type === 'display' && data) {
            const date = new Date(data);
            const options = { year: 'numeric', month: 'short', day: 'numeric' };
            return `<span class="text-muted">${date.toLocaleDateString(undefined, options)}</span>`;
          }
          return data;
        }
      },
      { data: "status", orderable: false, className: "text-center", render: function(data, type, row) {
          if (type === 'display') {
            let badgeClass = "bg-secondary";
            if (data === "ACTIVE") badgeClass = "bg-success";
            if (data === "DRAFT") badgeClass = "bg-warning";
            if (data === "EXPIRED") badgeClass = "bg-danger";
            return `<span class="badge ${badgeClass} rounded-pill px-3 py-2">${data}</span>`;
          }
          return data;
        }
      },
      { data: "responses", className: "text-center", render: function(data, type, row) {
          if (type === 'display') {
            return `<span class="badge bg-info">${data}</span>`;
          }
          return data;
        }
      },
      { data: "actions", orderable: false, className: "text-end", render: function(data, type, row) {
          if (type === 'display') {
            return `<div class="btn-group" role="group">
                <button class="btn btn-sm btn-outline-primary" title="View" onclick="viewSurvey('${row.id}')"><i class="bi bi-eye"></i></button>
                <button class="btn btn-sm btn-outline-success" title="Edit" onclick="editSurvey('${row.id}')"><i class="bi bi-pencil"></i></button>
                <button class="btn btn-sm btn-outline-danger" title="Delete" onclick="deleteSurvey('${row.id}')"><i class="bi bi-trash"></i></button>
              </div>`;
          }
          return data;
        }
      }
    ],
    order: [[1, 'desc']],
    pageLength: 10,
    lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
    dom: '<"row mb-2"<"col-sm-6"l><"col-sm-6 text-end"f>>rt<"row mt-2"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7 text-end"p>>',
    pagingType: "simple_numbers",
    drawCallback: function() {
      // Re-initialize tooltips for new buttons
      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        if (!tooltipTriggerEl._tooltip) {
          tooltipTriggerEl._tooltip = new bootstrap.Tooltip(tooltipTriggerEl);
        }
      });
    },
    responsive: true
  });

  // showError and showSuccess are now global (from app.js)

  document.addEventListener('click', function(e) {
    if (e.target.closest('.edit-survey')) {
      e.preventDefault();
      const surveyId = e.target.closest('.edit-survey').dataset.id;
      window.location.href = `/surveys/${surveyId}/edit/`;
    }
    if (e.target.closest('.delete-survey')) {
      e.preventDefault();
      const surveyId = e.target.closest('.delete-survey').dataset.id;
      deleteSurvey(surveyId);
    }
  });

  window.viewSurvey = function(surveyId) {
    window.location.href = `/surveys/${surveyId}/`;
  };

  window.editSurvey = function(surveyId) {
    window.location.href = `/surveys/${surveyId}/edit/`;
  };

  window.deleteSurvey = function(surveyId) {
    if (confirm('Are you sure you want to delete this survey?')) {
      fetch(`${window.API_BASE_URL}/api/v1/surveys/${surveyId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'X-CSRFToken': window.getCookie('csrftoken')
        }
      })
      .then(response => {
        if (!response.ok) {
          if (response.status === 403) {
            throw new Error('You do not have permission to delete this survey');
          } else if (response.status === 404) {
            throw new Error('Survey not found');
          } else {
            throw new Error('Failed to delete survey');
          }
        }
        showSuccess('Survey deleted successfully');
        fetchSurveys();
      })
      .catch(error => {
        showError(`Error: ${error.message}`);
      });
    }
  };

  const createSurveyBtn = document.getElementById('createSurveyBtn');
  if (createSurveyBtn) {
    createSurveyBtn.addEventListener('click', function() {
      const titleInput = document.getElementById('surveyTitle');
      const title = titleInput.value.trim();
      const description = document.getElementById('surveyDescription').value.trim();
      const status = document.getElementById('surveyStatus').value;
      const startDate = document.getElementById('surveyStartDate').value;
      const endDate = document.getElementById('surveyEndDate').value;
      const isPublic = document.getElementById('surveyIsPublic').checked;
      titleInput.classList.remove('is-invalid');
      let isValid = true;
      if (!title) {
        titleInput.classList.add('is-invalid');
        isValid = false;
      }
      if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
        showError('End date must be after start date');
        isValid = false;
      }
      if (!isValid) {
        return;
      }
      const statusCode = status === 'ACTIVE' ? 'A' : status === 'DRAFT' ? 'D' : 'A';
      const surveyData = {
        title,
        description,
        status: statusCode,
        is_public: isPublic,
        visibility: isPublic ? 'PU' : 'PR',
        allow_multiple_responses: false,
        show_progress_bar: true,
        thank_you_message: "Thank you for your response!"
      };
      if (startDate) surveyData.start_date = startDate;
      if (endDate) surveyData.end_date = endDate;
      const submitBtn = document.getElementById('createSurveyBtn');
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating...';
      fetch(`${window.API_BASE_URL}/api/v1/surveys/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'X-CSRFToken': window.getCookie('csrftoken')
        },
        body: JSON.stringify(surveyData)
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => {
            throw new Error(JSON.stringify(err));
          });
        }
        return response.json();
      })
      .then(data => {
        const modal = bootstrap.Modal.getInstance(document.getElementById('createSurveyModal'));
        modal.hide();
        document.getElementById('createSurveyForm').reset();
        showSuccess("Survey created successfully!");
        fetchSurveys();
      })
      .catch(error => {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.message) {
            showError(errorData.message);
          } else if (errorData.detail) {
            showError(errorData.detail);
          } else {
            const fieldErrors = [];
            for (const [field, errors] of Object.entries(errorData)) {
              if (Array.isArray(errors)) {
                fieldErrors.push(`${field}: ${errors.join(', ')}`);
              }
            }
            if (fieldErrors.length > 0) {
              showError(fieldErrors.join('<br>'));
            } else {
              showError("Error creating survey. Please check your inputs and try again.");
            }
          }
        } catch (e) {
          showError("Error creating survey. Please try again.");
        }
      })
      .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      });
    });
  }
});

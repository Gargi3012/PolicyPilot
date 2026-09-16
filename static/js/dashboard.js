/**
 * Policy Impact Simulator - Dashboard JavaScript
 * Handles dashboard interactions, data visualization, and user interface functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // Global variables
    let charts = {};
    let dashboardData = {};
    
    // Initialize dashboard
    initDashboard();

    /**
     * Initialize dashboard functionality
     */
    function initDashboard() {
        setupEventListeners();
        loadDashboardData();
        initializeCharts();
        setupTableFunctionality();
        setupPolicyComparison();
    }

    /**
     * Setup event listeners for dashboard interactions
     */
    function setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(handleSearch, 300));
        }

        // Sector filter
        const sectorFilter = document.getElementById('sectorFilter');
        if (sectorFilter) {
            sectorFilter.addEventListener('change', handleSectorFilter);
        }

        // Export buttons
        setupExportButtons();

        // Refresh data button
        const refreshBtn = document.getElementById('refreshData');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', refreshDashboardData);
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', handleKeyboardShortcuts);
    }

    /**
     * Load dashboard data from server
     */
    function loadDashboardData() {
        showLoading();
        
        // In a real implementation, this would fetch from an API
        // For now, we'll use the data already loaded in the template
        const policiesTable = document.getElementById('policiesTable');
        if (policiesTable) {
            const rows = policiesTable.querySelectorAll('tbody tr');
            dashboardData.policies = Array.from(rows).map(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 1) {
                    return {
                        name: cells[0].textContent.trim(),
                        sector: cells[1].textContent.trim(),
                        region: cells[2].textContent.trim(),
                        change: parseFloat(cells[3].textContent.replace('%', '')) || 0,
                        gdpImpact: parseFloat(cells[4].textContent.replace('%', '')) || 0,
                        inflationImpact: parseFloat(cells[5].textContent.replace('pp', '')) || 0,
                        unemploymentImpact: parseFloat(cells[6].textContent.replace('pp', '')) || 0
                    };
                }
                return null;
            }).filter(policy => policy !== null);
        }
        
        hideLoading();
    }

    /**
     * Initialize charts on the dashboard
     */
    function initializeCharts() {
        // Only initialize charts if we have data
        if (!dashboardData.policies || dashboardData.policies.length === 0) {
            return;
        }

        // Sector distribution chart
        initSectorChart();
        
        // Impact distribution chart
        initImpactChart();
        
        // Trend chart (if element exists)
        initTrendChart();
    }

    /**
     * Initialize sector distribution chart
     */
    function initSectorChart() {
        const sectorChartCanvas = document.getElementById('sectorChart');
        if (!sectorChartCanvas) return;

        const sectorCounts = {};
        dashboardData.policies.forEach(policy => {
            const sector = policy.sector.replace(/[^\w\s]/gi, '').trim();
            sectorCounts[sector] = (sectorCounts[sector] || 0) + 1;
        });

        const ctx = sectorChartCanvas.getContext('2d');
        charts.sectorChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(sectorCounts),
                datasets: [{
                    data: Object.values(sectorCounts),
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} policies (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 1000
                }
            }
        });
    }

    /**
     * Initialize impact distribution chart
     */
    function initImpactChart() {
        const impactChartCanvas = document.getElementById('impactChart');
        if (!impactChartCanvas) return;

        const gdpImpacts = dashboardData.policies.map(p => p.gdpImpact).filter(val => !isNaN(val));
        const inflationImpacts = dashboardData.policies.map(p => p.inflationImpact).filter(val => !isNaN(val));
        const unemploymentImpacts = dashboardData.policies.map(p => p.unemploymentImpact).filter(val => !isNaN(val));

        if (gdpImpacts.length === 0) return;

        const avgGDP = gdpImpacts.reduce((a, b) => a + b, 0) / gdpImpacts.length;
        const avgInflation = inflationImpacts.reduce((a, b) => a + b, 0) / inflationImpacts.length;
        const avgUnemployment = unemploymentImpacts.reduce((a, b) => a + b, 0) / unemploymentImpacts.length;

        const ctx = impactChartCanvas.getContext('2d');
        charts.impactChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['GDP Impact (%)', 'Inflation Impact (pp)', 'Unemployment Impact (pp)'],
                datasets: [{
                    label: 'Average Impact',
                    data: [avgGDP, avgInflation, avgUnemployment],
                    backgroundColor: [
                        avgGDP >= 0 ? '#28a745' : '#dc3545',
                        Math.abs(avgInflation) < 0.5 ? '#17a2b8' : '#ffc107',
                        avgUnemployment <= 0 ? '#28a745' : '#dc3545'
                    ],
                    borderColor: [
                        avgGDP >= 0 ? '#1e7e34' : '#bd2130',
                        Math.abs(avgInflation) < 0.5 ? '#117a8b' : '#d39e00',
                        avgUnemployment <= 0 ? '#1e7e34' : '#bd2130'
                    ],
                    borderWidth: 2,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(2);
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            afterLabel: function(context) {
                                const interpretations = [
                                    avgGDP > 1 ? 'Strong positive impact' : avgGDP > 0 ? 'Positive impact' : 'Negative impact',
                                    Math.abs(avgInflation) < 0.5 ? 'Stable inflation' : 'Inflation concern',
                                    avgUnemployment <= 0 ? 'Job creation expected' : 'Potential job losses'
                                ];
                                return interpretations[context.dataIndex];
                            }
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutBounce'
                }
            }
        });
    }

    /**
     * Initialize trend chart if data is available
     */
    function initTrendChart() {
        const trendChartCanvas = document.getElementById('trendChart');
        if (!trendChartCanvas) return;

        // This would typically show trends over time
        // For demo purposes, we'll create a simple trend visualization
        const ctx = trendChartCanvas.getContext('2d');
        charts.trendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Policy Simulations',
                    data: [2, 4, 3, 5, 6, 4],
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    /**
     * Setup table functionality (search, filter, sort)
     */
    function setupTableFunctionality() {
        const table = document.getElementById('policiesTable');
        if (!table) return;

        // Make table sortable
        setupTableSort(table);
        
        // Setup row click handlers
        setupTableRowHandlers(table);
    }

    /**
     * Setup table sorting functionality
     */
    function setupTableSort(table) {
        const headers = table.querySelectorAll('thead th');
        headers.forEach((header, index) => {
            if (index < headers.length - 1) { // Exclude actions column
                header.style.cursor = 'pointer';
                header.addEventListener('click', () => sortTable(table, index));
                
                // Add sort icon
                const icon = document.createElement('i');
                icon.className = 'fas fa-sort ms-1 text-muted';
                header.appendChild(icon);
            }
        });
    }

    /**
     * Sort table by column
     */
    function sortTable(table, columnIndex) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const header = table.querySelectorAll('thead th')[columnIndex];
        const icon = header.querySelector('i');
        
        // Determine sort direction
        const isAscending = !header.classList.contains('sort-desc');
        
        // Reset all sort icons
        table.querySelectorAll('thead th i').forEach(i => {
            i.className = 'fas fa-sort ms-1 text-muted';
        });
        
        // Update current sort icon
        icon.className = `fas fa-sort-${isAscending ? 'up' : 'down'} ms-1 text-primary`;
        header.classList.toggle('sort-desc', !isAscending);
        
        // Sort rows
        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex].textContent.trim();
            const bValue = b.cells[columnIndex].textContent.trim();
            
            // Handle numeric values
            if (!isNaN(parseFloat(aValue)) && !isNaN(parseFloat(bValue))) {
                return isAscending ? 
                    parseFloat(aValue) - parseFloat(bValue) : 
                    parseFloat(bValue) - parseFloat(aValue);
            }
            
            // Handle text values
            return isAscending ? 
                aValue.localeCompare(bValue) : 
                bValue.localeCompare(aValue);
        });
        
        // Re-append sorted rows
        rows.forEach(row => tbody.appendChild(row));
    }

    /**
     * Setup table row click handlers
     */
    function setupTableRowHandlers(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            // Skip empty state row
            if (row.cells.length === 1) return;
            
            row.addEventListener('click', function(e) {
                // Don't trigger on button clicks
                if (e.target.closest('.btn')) return;
                
                // Highlight selected row
                table.querySelectorAll('tbody tr').forEach(r => r.classList.remove('table-primary'));
                this.classList.add('table-primary');
                
                // Extract policy ID and navigate (if view button exists)
                const viewBtn = this.querySelector('a[href*="results"]');
                if (viewBtn) {
                    window.location.href = viewBtn.href;
                }
            });
        });
    }

    /**
     * Handle search functionality
     */
    function handleSearch(event) {
        const searchTerm = event.target.value.toLowerCase();
        filterTable(searchTerm, null);
    }

    /**
     * Handle sector filter
     */
    function handleSectorFilter(event) {
        const sectorFilter = event.target.value;
        filterTable(null, sectorFilter);
    }

    /**
     * Filter table based on search term and sector
     */
    function filterTable(searchTerm = null, sectorFilter = null) {
        const table = document.getElementById('policiesTable');
        if (!table) return;

        const searchInput = document.getElementById('searchInput');
        const sectorSelect = document.getElementById('sectorFilter');
        
        const currentSearch = searchTerm !== null ? searchTerm : 
                            (searchInput ? searchInput.value.toLowerCase() : '');
        const currentSector = sectorFilter !== null ? sectorFilter : 
                            (sectorSelect ? sectorSelect.value : '');

        const rows = table.querySelectorAll('tbody tr');
        let visibleCount = 0;

        rows.forEach(row => {
            // Skip empty state row
            if (row.cells.length === 1) return;

            const policyName = row.cells[0].textContent.toLowerCase();
            const sectorBadge = row.cells[1].querySelector('.badge');
            const sector = sectorBadge ? sectorBadge.textContent.trim() : '';

            const matchesSearch = !currentSearch || policyName.includes(currentSearch);
            const matchesSector = !currentSector || sector === currentSector;

            if (matchesSearch && matchesSector) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        // Show/hide no results message
        updateNoResultsMessage(table, visibleCount);
    }

    /**
     * Update no results message
     */
    function updateNoResultsMessage(table, visibleCount) {
        let noResultsRow = table.querySelector('.no-results-row');
        
        if (visibleCount === 0) {
            if (!noResultsRow) {
                noResultsRow = document.createElement('tr');
                noResultsRow.className = 'no-results-row';
                noResultsRow.innerHTML = `
                    <td colspan="9" class="text-center py-4 text-muted">
                        <i class="fas fa-search fa-2x mb-2"></i>
                        <p>No policies match your search criteria</p>
                    </td>
                `;
                table.querySelector('tbody').appendChild(noResultsRow);
            }
            noResultsRow.style.display = '';
        } else if (noResultsRow) {
            noResultsRow.style.display = 'none';
        }
    }

    /**
     * Setup policy comparison functionality
     */
    function setupPolicyComparison() {
        const compareForm = document.getElementById('compareForm');
        if (!compareForm) return;

        const checkboxes = compareForm.querySelectorAll('.compare-checkbox');
        const compareBtn = document.getElementById('compareBtn');

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateCompareButton);
        });

        function updateCompareButton() {
            const selectedCount = compareForm.querySelectorAll('.compare-checkbox:checked').length;
            if (compareBtn) {
                compareBtn.disabled = selectedCount < 2;
                compareBtn.innerHTML = `<i class="fas fa-balance-scale me-1"></i>Compare Selected (${selectedCount})`;
            }
        }
    }

    /**
     * Setup export buttons
     */
    function setupExportButtons() {
        // Export chart as image
        document.addEventListener('click', function(e) {
            if (e.target.matches('.export-chart')) {
                const chartType = e.target.dataset.chart;
                if (charts[chartType]) {
                    exportChartAsImage(charts[chartType], `${chartType}.png`);
                }
            }
        });

        // Export table as CSV
        const exportCsvBtn = document.getElementById('exportCsv');
        if (exportCsvBtn) {
            exportCsvBtn.addEventListener('click', exportTableAsCsv);
        }
    }

    /**
     * Export chart as image
     */
    function exportChartAsImage(chart, filename) {
        const link = document.createElement('a');
        link.download = filename;
        link.href = chart.toBase64Image();
        link.click();
    }

    /**
     * Export table as CSV
     */
    function exportTableAsCsv() {
        const table = document.getElementById('policiesTable');
        if (!table) return;

        const csv = [];
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => 
            th.textContent.trim().replace(/[^\w\s]/gi, '')
        );
        csv.push(headers.join(','));

        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            if (row.style.display !== 'none' && row.cells.length > 1) {
                const rowData = Array.from(row.cells).slice(0, -1).map(cell => {
                    let text = cell.textContent.trim();
                    // Clean up text
                    text = text.replace(/[^\w\s\-\.%]/gi, '');
                    return `"${text}"`;
                });
                csv.push(rowData.join(','));
            }
        });

        const csvContent = csv.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'policy_data.csv';
        link.click();
        
        window.URL.revokeObjectURL(url);
    }

    /**
     * Handle keyboard shortcuts
     */
    function handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + F: Focus search
        if ((event.ctrlKey || event.metaKey) && event.key === 'f') {
            event.preventDefault();
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.focus();
            }
        }

        // Escape: Clear search
        if (event.key === 'Escape') {
            const searchInput = document.getElementById('searchInput');
            if (searchInput && searchInput === document.activeElement) {
                searchInput.value = '';
                filterTable('', null);
            }
        }
    }

    /**
     * Refresh dashboard data
     */
    function refreshDashboardData() {
        showLoading();
        
        // Simulate data refresh
        setTimeout(() => {
            loadDashboardData();
            
            // Update charts
            Object.values(charts).forEach(chart => {
                chart.update();
            });
            
            hideLoading();
            showNotification('Dashboard data refreshed successfully', 'success');
        }, 1000);
    }

    /**
     * Show loading indicator
     */
    function showLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
        }
        
        // Add loading class to dashboard
        document.body.classList.add('loading');
    }

    /**
     * Hide loading indicator
     */
    function hideLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        
        // Remove loading class from dashboard
        document.body.classList.remove('loading');
    }

    /**
     * Show notification
     */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 1060; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    /**
     * Debounce function to limit function calls
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Cleanup function for when page is unloaded
     */
    window.addEventListener('beforeunload', function() {
        // Cleanup charts
        Object.values(charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
    });

    // Make some functions globally available
    window.dashboardUtils = {
        refreshData: refreshDashboardData,
        exportChart: exportChartAsImage,
        exportCsv: exportTableAsCsv,
        showNotification: showNotification
    };
});

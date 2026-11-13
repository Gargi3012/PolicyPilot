/**
 * Indian Policy Impact Simulator - Professional Dashboard Module
 * Handles table search, sorting, filtering, and chart visualizations
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    let charts = {};
    let dashboardData = {};

    initDashboard();

    function initDashboard() {
        setupEventListeners();
        loadDashboardData();
        initializeCharts();
        setupTableFunctionality();
        setupPolicyComparison();
    }

    function setupEventListeners() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(handleSearch, 200));
        }

        const sectorFilter = document.getElementById('sectorFilter');
        if (sectorFilter) {
            sectorFilter.addEventListener('change', handleSectorFilter);
        }

        const refreshBtn = document.getElementById('refreshData');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                window.location.reload();
            });
        }
    }

    function loadDashboardData() {
        const policiesTable = document.getElementById('policiesTable');
        if (policiesTable) {
            const rows = policiesTable.querySelectorAll('tbody tr');
            dashboardData.policies = Array.from(rows).map(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 4) {
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
    }

    function initializeCharts() {
        if (!dashboardData.policies || dashboardData.policies.length === 0) {
            return;
        }
        initSectorChart();
        initImpactChart();
    }

    function initSectorChart() {
        const sectorChartCanvas = document.getElementById('sectorChart');
        if (!sectorChartCanvas) return;

        // Count policies per sector
        const sectorCounts = {};
        dashboardData.policies.forEach(policy => {
            const sector = policy.sector.replace(/[^\w\s]/gi, '').trim();
            if (sector) {
                sectorCounts[sector] = (sectorCounts[sector] || 0) + 1;
            }
        });

        if (Object.keys(sectorCounts).length === 0) return;

        // Destroy existing instance if present
        if (window.sectorChartInstance) {
            window.sectorChartInstance.destroy();
        }

        const ctx = sectorChartCanvas.getContext('2d');
        const colors = [
            '#16834A', // Emerald
            '#0D9488', // Teal
            '#2563EB', // Blue-slate
            '#D97706', // Amber
            '#15803D', // Forest
            '#059669', // Mint
            '#475569', // Slate
            '#64746A'  // Charcoal
        ];

        window.sectorChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(sectorCounts),
                datasets: [{
                    data: Object.values(sectorCounts),
                    backgroundColor: colors.slice(0, Object.keys(sectorCounts).length),
                    borderWidth: 2,
                    borderColor: '#FFFFFF',
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 14,
                            usePointStyle: true,
                            boxWidth: 8,
                            font: {
                                size: 12,
                                weight: '500'
                            },
                            color: '#1B2B22'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#FFFFFF',
                        titleColor: '#1B2B22',
                        bodyColor: '#64746A',
                        borderColor: '#E3EBE5',
                        borderWidth: 1,
                        padding: 10,
                        boxPadding: 4,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                                return ` ${context.label}: ${context.parsed} (${pct}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

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

        // Destroy existing instance if present
        if (window.impactChartInstance) {
            window.impactChartInstance.destroy();
        }

        const ctx = impactChartCanvas.getContext('2d');
        window.impactChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Avg GDP Impact (%)', 'Avg Inflation (pp)', 'Avg Unemployment (pp)'],
                datasets: [{
                    label: 'Mean Projected Impact',
                    data: [
                        parseFloat(avgGDP.toFixed(2)),
                        parseFloat(avgInflation.toFixed(2)),
                        parseFloat(avgUnemployment.toFixed(2))
                    ],
                    backgroundColor: [
                        avgGDP >= 0 ? '#16834A' : '#DC2626',
                        '#D97706',
                        avgUnemployment <= 0 ? '#16834A' : '#DC2626'
                    ],
                    borderRadius: 6,
                    maxBarThickness: 50
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#EEF4F0',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#64746A',
                            font: { size: 11 }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#1B2B22',
                            font: { size: 12, weight: '600' }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#FFFFFF',
                        titleColor: '#1B2B22',
                        bodyColor: '#64746A',
                        borderColor: '#E3EBE5',
                        borderWidth: 1,
                        padding: 10,
                        callbacks: {
                            label: function(context) {
                                const unit = context.dataIndex === 0 ? '%' : 'pp';
                                return ` ${context.parsed.y > 0 ? '+' : ''}${context.parsed.y}${unit}`;
                            }
                        }
                    }
                }
            }
        });
    }

    function setupTableFunctionality() {
        const table = document.getElementById('policiesTable');
        if (!table) return;

        setupTableSort(table);
    }

    function setupTableSort(table) {
        const headers = table.querySelectorAll('thead th');
        headers.forEach((header, index) => {
            if (index < headers.length - 1) { // Exclude actions column
                header.style.cursor = 'pointer';
                header.addEventListener('click', () => sortTable(table, index));
            }
        });
    }

    function sortTable(table, columnIndex) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr:not(.no-results-row)'));
        const header = table.querySelectorAll('thead th')[columnIndex];
        if (!header) return;

        const isAscending = !header.classList.contains('sort-desc');

        table.querySelectorAll('thead th').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
        });

        header.classList.toggle('sort-desc', !isAscending);
        header.classList.toggle('sort-asc', isAscending);

        rows.sort((a, b) => {
            const aCell = a.cells[columnIndex];
            const bCell = b.cells[columnIndex];
            if (!aCell || !bCell) return 0;

            const aText = aCell.textContent.trim();
            const bText = bCell.textContent.trim();

            const aNum = parseFloat(aText.replace(/[^0-9.-]/g, ''));
            const bNum = parseFloat(bText.replace(/[^0-9.-]/g, ''));

            if (!isNaN(aNum) && !isNaN(bNum) && !aText.includes('/')) {
                return isAscending ? aNum - bNum : bNum - aNum;
            }
            return isAscending ? aText.localeCompare(bText) : bText.localeCompare(aText);
        });

        rows.forEach(row => tbody.appendChild(row));
    }

    function handleSearch(event) {
        const term = event.target.value.toLowerCase().trim();
        filterTable(term, null);
    }

    function handleSectorFilter(event) {
        const sector = event.target.value;
        filterTable(null, sector);
    }

    function filterTable(searchTerm = null, sectorFilter = null) {
        const table = document.getElementById('policiesTable');
        if (!table) return;

        const searchInput = document.getElementById('searchInput');
        const sectorSelect = document.getElementById('sectorFilter');

        const currentSearch = searchTerm !== null ? searchTerm : (searchInput ? searchInput.value.toLowerCase().trim() : '');
        const currentSector = sectorFilter !== null ? sectorFilter : (sectorSelect ? sectorSelect.value : '');

        const rows = table.querySelectorAll('tbody tr:not(.no-results-row)');
        let visibleCount = 0;

        rows.forEach(row => {
            if (row.cells.length < 3) return;

            const policyName = row.cells[0].textContent.toLowerCase();
            const sector = row.cells[1].textContent.trim();

            const matchesSearch = !currentSearch || policyName.includes(currentSearch);
            const matchesSector = !currentSector || sector.toLowerCase().includes(currentSector.toLowerCase());

            if (matchesSearch && matchesSector) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        updateTableCount(visibleCount, rows.length);
        updateNoResultsMessage(table, visibleCount);
    }

    function updateTableCount(visible, total) {
        const counter = document.getElementById('tableCounter');
        if (counter) {
            counter.textContent = `Showing ${visible} of ${total} simulations`;
        }
    }

    function updateNoResultsMessage(table, visibleCount) {
        let noResultsRow = table.querySelector('.no-results-row');
        if (visibleCount === 0) {
            if (!noResultsRow) {
                noResultsRow = document.createElement('tr');
                noResultsRow.className = 'no-results-row';
                noResultsRow.innerHTML = `
                    <td colspan="9" class="text-center py-5 text-muted">
                        <i class="fas fa-search fa-2x mb-2 text-secondary opacity-50"></i>
                        <p class="mb-0 fw-semibold">No policy simulations match your filter criteria.</p>
                        <small>Try clearing your search term or sector filter.</small>
                    </td>
                `;
                table.querySelector('tbody').appendChild(noResultsRow);
            }
            noResultsRow.style.display = '';
        } else if (noResultsRow) {
            noResultsRow.style.display = 'none';
        }
    }

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

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
});

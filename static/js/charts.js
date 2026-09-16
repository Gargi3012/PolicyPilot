/**
 * Policy Impact Simulator - Chart Utilities and Configurations
 * Provides common chart configurations and utility functions for data visualization
 */

// Chart.js default configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#495057';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 20;

/**
 * Color schemes for different chart types
 */
const ChartColors = {
    primary: '#007bff',
    secondary: '#6c757d',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8',
    light: '#f8f9fa',
    dark: '#343a40',
    
    // Gradient colors
    gradients: {
        primary: ['#007bff', '#0056b3'],
        success: ['#28a745', '#1e7e34'],
        danger: ['#dc3545', '#bd2130'],
        warning: ['#ffc107', '#d39e00'],
        info: ['#17a2b8', '#117a8b']
    },
    
    // Chart-specific color palettes
    sector: [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ],
    
    impact: {
        positive: '#28a745',
        negative: '#dc3545',
        neutral: '#ffc107'
    }
};

/**
 * Common chart options and configurations
 */
const ChartOptions = {
    /**
     * Default responsive options
     */
    responsive: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#007bff',
                borderWidth: 1,
                cornerRadius: 8,
                displayColors: true
            }
        },
        interaction: {
            intersect: false,
            mode: 'index'
        }
    },

    /**
     * Bar chart specific options
     */
    bar: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                    drawBorder: false
                },
                ticks: {
                    padding: 10
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    padding: 10
                }
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.parsed.y;
                        const suffix = context.dataset.label.includes('%') ? '%' : 
                                     context.dataset.label.includes('pp') ? 'pp' : '';
                        return `${context.dataset.label}: ${value.toFixed(2)}${suffix}`;
                    }
                }
            }
        }
    },

    /**
     * Line chart specific options
     */
    line: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        },
        elements: {
            line: {
                tension: 0.4
            },
            point: {
                radius: 4,
                hoverRadius: 6
            }
        }
    },

    /**
     * Doughnut chart specific options
     */
    doughnut: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',
        plugins: {
            legend: {
                position: 'bottom'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.parsed;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${label}: ${value} (${percentage}%)`;
                    }
                }
            }
        }
    },

    /**
     * Radar chart specific options
     */
    radar: {
        responsive: true,
        maintainAspectRatio: false,
        elements: {
            line: {
                borderWidth: 3
            }
        },
        scales: {
            r: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                },
                pointLabels: {
                    font: {
                        size: 12
                    }
                }
            }
        }
    }
};

/**
 * Chart utility functions
 */
const ChartUtils = {
    /**
     * Create a gradient background for charts
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     * @param {Array} colors - Array of color stops
     * @param {string} direction - Gradient direction ('vertical' or 'horizontal')
     * @returns {CanvasGradient} - Canvas gradient
     */
    createGradient: function(ctx, colors, direction = 'vertical') {
        const gradient = direction === 'vertical' 
            ? ctx.createLinearGradient(0, 0, 0, 400)
            : ctx.createLinearGradient(0, 0, 400, 0);
        
        colors.forEach((color, index) => {
            gradient.addColorStop(index / (colors.length - 1), color);
        });
        
        return gradient;
    },

    /**
     * Generate colors based on data values (positive/negative)
     * @param {Array} data - Array of numeric values
     * @returns {Array} - Array of colors
     */
    getImpactColors: function(data) {
        return data.map(value => {
            if (value > 0) return ChartColors.impact.positive;
            if (value < 0) return ChartColors.impact.negative;
            return ChartColors.impact.neutral;
        });
    },

    /**
     * Format numbers for chart labels
     * @param {number} value - Numeric value
     * @param {string} type - Type of formatting ('percentage', 'currency', 'number')
     * @returns {string} - Formatted string
     */
    formatValue: function(value, type = 'number') {
        if (typeof value !== 'number') return value;
        
        switch (type) {
            case 'percentage':
                return `${value.toFixed(2)}%`;
            case 'currency':
                return new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD'
                }).format(value);
            case 'decimal':
                return value.toFixed(2);
            default:
                return value.toString();
        }
    },

    /**
     * Create animation configuration
     * @param {number} duration - Animation duration in milliseconds
     * @param {string} easing - Easing function
     * @returns {Object} - Animation configuration
     */
    createAnimation: function(duration = 1000, easing = 'easeOutQuart') {
        return {
            duration: duration,
            easing: easing,
            delay: function(context) {
                return context.dataIndex * 100;
            }
        };
    },

    /**
     * Generate sector distribution chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} sectorData - Sector count data
     */
    createSectorChart: function(canvasId, sectorData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(sectorData),
                datasets: [{
                    data: Object.values(sectorData),
                    backgroundColor: ChartColors.sector,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                ...ChartOptions.doughnut,
                plugins: {
                    ...ChartOptions.doughnut.plugins,
                    title: {
                        display: true,
                        text: 'Policies by Sector',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    },

    /**
     * Generate impact comparison chart
     * @param {string} canvasId - Canvas element ID
     * @param {Array} policies - Policy data array
     */
    createImpactChart: function(canvasId, policies) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const labels = ['GDP Impact', 'Inflation Impact', 'Unemployment Impact', 'Environmental Impact'];
        const data = policies.map(policy => [
            policy.prediction?.gdp_impact || 0,
            policy.prediction?.inflation_impact || 0,
            policy.prediction?.unemployment_impact || 0,
            policy.prediction?.environmental_impact || 0
        ]);

        const datasets = policies.map((policy, index) => ({
            label: policy.name.length > 20 ? policy.name.substring(0, 20) + '...' : policy.name,
            data: data[index],
            backgroundColor: ChartColors.sector[index % ChartColors.sector.length] + '40',
            borderColor: ChartColors.sector[index % ChartColors.sector.length],
            borderWidth: 2,
            pointBackgroundColor: ChartColors.sector[index % ChartColors.sector.length],
            pointBorderColor: '#fff',
            pointBorderWidth: 2
        }));

        return new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: ChartOptions.radar
        });
    },

    /**
     * Generate time series chart for policy impacts over time
     * @param {string} canvasId - Canvas element ID
     * @param {Object} timeData - Time series data
     */
    createTimeSeriesChart: function(canvasId, timeData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: timeData.labels,
                datasets: [
                    {
                        label: 'GDP Impact (%)',
                        data: timeData.gdp,
                        borderColor: ChartColors.success,
                        backgroundColor: ChartColors.success + '20',
                        fill: true
                    },
                    {
                        label: 'Inflation Impact (pp)',
                        data: timeData.inflation,
                        borderColor: ChartColors.warning,
                        backgroundColor: ChartColors.warning + '20',
                        fill: true
                    },
                    {
                        label: 'Unemployment Impact (pp)',
                        data: timeData.unemployment,
                        borderColor: ChartColors.danger,
                        backgroundColor: ChartColors.danger + '20',
                        fill: true
                    }
                ]
            },
            options: {
                ...ChartOptions.line,
                plugins: {
                    ...ChartOptions.line.plugins,
                    title: {
                        display: true,
                        text: 'Policy Impact Over Time',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    },

    /**
     * Create confidence meter chart
     * @param {string} canvasId - Canvas element ID
     * @param {number} confidence - Confidence score (0-1)
     */
    createConfidenceMeter: function(canvasId, confidence) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const confidencePercent = confidence * 100;
        const remainingPercent = 100 - confidencePercent;

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [confidencePercent, remainingPercent],
                    backgroundColor: [
                        confidence > 0.7 ? ChartColors.success : 
                        confidence > 0.5 ? ChartColors.warning : ChartColors.danger,
                        '#e9ecef'
                    ],
                    borderWidth: 0,
                    cutout: '80%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            },
            plugins: [{
                id: 'centerText',
                beforeDraw: function(chart) {
                    const ctx = chart.ctx;
                    const centerX = chart.chartArea.left + (chart.chartArea.right - chart.chartArea.left) / 2;
                    const centerY = chart.chartArea.top + (chart.chartArea.bottom - chart.chartArea.top) / 2;
                    
                    ctx.save();
                    ctx.font = 'bold 24px Arial';
                    ctx.fillStyle = '#495057';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(`${confidencePercent.toFixed(0)}%`, centerX, centerY);
                    ctx.restore();
                }
            }]
        });
    },

    /**
     * Export chart as image
     * @param {Chart} chart - Chart.js instance
     * @param {string} filename - Download filename
     */
    exportChart: function(chart, filename = 'chart.png') {
        const link = document.createElement('a');
        link.download = filename;
        link.href = chart.toBase64Image();
        link.click();
    },

    /**
     * Update chart data with animation
     * @param {Chart} chart - Chart.js instance
     * @param {Object} newData - New data to update
     */
    updateChartData: function(chart, newData) {
        if (newData.labels) {
            chart.data.labels = newData.labels;
        }
        
        if (newData.datasets) {
            chart.data.datasets = newData.datasets;
        }
        
        chart.update('active');
    },

    /**
     * Destroy chart safely
     * @param {Chart} chart - Chart.js instance
     */
    destroyChart: function(chart) {
        if (chart && typeof chart.destroy === 'function') {
            chart.destroy();
        }
    }
};

/**
 * Chart theme configurations
 */
const ChartThemes = {
    light: {
        backgroundColor: '#ffffff',
        textColor: '#495057',
        gridColor: 'rgba(0, 0, 0, 0.1)',
        borderColor: 'rgba(0, 0, 0, 0.125)'
    },
    
    dark: {
        backgroundColor: '#2d3748',
        textColor: '#e2e8f0',
        gridColor: 'rgba(255, 255, 255, 0.1)',
        borderColor: 'rgba(255, 255, 255, 0.125)'
    }
};

/**
 * Apply theme to chart options
 * @param {Object} options - Chart options
 * @param {string} theme - Theme name ('light' or 'dark')
 * @returns {Object} - Updated options
 */
function applyChartTheme(options, theme = 'light') {
    const themeConfig = ChartThemes[theme];
    
    // Update scales colors
    if (options.scales) {
        Object.keys(options.scales).forEach(scaleKey => {
            const scale = options.scales[scaleKey];
            if (scale.grid) {
                scale.grid.color = themeConfig.gridColor;
            }
            if (scale.ticks) {
                scale.ticks.color = themeConfig.textColor;
            }
        });
    }
    
    // Update plugin colors
    if (options.plugins) {
        if (options.plugins.legend && options.plugins.legend.labels) {
            options.plugins.legend.labels.color = themeConfig.textColor;
        }
        
        if (options.plugins.title) {
            options.plugins.title.color = themeConfig.textColor;
        }
    }
    
    return options;
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChartColors, ChartOptions, ChartUtils, ChartThemes, applyChartTheme };
}

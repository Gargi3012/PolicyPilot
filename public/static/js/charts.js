/**
 * Indian Policy Impact Simulator - Professional Chart System
 * Premium Chart.js configurations with White + Sage Green + Emerald Green styling
 */

// Set global Chart.js defaults
if (typeof Chart !== 'undefined') {
    Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.font.weight = 500;
    Chart.defaults.color = '#64746A';
    Chart.defaults.borderColor = '#E3EBE5';
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.padding = 16;
    Chart.defaults.plugins.legend.labels.color = '#1B2B22';
    Chart.defaults.plugins.tooltip.backgroundColor = '#FFFFFF';
    Chart.defaults.plugins.tooltip.titleColor = '#1B2B22';
    Chart.defaults.plugins.tooltip.bodyColor = '#64746A';
    Chart.defaults.plugins.tooltip.borderColor = '#E3EBE5';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.boxPadding = 6;
    Chart.defaults.plugins.tooltip.usePointStyle = true;
}

/**
 * Coordinated Color Palettes for the Design System
 */
const ChartColors = {
    primary: '#16834A',        // Emerald Green
    primaryDark: '#14532D',    // Deep Forest Green
    sage: '#4D7C5D',           // Medium Sage
    lightSage: '#E5F1E8',      // Soft Sage
    slate: '#64746A',          // Muted Charcoal
    dark: '#1B2B22',           // Pine Black
    teal: '#0D9488',           // Teal
    amber: '#D97706',          // Muted Amber
    rose: '#DC2626',           // Crimson / Red
    border: '#E3EBE5',

    // Sector breakdown palette (curated earthy & emerald-compatible tones)
    sector: [
        '#16834A', // Emerald (Energy)
        '#0D9488', // Teal (Healthcare)
        '#2563EB', // Blue-slate (Education)
        '#D97706', // Amber (Transportation)
        '#15803D', // Forest (Agriculture)
        '#059669', // Mint-green (Finance)
        '#475569', // Slate (Technology)
        '#64746A'  // Neutral Charcoal (Manufacturing)
    ],

    impact: {
        positive: '#16834A',
        negative: '#DC2626',
        neutral: '#D97706'
    }
};

/**
 * Standard Chart Configurations
 */
const ChartOptions = {
    doughnut: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 16,
                    usePointStyle: true,
                    boxWidth: 8
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.parsed;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const pct = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                        return ` ${label}: ${value} policies (${pct}%)`;
                    }
                }
            }
        }
    },

    bar: {
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
                    padding: 8,
                    color: '#64746A'
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    padding: 8,
                    color: '#1B2B22',
                    font: {
                        weight: '600'
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    },

    radar: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            r: {
                beginAtZero: true,
                grid: {
                    color: '#E3EBE5'
                },
                angleLines: {
                    color: '#EEF4F0'
                },
                pointLabels: {
                    font: {
                        size: 11,
                        weight: '600'
                    },
                    color: '#1B2B22'
                },
                ticks: {
                    backdropColor: 'transparent',
                    color: '#64746A'
                }
            }
        },
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 16,
                    usePointStyle: true
                }
            }
        }
    }
};

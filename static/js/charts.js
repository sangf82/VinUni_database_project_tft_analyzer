// Chart.js configuration and initialization for TFT Analyzer

// Chart color scheme matching the light green theme
const chartColors = {
    primary: '#28a745',
    secondary: '#40c463',
    success: '#20c997',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#17a2b8',
    light: '#f8f9fa',
    dark: '#343a40',
    gold: '#ffd700',
    silver: '#c0c0c0',
    bronze: '#cd7f32',
    top_4: '#616669',
    other_top: '#4a4d4f'
};

// Global chart defaults
Chart.defaults.color = '#f8f9fa';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.backgroundColor = 'rgba(40, 167, 69, 0.1)';

// Initialize LP History Chart
function initLPChart(lpData) {
    const ctx = document.getElementById('lpChart');
    if (!ctx || !lpData || lpData.length === 0) return;

    const labels = lpData.map(entry => {
        const date = new Date(entry.recorded_at);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    const data = lpData.map(entry => entry.lp_value);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'LP',
                data: data,
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointHoverBackgroundColor: chartColors.secondary,
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 3
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
                    backgroundColor: 'rgba(33, 37, 41, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        title: function(context) {
                            return `Match ${context[0].dataIndex + 1}`;
                        },
                        label: function(context) {
                            return `LP: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6c757d',
                        maxTicksLimit: 8
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6c757d',
                        callback: function(value) {
                            return value + ' LP';
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                point: {
                    hoverRadius: 8
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Initialize Placement Distribution Chart
function initPlacementChart(placementData) {
    const ctx = document.getElementById('placementChart');
    if (!ctx || !placementData) return;

    const labels = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th'];
    const backgroundColors = [
        chartColors.gold,      // 1st place - Gold
        chartColors.silver,    // 2nd place - Silver
        chartColors.bronze,    // 3rd place - Bronze
        chartColors.top_4,   // 4th place - Green
        chartColors.other_top,      // 5th place - Light blue
        chartColors.other_top,   // 6th place - Yellow
        chartColors.other_top,    // 7th place - Red
        chartColors.other_top       // 8th place - Dark
    ];

    const borderColors = backgroundColors.map(color => color);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Matches',
                data: placementData,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2,
                borderRadius: 6,
                borderSkipped: false,
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
                    backgroundColor: 'rgba(33, 37, 41, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        title: function(context) {
                            return `${context[0].label} Place`;
                        },
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((context.parsed.y / total) * 100).toFixed(1) : 0;
                            return `${context.parsed.y} matches (${percentage}%)`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#f8f9fa',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6c757d',
                        stepSize: 1,
                        beginAtZero: true
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeInOutQuart'
            },
            onHover: (event, activeElements, chart) => {
                chart.canvas.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
            }
        }
    });
}

// Initialize Win Rate Donut Chart (optional enhancement)
function initWinRateChart(winRate, containerId = 'winRateChart') {
    const ctx = document.getElementById(containerId);
    if (!ctx || winRate === undefined) return;

    const lossRate = 100 - winRate;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Wins (Top 4)', 'Losses (5th-8th)'],
            datasets: [{
                data: [winRate, lossRate],
                backgroundColor: [
                    chartColors.success,
                    chartColors.danger
                ],
                borderColor: [
                    chartColors.success,
                    chartColors.danger
                ],
                borderWidth: 2,
                cutout: '70%'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#f8f9fa',
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(33, 37, 41, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed.toFixed(1)}%`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                duration: 2000
            }
        }
    });
}

// Initialize Rank Progress Chart (for showing tier progression)
function initRankProgressChart(rankHistory, containerId = 'rankProgressChart') {
    const ctx = document.getElementById(containerId);
    if (!ctx || !rankHistory || rankHistory.length === 0) return;

    const tierColors = {
        'IRON': '#6b4423',
        'BRONZE': '#cd7f32',
        'SILVER': '#c0c0c0',
        'GOLD': '#ffd700',
        'PLATINUM': '#40e0d0',
        'DIAMOND': '#b9f2ff',
        'MASTER': '#9d4edd',
        'GRANDMASTER': '#ff6b6b',
        'CHALLENGER': '#f72585'
    };

    const labels = rankHistory.map((entry, index) => `Game ${index + 1}`);
    const data = rankHistory.map(entry => {
        // Convert tier to numeric value for chart
        const tierValues = {
            'IRON': 1, 'BRONZE': 2, 'SILVER': 3, 'GOLD': 4,
            'PLATINUM': 5, 'DIAMOND': 6, 'MASTER': 7,
            'GRANDMASTER': 8, 'CHALLENGER': 9
        };
        return tierValues[entry.tier] || 1;
    });

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Rank Tier',
                data: data,
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.1,
                pointBackgroundColor: data.map(value => {
                    const tiers = ['', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER'];
                    return tierColors[tiers[value]] || chartColors.primary;
                }),
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6
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
                    backgroundColor: 'rgba(33, 37, 41, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const tiers = ['', 'Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster', 'Challenger'];
                            return `Tier: ${tiers[context.parsed.y]}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6c757d',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6c757d',
                        stepSize: 1,
                        min: 1,
                        max: 9,
                        callback: function(value) {
                            const tiers = ['', 'Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'GM', 'Challenger'];
                            return tiers[value] || '';
                        }
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Utility function to update chart data (for real-time updates)
function updateChartData(chart, newData, newLabels = null) {
    if (newLabels) {
        chart.data.labels = newLabels;
    }
    chart.data.datasets[0].data = newData;
    chart.update('active');
}

// Function to animate chart on scroll (intersection observer)
function setupChartAnimations() {
    const charts = document.querySelectorAll('canvas');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const chart = Chart.getChart(entry.target);
                if (chart) {
                    chart.update('active');
                }
            }
        });
    }, { threshold: 0.5 });

    charts.forEach(chart => observer.observe(chart));
}

// Initialize chart animations on page load
document.addEventListener('DOMContentLoaded', function() {
    setupChartAnimations();
});

// Export functions for use in other scripts
window.TFTCharts = {
    initLPChart,
    initPlacementChart,
    initWinRateChart,
    initRankProgressChart,
    updateChartData
};


// Dashboard specific JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Animate stat cards on load
    animateStatCards();
    
    // Setup refresh button
    setupRefreshButton();
    
    // Setup placement grid hover effects
    setupPlacementGrid();

    // LP History Chart
    const lpData = window.lpHistoryData || [];
    if (lpData && lpData.length > 0) {
        initLPChart(lpData);
    }

    // Placement Distribution Chart
    const placementData = window.placementDistributionData || {};
    if (placementData) {
        initPlacementChart(placementData);
    }
});

function animateStatCards() {
    const statCards = document.querySelectorAll('.card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function setupRefreshButton() {
    const refreshBtn = document.querySelector('a[href*="refresh_data"]');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function(e) {
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.add('fa-spin');
                
                // Remove spin after 2 seconds
                setTimeout(() => {
                    icon.classList.remove('fa-spin');
                }, 2000);
            }
        });
    }
}

function setupPlacementGrid() {
    const placementSquares = document.querySelectorAll('.placement-square');
    placementSquares.forEach(square => {
        square.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        square.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// Utility function to format numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Function to update stats dynamically (for future API integration)
function updateStats(newStats) {
    const statElements = {
        winRate: document.querySelector('.stat-win-rate'),
        gamesPlayed: document.querySelector('.stat-games-played'),
        avgPlacement: document.querySelector('.stat-avg-placement'),
        rank: document.querySelector('.stat-rank')
    };
    
    Object.keys(statElements).forEach(key => {
        const element = statElements[key];
        if (element && newStats[key] !== undefined) {
            // Animate number change
            animateNumberChange(element, newStats[key]);
        }
    });
}

function animateNumberChange(element, newValue) {
    const currentValue = parseFloat(element.textContent) || 0;
    const increment = (newValue - currentValue) / 20;
    let current = currentValue;
    
    const timer = setInterval(() => {
        current += increment;
        
        if ((increment > 0 && current >= newValue) || (increment < 0 && current <= newValue)) {
            current = newValue;
            clearInterval(timer);
        }
        
        element.textContent = Math.round(current * 10) / 10;
    }, 50);
}

// Show/hide loading states
function showLoading(element) {
    const loadingHtml = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    element.innerHTML = loadingHtml;
}

function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
}

// Add fade in animation to tables
function fadeInTable() {
    const table = document.querySelector('.table');
    if (table) {
        table.style.opacity = '0';
        table.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            table.style.transition = 'all 0.6s ease';
            table.style.opacity = '1';
            table.style.transform = 'translateY(0)';
        }, 200);
    }
}

// Call fade in animation
fadeInTable();

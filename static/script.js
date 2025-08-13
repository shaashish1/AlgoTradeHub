// AlgoTrading Web Application JavaScript

// Global variables
let chartInstances = {};
let refreshIntervals = {};
let toastInstance = null;

// Utility functions
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) return;

    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function formatCurrency(amount, decimals = 2) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(amount);
}

function formatPercentage(value, decimals = 2) {
    return `${value.toFixed(decimals)}%`;
}

function formatNumber(value, decimals = 2) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(value);
}

function formatTimestamp(timestamp) {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString();
}

function formatDuration(startTime, endTime = null) {
    if (!startTime) return 'N/A';

    const start = new Date(startTime);
    const end = endTime ? new Date(endTime) : new Date();
    const diffMs = end - start;
    const diffMinutes = Math.floor(diffMs / (1000 * 60));

    if (diffMinutes < 60) {
        return `${diffMinutes}m`;
    } else if (diffMinutes < 1440) {
        const hours = Math.floor(diffMinutes / 60);
        const minutes = diffMinutes % 60;
        return `${hours}h ${minutes}m`;
    } else {
        const days = Math.floor(diffMinutes / 1440);
        const hours = Math.floor((diffMinutes % 1440) / 60);
        return `${days}d ${hours}h`;
    }
}

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

// API helper functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

async function getStatus() {
    return apiRequest('/api/status');
}

async function getPerformance() {
    return apiRequest('/api/get_performance');
}

async function getTrades() {
    return apiRequest('/api/get_trades');
}

async function getPositions() {
    return apiRequest('/api/get_positions');
}

async function getMetrics() {
    return apiRequest('/api/get_metrics');
}

async function getChartData(type) {
    return apiRequest(`/api/get_chart_data?type=${type}`);
}

async function runBacktest(config) {
    return apiRequest('/api/run_backtest', {
        method: 'POST',
        body: JSON.stringify(config)
    });
}

async function startScanner() {
    return apiRequest('/api/start_scanner', {
        method: 'POST'
    });
}

async function stopScanner() {
    return apiRequest('/api/stop_scanner', {
        method: 'POST'
    });
}

async function updateConfig(type, data, exchange = null) {
    return apiRequest('/api/update_config', {
        method: 'POST',
        body: JSON.stringify({
            type,
            data,
            exchange
        })
    });
}

async function exportData(type) {
    return apiRequest(`/api/export_data?type=${type}`);
}

// Chart utilities
function createChart(containerId, data, layout = {}) {
    const defaultLayout = {
        responsive: true,
        displayModeBar: false,
        margin: { l: 50, r: 50, t: 50, b: 50 },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size: 12,
            color: '#495057'
        },
        xaxis: {
            gridcolor: '#e9ecef',
            linecolor: '#dee2e6',
            tickcolor: '#dee2e6'
        },
        yaxis: {
            gridcolor: '#e9ecef',
            linecolor: '#dee2e6',
            tickcolor: '#dee2e6'
        }
    };

    const mergedLayout = { ...defaultLayout, ...layout };

    const config = {
        responsive: true,
        displayModeBar: false,
        showTips: false
    };

    if (chartInstances[containerId]) {
        Plotly.purge(containerId);
    }

    Plotly.newPlot(containerId, data, mergedLayout, config);
    chartInstances[containerId] = true;
}

function destroyChart(containerId) {
    if (chartInstances[containerId]) {
        Plotly.purge(containerId);
        delete chartInstances[containerId];
    }
}

// Loading states
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('loading');
        element.innerHTML = `
            <div class="d-flex justify-content-center align-items-center" style="height: 200px;">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('loading');
    }
}

// Data refresh functions
async function refreshDashboard() {
    try {
        const [status, performance, trades, positions] = await Promise.all([
            getStatus(),
            getPerformance(),
            getTrades(),
            getPositions()
        ]);

        updateDashboardData(status, performance, trades, positions);
    } catch (error) {
        console.error('Error refreshing dashboard:', error);
        showToast('Error refreshing dashboard data', 'danger');
    }
}

function updateDashboardData(status, performance, trades, positions) {
    // Update status indicators
    updateStatusIndicators(status);

    // Update performance metrics
    updatePerformanceMetrics(performance);

    // Update tables
    updateTradesTable(trades.trades || []);
    updatePositionsTable(positions.positions || {});
}

function updateStatusIndicators(status) {
    const statusElements = document.querySelectorAll('[data-status]');
    statusElements.forEach(element => {
        const statusType = element.dataset.status;
        if (status[statusType] !== undefined) {
            element.textContent = status[statusType];
        }
    });
}

function updatePerformanceMetrics(performance) {
    const metricsElements = document.querySelectorAll('[data-metric]');
    metricsElements.forEach(element => {
        const metricType = element.dataset.metric;
        if (performance[metricType] !== undefined) {
            let value = performance[metricType];

            // Format based on metric type
            if (metricType.includes('pnl') || metricType.includes('profit')) {
                value = formatCurrency(value);
            } else if (metricType.includes('rate') || metricType.includes('percentage')) {
                value = formatPercentage(value);
            } else if (typeof value === 'number') {
                value = formatNumber(value);
            }

            element.textContent = value;

            // Add color classes for PnL values
            if (metricType.includes('pnl')) {
                element.classList.remove('text-success', 'text-danger');
                element.classList.add(performance[metricType] >= 0 ? 'text-success' : 'text-danger');
            }
        }
    });
}

function updateTradesTable(trades) {
    const tableBody = document.querySelector('#trades-table tbody');
    if (!tableBody) return;

    if (trades.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="10" class="text-center text-muted">No trades available</td>
            </tr>
        `;
        return;
    }

    const recentTrades = trades.slice(-20).reverse();
    tableBody.innerHTML = recentTrades.map(trade => `
        <tr>
            <td>${formatTimestamp(trade.exit_time)}</td>
            <td>${trade.exchange}</td>
            <td>${trade.symbol}</td>
            <td>
                <span class="badge bg-${trade.side === 'buy' ? 'success' : 'danger'}">
                    ${trade.side.toUpperCase()}
                </span>
            </td>
            <td>${formatCurrency(trade.entry_price, 4)}</td>
            <td>${trade.exit_price ? formatCurrency(trade.exit_price, 4) : 'N/A'}</td>
            <td>${formatNumber(trade.quantity, 4)}</td>
            <td class="text-${trade.pnl >= 0 ? 'success' : 'danger'}">
                ${formatCurrency(trade.pnl)}
            </td>
            <td class="text-${trade.pnl_percentage >= 0 ? 'success' : 'danger'}">
                ${formatPercentage(trade.pnl_percentage)}
            </td>
            <td>${formatDuration(trade.entry_time, trade.exit_time)}</td>
        </tr>
    `).join('');
}

function updatePositionsTable(positions) {
    const tableBody = document.querySelector('#positions-table tbody');
    if (!tableBody) return;

    const positionArray = Object.values(positions);

    if (positionArray.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="10" class="text-center text-muted">No open positions</td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = positionArray.map(position => `
        <tr>
            <td>${position.exchange}</td>
            <td>${position.symbol}</td>
            <td>
                <span class="badge bg-${position.side === 'buy' ? 'success' : 'danger'}">
                    ${position.side.toUpperCase()}
                </span>
            </td>
            <td>${formatCurrency(position.entry_price, 4)}</td>
            <td>${formatCurrency(position.current_price, 4)}</td>
            <td>${formatNumber(position.quantity, 4)}</td>
            <td class="text-${position.pnl >= 0 ? 'success' : 'danger'}">
                ${formatCurrency(position.pnl)}
            </td>
            <td class="text-${position.pnl_percentage >= 0 ? 'success' : 'danger'}">
                ${formatPercentage(position.pnl_percentage)}
            </td>
            <td>${formatDuration(position.entry_time)}</td>
            <td>
                <span class="badge bg-primary">${position.status.toUpperCase()}</span>
            </td>
        </tr>
    `).join('');
}

// Auto-refresh functionality
function startAutoRefresh(interval = 30000) {
    if (refreshIntervals.dashboard) {
        clearInterval(refreshIntervals.dashboard);
    }

    refreshIntervals.dashboard = setInterval(refreshDashboard, interval);
}

function stopAutoRefresh() {
    Object.values(refreshIntervals).forEach(interval => {
        clearInterval(interval);
    });
    refreshIntervals = {};
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Start auto-refresh if on dashboard
    if (window.location.pathname === '/' || window.location.pathname.includes('dashboard')) {
        startAutoRefresh();
    }

    // Handle form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            if (validateForm(form.id)) {
                // Handle form submission based on form ID
                handleFormSubmission(form);
            }
        });
    });

    // Handle real-time updates
    if (window.location.pathname.includes('realtime')) {
        startRealtimeUpdates();
    }
});

function handleFormSubmission(form) {
    const formId = form.id;

    switch (formId) {
        case 'backtest-form':
            handleBacktestForm(form);
            break;
        case 'config-form':
            handleConfigForm(form);
            break;
        default:
            console.warn('Unknown form:', formId);
    }
}

async function handleBacktestForm(form) {
    const formData = new FormData(form);
    const config = {
        exchange: formData.get('exchange'),
        symbol: formData.get('symbol'),
        timeframe: formData.get('timeframe'),
        start_date: formData.get('start_date'),
        end_date: formData.get('end_date'),
        initial_capital: parseFloat(formData.get('initial_capital')),
        commission: parseFloat(formData.get('commission'))
    };

    try {
        showLoading('backtest-results');
        const result = await runBacktest(config);

        if (result.status === 'success') {
            showToast('Backtest started successfully', 'success');
            // Poll for results
            pollBacktestResults();
        } else {
            throw new Error(result.error || 'Backtest failed');
        }
    } catch (error) {
        hideLoading('backtest-results');
        showToast(error.message, 'danger');
    }
}

async function handleConfigForm(form) {
    const formData = new FormData(form);
    const configType = formData.get('config_type');
    const configData = {};

    // Collect form data
    for (let [key, value] of formData.entries()) {
        if (key !== 'config_type') {
            configData[key] = value;
        }
    }

    try {
        const result = await updateConfig(configType, configData);

        if (result.status === 'success') {
            showToast('Configuration updated successfully', 'success');
        } else {
            throw new Error(result.error || 'Configuration update failed');
        }
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

function pollBacktestResults() {
    const pollInterval = setInterval(async () => {
        try {
            const metrics = await getMetrics();
            if (metrics.metrics && Object.keys(metrics.metrics).length > 0) {
                clearInterval(pollInterval);
                hideLoading('backtest-results');
                displayBacktestResults(metrics.metrics);
            }
        } catch (error) {
            console.error('Error polling backtest results:', error);
        }
    }, 2000);

    // Stop polling after 2 minutes
    setTimeout(() => {
        clearInterval(pollInterval);
        hideLoading('backtest-results');
    }, 120000);
}

function displayBacktestResults(metrics) {
    const resultsContainer = document.getElementById('backtest-results');
    if (!resultsContainer) return;

    // Display charts and metrics
    loadBacktestChart('portfolio');
    displayPerformanceMetrics(metrics);
}

function displayPerformanceMetrics(metrics) {
    const metricsContainer = document.getElementById('performance-metrics');
    if (!metricsContainer) return;

    const keyMetrics = [
        'Return [%]', 'Volatility (Ann.) [%]', 'Sharpe Ratio', 'Max. Drawdown [%]',
        '# Trades', 'Win Rate [%]', 'Profit Factor', 'Net Profit [$]'
    ];

    metricsContainer.innerHTML = keyMetrics.map(metric => {
        const value = metrics[metric];
        if (value !== undefined) {
            return `
                <div class="col-md-3 col-sm-6 mb-3">
                    <div class="metric-card">
                        <div class="metric-label">${metric}</div>
                        <div class="metric-value">${value}</div>
                    </div>
                </div>
            `;
        }
        return '';
    }).join('');
}

async function loadBacktestChart(type) {
    try {
        const chartData = await getChartData(type);
        if (chartData.chart) {
            const data = JSON.parse(chartData.chart);
            createChart('backtest-results', data.data, data.layout);
        }
    } catch (error) {
        console.error('Error loading backtest chart:', error);
    }
}

function startRealtimeUpdates() {
    // Start frequent updates for real-time page
    if (refreshIntervals.realtime) {
        clearInterval(refreshIntervals.realtime);
    }

    refreshIntervals.realtime = setInterval(async () => {
        try {
            const [positions, trades] = await Promise.all([
                getPositions(),
                getTrades()
            ]);

            updatePositionsTable(positions.positions || {});
            updateTradesTable(trades.trades || []);
        } catch (error) {
            console.error('Error updating realtime data:', error);
        }
    }, 5000); // Update every 5 seconds
}

// Cleanup on page unload
window.addEventListener('beforeunload', function () {
    stopAutoRefresh();
    Object.keys(chartInstances).forEach(containerId => {
        destroyChart(containerId);
    });
});

// Export functions for global use
window.AlgoTrading = {
    showToast,
    formatCurrency,
    formatPercentage,
    formatNumber,
    formatTimestamp,
    formatDuration,
    apiRequest,
    getStatus,
    getPerformance,
    getTrades,
    getPositions,
    getMetrics,
    getChartData,
    runBacktest,
    startScanner,
    stopScanner,
    updateConfig,
    exportData,
    createChart,
    destroyChart,
    refreshDashboard,
    startAutoRefresh,
    stopAutoRefresh
};

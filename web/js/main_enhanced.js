// Enhanced Main JavaScript for Fuzzy Traffic Control System
// Supports all 9 scenarios with advanced visualizations

let comparisonData = null;
let charts = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadComparisonData();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const scenarioSelect = document.getElementById('scenario-select');
    if (scenarioSelect) {
        scenarioSelect.addEventListener('change', () => {
            const scenario = scenarioSelect.value;
            updateVisualization(scenario);
        });
    }

    const showAllBtn = document.getElementById('show-all-btn');
    if (showAllBtn) {
        showAllBtn.addEventListener('click', showAllScenariosModal);
    }
}

// Load comparison data from JSON
async function loadComparisonData() {
    try {
        const response = await fetch('data/comparison_results.json');
        if (response.ok) {
            comparisonData = await response.json();
        } else {
            comparisonData = getEnhancedMockData();
        }
    } catch (error) {
        console.warn('Using mock data:', error);
        comparisonData = getEnhancedMockData();
    }

    updateSummaryStats();
    updateAllScenariosChart();
    updateVisualization('normal');
}

// Update overall summary statistics
function updateSummaryStats() {
    if (!comparisonData) return;

    const scenarios = Object.values(comparisonData);

    // Calculate average improvement
    const avgImprovement = scenarios.reduce((sum, s) =>
        sum + s.comparison['waiting_time_improvement_%'], 0) / scenarios.length;

    // Find best scenario
    const bestScenario = scenarios.reduce((best, current) =>
        current.comparison['waiting_time_improvement_%'] >
        best.comparison['waiting_time_improvement_%'] ? current : best
    );

    // Calculate success rate
    const successCount = scenarios.filter(s =>
        s.comparison['waiting_time_improvement_%'] > 0).length;

    // Calculate average queue reduction
    const avgQueueReduction = scenarios.reduce((sum, s) =>
        sum + s.comparison['queue_length_improvement_%'], 0) / scenarios.length;

    // Update DOM
    document.getElementById('avg-improvement').textContent =
        `${avgImprovement >= 0 ? '+' : ''}${avgImprovement.toFixed(1)}%`;
    document.getElementById('avg-improvement').style.color =
        avgImprovement >= 0 ? 'var(--success-color)' : 'var(--danger-color)';

    document.getElementById('best-scenario').textContent =
        bestScenario.scenario.name;

    document.getElementById('success-rate').textContent =
        `${successCount}/${scenarios.length}`;

    document.getElementById('queue-reduction').textContent =
        `${avgQueueReduction >= 0 ? '+' : ''}${avgQueueReduction.toFixed(1)}%`;
    document.getElementById('queue-reduction').style.color =
        avgQueueReduction >= 0 ? 'var(--success-color)' : 'var(--danger-color)';
}

// Update all scenarios comparison chart
function updateAllScenariosChart() {
    const ctx = document.getElementById('allScenariosChart');
    if (!ctx || !comparisonData) return;

    if (charts.allScenarios) {
        charts.allScenarios.destroy();
    }

    const scenarioNames = Object.values(comparisonData).map(d => d.scenario.name);
    const fuzzyData = Object.values(comparisonData).map(d => d.fuzzy.average_waiting_time);
    const fixedData = Object.values(comparisonData).map(d => d.fixed.average_waiting_time);

    charts.allScenarios = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: scenarioNames,
            datasets: [{
                label: 'Fuzzy Controller',
                data: fuzzyData,
                backgroundColor: 'rgba(37, 99, 235, 0.7)',
                borderColor: 'rgba(37, 99, 235, 1)',
                borderWidth: 2
            }, {
                label: 'Fixed-Time Controller',
                data: fixedData,
                backgroundColor: 'rgba(239, 68, 68, 0.7)',
                borderColor: 'rgba(239, 68, 68, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Average Waiting Time - All 9 Scenarios',
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        afterLabel: function(context) {
                            const scenarioKey = Object.keys(comparisonData)[context.dataIndex];
                            const improvement = comparisonData[scenarioKey].comparison['waiting_time_improvement_%'];
                            return `Improvement: ${improvement >= 0 ? '+' : ''}${improvement.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Avg Waiting Time (seconds)'
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

// Update visualization for selected scenario
function updateVisualization(scenarioKey) {
    if (!comparisonData || !comparisonData[scenarioKey]) {
        console.error('Scenario data not found:', scenarioKey);
        return;
    }

    const data = comparisonData[scenarioKey];

    updateScenarioInfo(data.scenario);
    updateWaitingTimeChart(data);
    updateQueueLengthChart(data);
    updateThroughputChart(data);
    updateImprovementChart(data);
    updateMetricsTable(data);
}

// Update scenario information
function updateScenarioInfo(scenario) {
    const infoDiv = document.getElementById('scenario-info');
    const arrivalRates = Object.entries(scenario.arrival_rates)
        .map(([dir, rate]) => `${dir}: ${rate} veh/min`)
        .join(', ');

    infoDiv.innerHTML = `
        <h3>${scenario.name}</h3>
        <p><strong>Description:</strong> ${scenario.description}</p>
        <p><strong>Arrival Rates:</strong> ${arrivalRates}</p>
    `;
}

// Update Waiting Time Chart
function updateWaitingTimeChart(data) {
    const ctx = document.getElementById('waitingTimeChart');
    if (!ctx) return;

    if (charts.waitingTime) {
        charts.waitingTime.destroy();
    }

    charts.waitingTime = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Fuzzy Controller', 'Fixed-Time Controller'],
            datasets: [{
                label: 'Average Waiting Time (seconds)',
                data: [
                    data.fuzzy.average_waiting_time,
                    data.fixed.average_waiting_time
                ],
                backgroundColor: [
                    'rgba(37, 99, 235, 0.7)',
                    'rgba(239, 68, 68, 0.7)'
                ],
                borderColor: [
                    'rgba(37, 99, 235, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Average Waiting Time Comparison',
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Seconds'
                    }
                }
            }
        }
    });
}

// Update Queue Length Chart
function updateQueueLengthChart(data) {
    const ctx = document.getElementById('queueLengthChart');
    if (!ctx) return;

    if (charts.queueLength) {
        charts.queueLength.destroy();
    }

    charts.queueLength = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Fuzzy Controller', 'Fixed-Time Controller'],
            datasets: [{
                label: 'Average Queue Length (vehicles)',
                data: [
                    data.fuzzy.average_queue_length,
                    data.fixed.average_queue_length
                ],
                backgroundColor: [
                    'rgba(124, 58, 237, 0.7)',
                    'rgba(239, 68, 68, 0.7)'
                ],
                borderColor: [
                    'rgba(124, 58, 237, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Average Queue Length Comparison',
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Vehicles'
                    }
                }
            }
        }
    });
}

// Update Throughput Chart
function updateThroughputChart(data) {
    const ctx = document.getElementById('throughputChart');
    if (!ctx) return;

    if (charts.throughput) {
        charts.throughput.destroy();
    }

    charts.throughput = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Fuzzy Controller', 'Fixed-Time Controller'],
            datasets: [{
                label: 'Throughput (vehicles/hour)',
                data: [
                    data.fuzzy.throughput_per_hour,
                    data.fixed.throughput_per_hour
                ],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(239, 68, 68, 0.7)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Throughput Comparison',
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Vehicles/Hour'
                    }
                }
            }
        }
    });
}

// Update Improvement Chart
function updateImprovementChart(data) {
    const ctx = document.getElementById('improvementChart');
    if (!ctx) return;

    if (charts.improvement) {
        charts.improvement.destroy();
    }

    const improvements = [
        data.comparison['waiting_time_improvement_%'],
        data.comparison['queue_length_improvement_%'],
        data.comparison['throughput_improvement_%'],
        data.comparison['delay_reduction_%']
    ];

    charts.improvement = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Waiting Time', 'Queue Length', 'Throughput', 'Delay'],
            datasets: [{
                label: 'Improvement (%)',
                data: improvements,
                backgroundColor: improvements.map(v =>
                    v >= 0 ? 'rgba(16, 185, 129, 0.7)' : 'rgba(239, 68, 68, 0.7)'
                ),
                borderColor: improvements.map(v =>
                    v >= 0 ? 'rgba(16, 185, 129, 1)' : 'rgba(239, 68, 68, 1)'
                ),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Fuzzy vs Fixed-Time Improvement',
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Improvement (%)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Update Metrics Table
function updateMetricsTable(data) {
    const tableDiv = document.getElementById('metrics-table');
    if (!tableDiv) return;

    const fuzzy = data.fuzzy;
    const fixed = data.fixed;
    const comp = data.comparison;

    const html = `
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Fuzzy Controller</th>
                    <th>Fixed-Time Controller</th>
                    <th>Improvement</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Avg Waiting Time</td>
                    <td>${fuzzy.average_waiting_time.toFixed(2)}s</td>
                    <td>${fixed.average_waiting_time.toFixed(2)}s</td>
                    <td class="metric-improvement ${comp['waiting_time_improvement_%'] >= 0 ? 'positive' : 'negative'}">
                        ${comp['waiting_time_improvement_%'] >= 0 ? '+' : ''}${comp['waiting_time_improvement_%'].toFixed(1)}%
                    </td>
                </tr>
                <tr>
                    <td>Max Waiting Time</td>
                    <td>${fuzzy.max_waiting_time.toFixed(2)}s</td>
                    <td>${fixed.max_waiting_time.toFixed(2)}s</td>
                    <td>-</td>
                </tr>
                <tr>
                    <td>Avg Queue Length</td>
                    <td>${fuzzy.average_queue_length.toFixed(2)} vehicles</td>
                    <td>${fixed.average_queue_length.toFixed(2)} vehicles</td>
                    <td class="metric-improvement ${comp['queue_length_improvement_%'] >= 0 ? 'positive' : 'negative'}">
                        ${comp['queue_length_improvement_%'] >= 0 ? '+' : ''}${comp['queue_length_improvement_%'].toFixed(1)}%
                    </td>
                </tr>
                <tr>
                    <td>Max Queue Length</td>
                    <td>${fuzzy.max_queue_length} vehicles</td>
                    <td>${fixed.max_queue_length} vehicles</td>
                    <td>-</td>
                </tr>
                <tr>
                    <td>Throughput</td>
                    <td>${fuzzy.throughput_per_hour.toFixed(1)} veh/h</td>
                    <td>${fixed.throughput_per_hour.toFixed(1)} veh/h</td>
                    <td class="metric-improvement ${comp['throughput_improvement_%'] >= 0 ? 'positive' : 'negative'}">
                        ${comp['throughput_improvement_%'] >= 0 ? '+' : ''}${comp['throughput_improvement_%'].toFixed(1)}%
                    </td>
                </tr>
                <tr>
                    <td>Fairness Index</td>
                    <td>${fuzzy.fairness_index.toFixed(3)}</td>
                    <td>${fixed.fairness_index.toFixed(3)}</td>
                    <td class="metric-improvement ${comp.fairness_improvement >= 0 ? 'positive' : 'negative'}">
                        ${comp.fairness_improvement >= 0 ? '+' : ''}${comp.fairness_improvement.toFixed(3)}
                    </td>
                </tr>
            </tbody>
        </table>
    `;

    tableDiv.innerHTML = html;
}

// Show all scenarios modal
function showAllScenariosModal() {
    // Create modal if it doesn't exist
    let modal = document.getElementById('all-scenarios-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'all-scenarios-modal';
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 1200px;">
                <div class="modal-header">
                    <h2>All Scenarios Comparison</h2>
                    <span class="modal-close">&times;</span>
                </div>
                <div id="modal-charts-container"></div>
            </div>
        `;
        document.body.appendChild(modal);

        // Close modal on click
        modal.querySelector('.modal-close').onclick = () => {
            modal.classList.remove('active');
        };
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        };
    }

    // Show modal
    modal.classList.add('active');

    // Populate with comparison data
    const container = document.getElementById('modal-charts-container');
    container.innerHTML = createAllScenariosComparisonTable();
}

// Create comparison table for all scenarios
function createAllScenariosComparisonTable() {
    if (!comparisonData) return '<p>No data available</p>';

    let html = `
        <table class="metrics-table" style="margin-top: 1rem;">
            <thead>
                <tr>
                    <th>Scenario</th>
                    <th>Fuzzy Wait (s)</th>
                    <th>Fixed Wait (s)</th>
                    <th>Improvement</th>
                    <th>Queue Reduction</th>
                    <th>Throughput Gain</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (const [key, data] of Object.entries(comparisonData)) {
        const waitImprove = data.comparison['waiting_time_improvement_%'];
        const queueImprove = data.comparison['queue_length_improvement_%'];
        const throughputImprove = data.comparison['throughput_improvement_%'];

        html += `
            <tr>
                <td><strong>${data.scenario.name}</strong></td>
                <td>${data.fuzzy.average_waiting_time.toFixed(2)}</td>
                <td>${data.fixed.average_waiting_time.toFixed(2)}</td>
                <td class="metric-improvement ${waitImprove >= 0 ? 'positive' : 'negative'}">
                    ${waitImprove >= 0 ? '+' : ''}${waitImprove.toFixed(1)}%
                </td>
                <td class="metric-improvement ${queueImprove >= 0 ? 'positive' : 'negative'}">
                    ${queueImprove >= 0 ? '+' : ''}${queueImprove.toFixed(1)}%
                </td>
                <td class="metric-improvement ${throughputImprove >= 0 ? 'positive' : 'negative'}">
                    ${throughputImprove >= 0 ? '+' : ''}${throughputImprove.toFixed(1)}%
                </td>
            </tr>
        `;
    }

    html += `
            </tbody>
        </table>
    `;

    return html;
}

// Enhanced Mock data with all 9 scenarios
function getEnhancedMockData() {
    return {
        "normal": {
            "scenario": {
                "name": "Normal Traffic",
                "description": "Balanced traffic with moderate flow on all directions",
                "arrival_rates": {"north": 12, "south": 12, "east": 12, "west": 12}
            },
            "fuzzy": {
                "average_waiting_time": 9.81,
                "max_waiting_time": 35.0,
                "average_queue_length": 7.62,
                "max_queue_length": 21,
                "throughput_per_hour": 2784,
                "fairness_index": 1.000
            },
            "fixed": {
                "average_waiting_time": 15.69,
                "max_waiting_time": 50.0,
                "average_queue_length": 12.26,
                "max_queue_length": 33,
                "throughput_per_hour": 2752,
                "fairness_index": 0.998
            },
            "comparison": {
                "waiting_time_improvement_%": 37.5,
                "queue_length_improvement_%": 37.8,
                "throughput_improvement_%": 1.2,
                "delay_reduction_%": 37.5,
                "fairness_improvement": 0.002
            }
        },
        "rush_ns": {
            "scenario": {
                "name": "Rush Hour (N-S)",
                "description": "Heavy North-South traffic",
                "arrival_rates": {"north": 35, "south": 35, "east": 10, "west": 10}
            },
            "fuzzy": {
                "average_waiting_time": 13.64,
                "max_waiting_time": 53.0,
                "average_queue_length": 19.70,
                "max_queue_length": 58,
                "throughput_per_hour": 5184,
                "fairness_index": 0.956
            },
            "fixed": {
                "average_waiting_time": 17.89,
                "max_waiting_time": 51.0,
                "average_queue_length": 26.00,
                "max_queue_length": 75,
                "throughput_per_hour": 5128,
                "fairness_index": 0.986
            },
            "comparison": {
                "waiting_time_improvement_%": 23.7,
                "queue_length_improvement_%": 24.2,
                "throughput_improvement_%": 1.1,
                "delay_reduction_%": 23.7,
                "fairness_improvement": -0.030
            }
        },
        "rush_ew": {
            "scenario": {
                "name": "Rush Hour (E-W)",
                "description": "Heavy East-West traffic",
                "arrival_rates": {"north": 10, "south": 10, "east": 35, "west": 35}
            },
            "fuzzy": {
                "average_waiting_time": 12.65,
                "max_waiting_time": 48.2,
                "average_queue_length": 18.45,
                "max_queue_length": 55,
                "throughput_per_hour": 5208,
                "fairness_index": 0.962
            },
            "fixed": {
                "average_waiting_time": 19.46,
                "max_waiting_time": 58.3,
                "average_queue_length": 28.76,
                "max_queue_length": 82,
                "throughput_per_hour": 5112,
                "fairness_index": 0.978
            },
            "comparison": {
                "waiting_time_improvement_%": 35.0,
                "queue_length_improvement_%": 35.9,
                "throughput_improvement_%": 1.9,
                "delay_reduction_%": 35.0,
                "fairness_improvement": -0.016
            }
        },
        "light": {
            "scenario": {
                "name": "Light Traffic",
                "description": "Light traffic (late night)",
                "arrival_rates": {"north": 5, "south": 5, "east": 5, "west": 5}
            },
            "fuzzy": {
                "average_waiting_time": 8.27,
                "max_waiting_time": 28.5,
                "average_queue_length": 2.87,
                "max_queue_length": 9,
                "throughput_per_hour": 1152,
                "fairness_index": 0.998
            },
            "fixed": {
                "average_waiting_time": 15.68,
                "max_waiting_time": 42.1,
                "average_queue_length": 5.44,
                "max_queue_length": 15,
                "throughput_per_hour": 1128,
                "fairness_index": 0.995
            },
            "comparison": {
                "waiting_time_improvement_%": 47.2,
                "queue_length_improvement_%": 47.2,
                "throughput_improvement_%": 2.1,
                "delay_reduction_%": 47.2,
                "fairness_improvement": 0.003
            }
        },
        "asymmetric_north": {
            "scenario": {
                "name": "Asymmetric (Heavy North)",
                "description": "Heavy North traffic only",
                "arrival_rates": {"north": 45, "south": 8, "east": 8, "west": 8}
            },
            "fuzzy": {
                "average_waiting_time": 13.48,
                "max_waiting_time": 55.8,
                "average_queue_length": 15.23,
                "max_queue_length": 48,
                "throughput_per_hour": 3984,
                "fairness_index": 0.912
            },
            "fixed": {
                "average_waiting_time": 19.39,
                "max_waiting_time": 68.2,
                "average_queue_length": 21.89,
                "max_queue_length": 68,
                "throughput_per_hour": 3876,
                "fairness_index": 0.895
            },
            "comparison": {
                "waiting_time_improvement_%": 30.5,
                "queue_length_improvement_%": 30.4,
                "throughput_improvement_%": 2.8,
                "delay_reduction_%": 30.5,
                "fairness_improvement": 0.017
            }
        },
        "peak": {
            "scenario": {
                "name": "Peak Congestion",
                "description": "Heavy traffic all directions",
                "arrival_rates": {"north": 40, "south": 40, "east": 40, "west": 40}
            },
            "fuzzy": {
                "average_waiting_time": 20.37,
                "max_waiting_time": 72.5,
                "average_queue_length": 45.82,
                "max_queue_length": 125,
                "throughput_per_hour": 8640,
                "fairness_index": 0.978
            },
            "fixed": {
                "average_waiting_time": 19.80,
                "max_waiting_time": 68.9,
                "average_queue_length": 44.32,
                "max_queue_length": 118,
                "throughput_per_hour": 8784,
                "fairness_index": 0.982
            },
            "comparison": {
                "waiting_time_improvement_%": -2.9,
                "queue_length_improvement_%": -3.4,
                "throughput_improvement_%": -1.6,
                "delay_reduction_%": -2.9,
                "fairness_improvement": -0.004
            }
        },
        "morning": {
            "scenario": {
                "name": "Morning Commute",
                "description": "Inbound heavy traffic",
                "arrival_rates": {"north": 30, "south": 10, "east": 25, "west": 8}
            },
            "fuzzy": {
                "average_waiting_time": 14.75,
                "max_waiting_time": 58.3,
                "average_queue_length": 21.34,
                "max_queue_length": 65,
                "throughput_per_hour": 4212,
                "fairness_index": 0.934
            },
            "fixed": {
                "average_waiting_time": 17.12,
                "max_waiting_time": 62.5,
                "average_queue_length": 24.89,
                "max_queue_length": 75,
                "throughput_per_hour": 4176,
                "fairness_index": 0.925
            },
            "comparison": {
                "waiting_time_improvement_%": 13.9,
                "queue_length_improvement_%": 14.3,
                "throughput_improvement_%": 0.9,
                "delay_reduction_%": 13.9,
                "fairness_improvement": 0.009
            }
        },
        "evening": {
            "scenario": {
                "name": "Evening Commute",
                "description": "Outbound heavy traffic",
                "arrival_rates": {"north": 10, "south": 30, "east": 8, "west": 25}
            },
            "fuzzy": {
                "average_waiting_time": 14.31,
                "max_waiting_time": 56.7,
                "average_queue_length": 20.78,
                "max_queue_length": 62,
                "throughput_per_hour": 4224,
                "fairness_index": 0.941
            },
            "fixed": {
                "average_waiting_time": 17.64,
                "max_waiting_time": 64.2,
                "average_queue_length": 25.56,
                "max_queue_length": 78,
                "throughput_per_hour": 4152,
                "fairness_index": 0.928
            },
            "comparison": {
                "waiting_time_improvement_%": 18.9,
                "queue_length_improvement_%": 18.7,
                "throughput_improvement_%": 1.7,
                "delay_reduction_%": 18.9,
                "fairness_improvement": 0.013
            }
        },
        "weekend": {
            "scenario": {
                "name": "Weekend Leisure",
                "description": "Moderate balanced flow",
                "arrival_rates": {"north": 15, "south": 18, "east": 15, "west": 18}
            },
            "fuzzy": {
                "average_waiting_time": 10.52,
                "max_waiting_time": 38.9,
                "average_queue_length": 11.23,
                "max_queue_length": 32,
                "throughput_per_hour": 3828,
                "fairness_index": 0.987
            },
            "fixed": {
                "average_waiting_time": 15.56,
                "max_waiting_time": 48.7,
                "average_queue_length": 16.58,
                "max_queue_length": 45,
                "throughput_per_hour": 3768,
                "fairness_index": 0.982
            },
            "comparison": {
                "waiting_time_improvement_%": 32.4,
                "queue_length_improvement_%": 32.3,
                "throughput_improvement_%": 1.6,
                "delay_reduction_%": 32.4,
                "fairness_improvement": 0.005
            }
        }
    };
}

// Main JavaScript for Fuzzy Traffic Control System Visualization

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
    scenarioSelect.addEventListener('change', () => {
        const scenario = scenarioSelect.value;
        updateVisualization(scenario);
    });
}

// Load comparison data from JSON
async function loadComparisonData() {
    try {
        // Try to load from data file
        const response = await fetch('data/comparison_results.json');
        if (response.ok) {
            comparisonData = await response.json();
            updateVisualization('normal');
        } else {
            // Use mock data if file not found
            comparisonData = getMockData();
            updateVisualization('normal');
        }
    } catch (error) {
        console.warn('Could not load comparison data, using mock data:', error);
        comparisonData = getMockData();
        updateVisualization('normal');
    }
}

// Update all visualizations for selected scenario
function updateVisualization(scenarioKey) {
    if (!comparisonData || !comparisonData[scenarioKey]) {
        console.error('Scenario data not found:', scenarioKey);
        return;
    }

    const data = comparisonData[scenarioKey];

    // Update scenario info
    updateScenarioInfo(data.scenario);

    // Update charts
    updateWaitingTimeChart(data);
    updateQueueLengthChart(data);
    updateThroughputChart(data);
    updateImprovementChart(data);

    // Update metrics table
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
                    <td>Total Delay</td>
                    <td>${(fuzzy.total_delay / 3600).toFixed(2)}h</td>
                    <td>${(fixed.total_delay / 3600).toFixed(2)}h</td>
                    <td class="metric-improvement ${comp['delay_reduction_%'] >= 0 ? 'positive' : 'negative'}">
                        ${comp['delay_reduction_%'] >= 0 ? '+' : ''}${comp['delay_reduction_%'].toFixed(1)}%
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

// Mock data for demonstration (used when JSON file is not available)
function getMockData() {
    return {
        "normal": {
            "scenario": {
                "name": "Normal Traffic",
                "description": "Balanced traffic with moderate flow on all directions",
                "arrival_rates": {"north": 12, "south": 12, "east": 12, "west": 12}
            },
            "fuzzy": {
                "average_waiting_time": 45.2,
                "max_waiting_time": 125.8,
                "average_queue_length": 8.5,
                "max_queue_length": 28,
                "throughput_per_hour": 576,
                "total_delay": 25920,
                "fairness_index": 0.892
            },
            "fixed": {
                "average_waiting_time": 62.4,
                "max_waiting_time": 178.3,
                "average_queue_length": 12.3,
                "max_queue_length": 42,
                "throughput_per_hour": 528,
                "total_delay": 35712,
                "fairness_index": 0.834
            },
            "comparison": {
                "waiting_time_improvement_%": 27.6,
                "queue_length_improvement_%": 30.9,
                "throughput_improvement_%": 9.1,
                "delay_reduction_%": 27.4,
                "fairness_improvement": 0.058
            }
        },
        "rush_ns": {
            "scenario": {
                "name": "Rush Hour (N-S)",
                "description": "Heavy North-South traffic (main road during rush hour)",
                "arrival_rates": {"north": 35, "south": 35, "east": 10, "west": 10}
            },
            "fuzzy": {
                "average_waiting_time": 58.7,
                "max_waiting_time": 198.5,
                "average_queue_length": 15.2,
                "max_queue_length": 52,
                "throughput_per_hour": 1080,
                "total_delay": 63288,
                "fairness_index": 0.765
            },
            "fixed": {
                "average_waiting_time": 89.3,
                "max_waiting_time": 285.2,
                "average_queue_length": 24.8,
                "max_queue_length": 78,
                "throughput_per_hour": 972,
                "total_delay": 96336,
                "fairness_index": 0.683
            },
            "comparison": {
                "waiting_time_improvement_%": 34.3,
                "queue_length_improvement_%": 38.7,
                "throughput_improvement_%": 11.1,
                "delay_reduction_%": 34.3,
                "fairness_improvement": 0.082
            }
        },
        "rush_ew": {
            "scenario": {
                "name": "Rush Hour (E-W)",
                "description": "Heavy East-West traffic corridor",
                "arrival_rates": {"north": 10, "south": 10, "east": 35, "west": 35}
            },
            "fuzzy": {
                "average_waiting_time": 56.3,
                "max_waiting_time": 192.1,
                "average_queue_length": 14.8,
                "max_queue_length": 50,
                "throughput_per_hour": 1080,
                "total_delay": 60696,
                "fairness_index": 0.778
            },
            "fixed": {
                "average_waiting_time": 87.5,
                "max_waiting_time": 278.6,
                "average_queue_length": 24.1,
                "max_queue_length": 76,
                "throughput_per_hour": 972,
                "total_delay": 94500,
                "fairness_index": 0.695
            },
            "comparison": {
                "waiting_time_improvement_%": 35.7,
                "queue_length_improvement_%": 38.6,
                "throughput_improvement_%": 11.1,
                "delay_reduction_%": 35.8,
                "fairness_improvement": 0.083
            }
        },
        "light": {
            "scenario": {
                "name": "Light Traffic",
                "description": "Late night scenario with minimal traffic",
                "arrival_rates": {"north": 5, "south": 5, "east": 5, "west": 5}
            },
            "fuzzy": {
                "average_waiting_time": 28.4,
                "max_waiting_time": 75.3,
                "average_queue_length": 3.2,
                "max_queue_length": 12,
                "throughput_per_hour": 240,
                "total_delay": 6816,
                "fairness_index": 0.945
            },
            "fixed": {
                "average_waiting_time": 35.8,
                "max_waiting_time": 92.5,
                "average_queue_length": 4.5,
                "max_queue_length": 16,
                "throughput_per_hour": 228,
                "total_delay": 8604,
                "fairness_index": 0.912
            },
            "comparison": {
                "waiting_time_improvement_%": 20.7,
                "queue_length_improvement_%": 28.9,
                "throughput_improvement_%": 5.3,
                "delay_reduction_%": 20.8,
                "fairness_improvement": 0.033
            }
        },
        "asymmetric_north": {
            "scenario": {
                "name": "Asymmetric (Heavy North)",
                "description": "Very heavy traffic from North only",
                "arrival_rates": {"north": 45, "south": 8, "east": 8, "west": 8}
            },
            "fuzzy": {
                "average_waiting_time": 65.8,
                "max_waiting_time": 215.3,
                "average_queue_length": 18.5,
                "max_queue_length": 62,
                "throughput_per_hour": 828,
                "total_delay": 54504,
                "fairness_index": 0.652
            },
            "fixed": {
                "average_waiting_time": 112.7,
                "max_waiting_time": 342.8,
                "average_queue_length": 32.4,
                "max_queue_length": 98,
                "throughput_per_hour": 720,
                "total_delay": 93348,
                "fairness_index": 0.542
            },
            "comparison": {
                "waiting_time_improvement_%": 41.6,
                "queue_length_improvement_%": 42.9,
                "throughput_improvement_%": 15.0,
                "delay_reduction_%": 41.6,
                "fairness_improvement": 0.110
            }
        },
        "peak": {
            "scenario": {
                "name": "Peak Congestion",
                "description": "Extreme congestion with heavy traffic on all directions",
                "arrival_rates": {"north": 40, "south": 40, "east": 40, "west": 40}
            },
            "fuzzy": {
                "average_waiting_time": 98.5,
                "max_waiting_time": 312.7,
                "average_queue_length": 32.8,
                "max_queue_length": 105,
                "throughput_per_hour": 1920,
                "total_delay": 189120,
                "fairness_index": 0.723
            },
            "fixed": {
                "average_waiting_time": 145.3,
                "max_waiting_time": 458.2,
                "average_queue_length": 52.6,
                "max_queue_length": 152,
                "throughput_per_hour": 1680,
                "total_delay": 278976,
                "fairness_index": 0.615
            },
            "comparison": {
                "waiting_time_improvement_%": 32.2,
                "queue_length_improvement_%": 37.6,
                "throughput_improvement_%": 14.3,
                "delay_reduction_%": 32.2,
                "fairness_improvement": 0.108
            }
        }
    };
}

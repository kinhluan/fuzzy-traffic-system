// Demo Simulation for Traffic Scenarios

class TrafficDemo {
    constructor() {
        this.scenarios = {
            normal: {
                name: "Normal Traffic",
                description: "Balanced traffic flow with moderate vehicle arrival rates on all directions (12 veh/min).",
                arrivalRates: { north: 12, south: 12, east: 12, west: 12 }
            },
            rush_ns: {
                name: "Rush Hour (N-S)",
                description: "Heavy traffic on North-South corridor (35 veh/min), light on East-West (10 veh/min). Simulates main road during rush hour.",
                arrivalRates: { north: 35, south: 35, east: 10, west: 10 }
            },
            rush_ew: {
                name: "Rush Hour (E-W)",
                description: "Heavy traffic on East-West corridor (35 veh/min), light on North-South (10 veh/min).",
                arrivalRates: { north: 10, south: 10, east: 35, west: 35 }
            },
            light: {
                name: "Light Traffic",
                description: "Late night scenario with minimal traffic on all directions (5 veh/min).",
                arrivalRates: { north: 5, south: 5, east: 5, west: 5 }
            },
            asymmetric_north: {
                name: "Asymmetric (Heavy North)",
                description: "Very heavy traffic from North only (45 veh/min), testing controller adaptability.",
                arrivalRates: { north: 45, south: 8, east: 8, west: 8 }
            },
            peak: {
                name: "Peak Congestion",
                description: "Extreme congestion with heavy traffic on all directions (40 veh/min). Stress test scenario.",
                arrivalRates: { north: 40, south: 40, east: 40, west: 40 }
            }
        };

        this.currentScenario = 'normal';
        this.controllerType = 'fuzzy';
        this.isRunning = false;
        this.isPaused = false;
        this.simulationTime = 0;
        this.speed = 5;

        this.queues = { north: 0, south: 0, east: 0, west: 0 };
        this.totalVehicles = 0;
        this.totalWaitingTime = 0;
        this.departedVehicles = 0;

        this.currentPhase = 'ns_green';
        this.phaseTime = 0;
        this.phaseDuration = 40;

        this.animationFrame = null;
        this.lastUpdate = Date.now();

        this.init();
    }

    init() {
        // Event listeners
        document.getElementById('demo-scenario-select').addEventListener('change', (e) => {
            this.changeScenario(e.target.value);
        });

        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.changeController(e.target.dataset.controller);
            });
        });

        document.getElementById('btn-start').addEventListener('click', () => this.start());
        document.getElementById('btn-pause').addEventListener('click', () => this.pause());
        document.getElementById('btn-reset').addEventListener('click', () => this.reset());

        document.getElementById('speed-slider').addEventListener('input', (e) => {
            this.speed = parseInt(e.target.value);
            document.getElementById('speed-value').textContent = this.speed + 'x';
        });

        // Initialize
        this.updateScenarioDescription();
        this.updateStats();
    }

    changeScenario(scenarioKey) {
        this.currentScenario = scenarioKey;
        this.updateScenarioDescription();
        if (this.isRunning) {
            this.reset();
        }
    }

    changeController(type) {
        this.controllerType = type;
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.controller === type);
        });
        if (this.isRunning) {
            this.reset();
        }
    }

    updateScenarioDescription() {
        const scenario = this.scenarios[this.currentScenario];
        const html = `
            <h3>${scenario.name}</h3>
            <p>${scenario.description}</p>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin-top: 1rem;">
                <div><strong>North:</strong> ${scenario.arrivalRates.north} veh/min</div>
                <div><strong>South:</strong> ${scenario.arrivalRates.south} veh/min</div>
                <div><strong>East:</strong> ${scenario.arrivalRates.east} veh/min</div>
                <div><strong>West:</strong> ${scenario.arrivalRates.west} veh/min</div>
            </div>
        `;
        document.getElementById('scenario-description').innerHTML = html;
    }

    start() {
        this.isRunning = true;
        this.isPaused = false;
        document.getElementById('btn-start').disabled = true;
        document.getElementById('btn-pause').disabled = false;
        this.lastUpdate = Date.now();
        this.update();
    }

    pause() {
        this.isPaused = !this.isPaused;
        const btn = document.getElementById('btn-pause');
        btn.textContent = this.isPaused ? '▶ Resume' : '⏸ Pause';
        if (!this.isPaused) {
            this.lastUpdate = Date.now();
            this.update();
        }
    }

    reset() {
        this.isRunning = false;
        this.isPaused = false;
        this.simulationTime = 0;
        this.queues = { north: 0, south: 0, east: 0, west: 0 };
        this.totalVehicles = 0;
        this.totalWaitingTime = 0;
        this.departedVehicles = 0;
        this.phaseTime = 0;
        this.currentPhase = 'ns_green';

        document.getElementById('btn-start').disabled = false;
        document.getElementById('btn-pause').disabled = true;
        document.getElementById('btn-pause').textContent = '⏸ Pause';

        this.updateStats();
        this.updateLights();
        this.updateQueues();

        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
    }

    update() {
        if (!this.isRunning || this.isPaused) return;

        const now = Date.now();
        const deltaTime = (now - this.lastUpdate) / 1000 * this.speed;
        this.lastUpdate = now;

        this.simulationTime += deltaTime;
        this.phaseTime += deltaTime;

        // Generate arrivals
        this.generateArrivals(deltaTime);

        // Process traffic lights
        this.processTrafficLights();

        // Process departures
        this.processDepartures(deltaTime);

        // Update display
        this.updateStats();
        this.updateQueues();
        this.updateLights();

        // Continue animation
        this.animationFrame = requestAnimationFrame(() => this.update());
    }

    generateArrivals(deltaTime) {
        const scenario = this.scenarios[this.currentScenario];

        for (const direction in scenario.arrivalRates) {
            const rate = scenario.arrivalRates[direction] / 60; // Convert to per second
            const arrivals = Math.random() < (rate * deltaTime) ? 1 : 0;

            if (arrivals > 0) {
                this.queues[direction] += arrivals;
                this.totalVehicles += arrivals;
            }
        }
    }

    processTrafficLights() {
        // Get phase duration based on controller type
        let nextPhase = this.currentPhase;

        if (this.controllerType === 'fuzzy') {
            // Fuzzy logic: adapt based on queue lengths
            const nsQueue = this.queues.north + this.queues.south;
            const ewQueue = this.queues.east + this.queues.west;

            if (this.currentPhase === 'ns_green') {
                // Dynamic duration based on queue
                this.phaseDuration = 20 + Math.min(nsQueue * 2, 50);
                if (this.phaseTime >= this.phaseDuration) {
                    nextPhase = 'ns_yellow';
                    this.phaseTime = 0;
                    this.phaseDuration = 3;
                }
            } else if (this.currentPhase === 'ns_yellow') {
                if (this.phaseTime >= 3) {
                    nextPhase = 'all_red_1';
                    this.phaseTime = 0;
                    this.phaseDuration = 2;
                }
            } else if (this.currentPhase === 'all_red_1') {
                if (this.phaseTime >= 2) {
                    nextPhase = 'ew_green';
                    this.phaseTime = 0;
                    this.phaseDuration = 20 + Math.min(ewQueue * 2, 50);
                }
            } else if (this.currentPhase === 'ew_green') {
                if (this.phaseTime >= this.phaseDuration) {
                    nextPhase = 'ew_yellow';
                    this.phaseTime = 0;
                    this.phaseDuration = 3;
                }
            } else if (this.currentPhase === 'ew_yellow') {
                if (this.phaseTime >= 3) {
                    nextPhase = 'all_red_2';
                    this.phaseTime = 0;
                    this.phaseDuration = 2;
                }
            } else if (this.currentPhase === 'all_red_2') {
                if (this.phaseTime >= 2) {
                    nextPhase = 'ns_green';
                    this.phaseTime = 0;
                }
            }
        } else {
            // Fixed-time: 40s green for both
            if (this.currentPhase === 'ns_green' && this.phaseTime >= 40) {
                nextPhase = 'ns_yellow';
                this.phaseTime = 0;
            } else if (this.currentPhase === 'ns_yellow' && this.phaseTime >= 3) {
                nextPhase = 'all_red_1';
                this.phaseTime = 0;
            } else if (this.currentPhase === 'all_red_1' && this.phaseTime >= 2) {
                nextPhase = 'ew_green';
                this.phaseTime = 0;
            } else if (this.currentPhase === 'ew_green' && this.phaseTime >= 40) {
                nextPhase = 'ew_yellow';
                this.phaseTime = 0;
            } else if (this.currentPhase === 'ew_yellow' && this.phaseTime >= 3) {
                nextPhase = 'all_red_2';
                this.phaseTime = 0;
            } else if (this.currentPhase === 'all_red_2' && this.phaseTime >= 2) {
                nextPhase = 'ns_green';
                this.phaseTime = 0;
            }
        }

        this.currentPhase = nextPhase;
    }

    processDepartures(deltaTime) {
        const departureRate = 2; // vehicles per second when green

        if (this.currentPhase === 'ns_green') {
            const nsDepart = Math.min(this.queues.north, deltaTime * departureRate);
            const ssDepart = Math.min(this.queues.south, deltaTime * departureRate);

            this.queues.north -= nsDepart;
            this.queues.south -= ssDepart;
            this.departedVehicles += nsDepart + ssDepart;
            this.totalWaitingTime += (nsDepart + ssDepart) * this.simulationTime * 0.1;
        } else if (this.currentPhase === 'ew_green') {
            const ewDepart = Math.min(this.queues.east, deltaTime * departureRate);
            const wwDepart = Math.min(this.queues.west, deltaTime * departureRate);

            this.queues.east -= ewDepart;
            this.queues.west -= wwDepart;
            this.departedVehicles += ewDepart + wwDepart;
            this.totalWaitingTime += (ewDepart + wwDepart) * this.simulationTime * 0.1;
        }
    }

    updateStats() {
        document.getElementById('stat-time').textContent = Math.floor(this.simulationTime) + 's';
        document.getElementById('stat-vehicles').textContent = Math.floor(this.totalVehicles);

        const avgWaiting = this.departedVehicles > 0
            ? this.totalWaitingTime / this.departedVehicles
            : 0;
        document.getElementById('stat-waiting').textContent = avgWaiting.toFixed(1) + 's';

        const totalQueue = this.queues.north + this.queues.south +
                          this.queues.east + this.queues.west;
        document.getElementById('stat-queue').textContent = Math.floor(totalQueue);
    }

    updateQueues() {
        document.querySelector('.count-north').textContent = '🚗 ' + Math.floor(this.queues.north);
        document.querySelector('.count-south').textContent = '🚗 ' + Math.floor(this.queues.south);
        document.querySelector('.count-east').textContent = '🚗 ' + Math.floor(this.queues.east);
        document.querySelector('.count-west').textContent = '🚗 ' + Math.floor(this.queues.west);

        // Render vehicles visually
        this.renderVehicles();
    }

    renderVehicles() {
        const directions = ['north', 'south', 'east', 'west'];

        directions.forEach(direction => {
            const container = document.getElementById(`vehicles-${direction}`);
            container.innerHTML = '';

            const count = Math.min(Math.floor(this.queues[direction]), 10); // Max 10 visible
            const positions = this.getVehiclePositions(direction, count);

            for (let i = 0; i < count; i++) {
                const vehicle = document.createElement('div');
                vehicle.className = `vehicle ${direction}`;
                vehicle.style.left = positions[i].x + 'px';
                vehicle.style.top = positions[i].y + 'px';
                container.appendChild(vehicle);
            }
        });
    }

    getVehiclePositions(direction, count) {
        const positions = [];
        const spacing = 30;

        for (let i = 0; i < count; i++) {
            let pos = { x: 0, y: 0 };

            switch(direction) {
                case 'north':
                    pos = { x: 240, y: 180 - (i * spacing) };
                    break;
                case 'south':
                    pos = { x: 240, y: 320 + (i * spacing) };
                    break;
                case 'east':
                    pos = { x: 320 + (i * spacing), y: 240 };
                    break;
                case 'west':
                    pos = { x: 180 - (i * spacing), y: 240 };
                    break;
            }

            positions.push(pos);
        }

        return positions;
    }

    updateLights() {
        // Determine which light should be active for each direction
        const lights = {
            north: 'red',
            south: 'red',
            east: 'red',
            west: 'red'
        };

        if (this.currentPhase === 'ns_green') {
            lights.north = 'green';
            lights.south = 'green';
        } else if (this.currentPhase === 'ns_yellow') {
            lights.north = 'yellow';
            lights.south = 'yellow';
        } else if (this.currentPhase === 'ew_green') {
            lights.east = 'green';
            lights.west = 'green';
        } else if (this.currentPhase === 'ew_yellow') {
            lights.east = 'yellow';
            lights.west = 'yellow';
        }

        // Update all traffic lights (3 per direction)
        document.querySelectorAll('.traffic-light').forEach(lightEl => {
            const direction = lightEl.dataset.direction;
            const color = lightEl.dataset.color;
            const isActive = lights[direction] === color;

            if (isActive) {
                lightEl.classList.add('active', color);
            } else {
                lightEl.classList.remove('active', 'red', 'yellow', 'green');
            }
        });
    }
}

// Initialize demo when page loads
document.addEventListener('DOMContentLoaded', () => {
    new TrafficDemo();
});

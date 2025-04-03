import { Component, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

class TimerWidget extends Component {
    static template = "custom_timer_widget";
    
    constructor() {
        super(...arguments);
        this.state = useState({
            timeLeft: 0,
            intervalId: null,
            isRunning: false,
        });
    }

    startTimer() {
        if (this.state.isRunning) return; // Prevent starting multiple intervals
        this.state.isRunning = true;

        const intervalId = setInterval(() => {
            if (this.state.timeLeft <= 0) {
                clearInterval(this.state.intervalId);
                this.state.isRunning = false;
                document.getElementById("display").innerText = "EXPIRED";
            } else {
                this.state.timeLeft -= 1;
                this.updateDisplay();
            }
        }, 1000);

        this.state.intervalId = intervalId;
    }

    stopTimer() {
        clearInterval(this.state.intervalId);
        this.state.isRunning = false;
    }

    resetTimer() {
        this.stopTimer();
        this.state.timeLeft = 0;
        this.updateDisplay();
    }

    updateDisplay() {
        const days = Math.floor(this.state.timeLeft / (60 * 60 * 24));
        const hours = Math.floor((this.state.timeLeft % (60 * 60 * 24)) / (60 * 60));
        const minutes = Math.floor((this.state.timeLeft % (60 * 60)) / 60);
        const seconds = Math.floor(this.state.timeLeft % 60);

        document.getElementById("display").innerText = 
            `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }

    setTimer() {
        // Example: Set timer for 1 day, 1 hour, 1 minute, and 10 seconds
        const totalSeconds = (1 * 24 * 60 * 60) + (1 * 60 * 60) + (1 * 60) + 10;
        this.state.timeLeft = totalSeconds;
        this.updateDisplay();
    }

    mounted() {
        this.setTimer();
    }
}

export const timer_id = {
    component: TimerWidget,
    supportedType: ["char"]
}

registry.category("fields").add("custom_timer_widget", timer_id);8
<templates>
    <t t-name="custom_timer_widget">
        <div class="stopwatch">
            <div id="display">Loading...</div>
            <button id="startBtn" t-on-click="startTimer">Start</button>
            <button id="stopBtn" t-on-click="stopTimer">Stop</button>
            <button id="resetBtn" t-on-click="resetTimer">Reset</button>
        </div>
    </t>
</templates>

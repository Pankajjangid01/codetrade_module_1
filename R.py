<templates>
    <t t-name="custom_timer_widget">
        <div class="stopwatch">
            <div>
                <input type="number" name="hours" placeholder="HH" t-on-input="onInputChange"/>
                <input type="number" name="minutes" placeholder="MM" t-on-input="onInputChange"/>
                <input type="number" name="seconds" placeholder="SS" t-on-input="onInputChange"/>
                <button t-on-click="setTimer">Set Timer</button>
            </div>
            <div id="display">00h : 00m : 00s</div>
            <button t-on-click="startTimer">Start</button>
            <button t-on-click="stopTimer">Stop</button>
            <button t-on-click="resetTimer">Reset</button>
        </div>
    </t>
</templates>

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
            hours: 0,
            minutes: 0,
            seconds: 0,
        });
    }

    startTimer() {
        if (this.state.isRunning || this.state.timeLeft <= 0) return;

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
        const hours = Math.floor(this.state.timeLeft / 3600);
        const minutes = Math.floor((this.state.timeLeft % 3600) / 60);
        const seconds = this.state.timeLeft % 60;

        document.getElementById("display").innerText = 
            `${hours.toString().padStart(2, '0')}h : ${minutes.toString().padStart(2, '0')}m : ${seconds.toString().padStart(2, '0')}s`;
    }

    setTimer() {
        const hours = parseInt(this.state.hours) || 0;
        const minutes = parseInt(this.state.minutes) || 0;
        const seconds = parseInt(this.state.seconds) || 0;

        this.state.timeLeft = (hours * 3600) + (minutes * 60) + seconds;
        this.updateDisplay();
    }

    onInputChange(event) {
        const { name, value } = event.target;
        this.state[name] = value;
    }
}

export const timer_id = {
    component: TimerWidget,
    supportedType: ["char"]
}

registry.category("fields").add("custom_timer_widget", timer_id);

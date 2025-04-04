import { Component, useState, onWillUpdateProps, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";

// Store timers globally for persistence
const globalTimers = new Map();

export class TimerWidget extends Component {
    static template = "timer_widget";

    setup() {
        const recordId = this.props.record.resId; // Unique ID for each record

        // Load timer state from globalTimers if it exists, otherwise initialize
        if (globalTimers.has(recordId)) {
            this.state = globalTimers.get(recordId);
        } else {
            this.state = useState({ seconds: 0, isRunning: false });
            globalTimers.set(recordId, this.state);
        }

        this.interval = null;

        // Resume timer if it was running previously
        if (this.state.isRunning) {
            this.startTimer();
        }

        onWillUpdateProps(() => {
            if (recordId !== this.props.record.resId) {
                this.stopTimer(); // Stop timer when switching records
            }
        });

        onWillUnmount(() => {
            this.stopTimer(); // Ensure cleanup when the component is destroyed
        });
    }

    startTimer() {
        if (!this.state.isRunning) {
            this.state.isRunning = true;
            this.interval = setInterval(() => {
                this.state.seconds++;
            }, 1000);
        }
    }

    stopTimer() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
        this.state.isRunning = false;
    }

    get formattedTime() {
        const hours = Math.floor(this.state.seconds / 3600);
        const minutes = Math.floor((this.state.seconds % 3600) / 60);
        const seconds = this.state.seconds % 60;
        return `${hours}:${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
}

export const custom_timer = {
    component: TimerWidget,
    supportedType: ["char"]
}

registry.category("fields").add("timer_widget", custom_timer);

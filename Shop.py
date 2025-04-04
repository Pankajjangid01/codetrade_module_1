import { Component, useState, onWillUpdateProps, onWillUnmount, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";

const globalTimers = new Map();

class TimerWidget extends Component {
    static template = "timer_widget";

    setup() {
        const recordId = this.props.record.resId;

        if (globalTimers.has(recordId)) {
            const savedState = globalTimers.get(recordId);
            this.state = useState(savedState.state);

            if (savedState.interval) {
                this.interval = savedState.interval;
                this.startTimer(true); // Continue the timer if it was already running
            }
        } else {
            this.state = useState({ seconds: 0, isRunning: false });
            globalTimers.set(recordId, { state: this.state, interval: null });
        }

        onWillUpdateProps(() => {
            this.resetTimer();
        });

        onWillUnmount(() => {  
            globalTimers.set(recordId, { state: this.state, interval: this.interval });
            if (this.interval) clearInterval(this.interval); // Clear interval to avoid memory leak
        });
    }

    startTimer(resume = false) {
        if (!this.state.isRunning || resume) {
            this.state.isRunning = true;
            this.interval = setInterval(() => {
                this.state.seconds++;
                this.render(); // Force re-render to update UI
            }, 1000);

            globalTimers.set(this.props.record.resId, { state: this.state, interval: this.interval });
        }
    }

    stopTimer() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
        this.state.isRunning = false;
        this.render(); // Force re-render to update UI
    }

    resetTimer() {
        this.stopTimer();
        this.state.seconds = 0;
        this.state.isRunning = false;
        globalTimers.get(this.props.record.resId).interval = null;
        this.render(); // Ensure UI is updated
    }

    get formattedTime() {
        const hours = Math.floor(this.state.seconds / 3600);
        const minutes = Math.floor((this.state.seconds % 3600) / 60);
        const seconds = this.state.seconds % 60;
        return `${hours < 10 ? '0' : ''}${hours}:${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
}

export const custom_timer = {
    component: TimerWidget,
    supportedType: ["char"]
}

registry.category("fields").add("timer_widget", custom_timer);

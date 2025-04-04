import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class TimerWidget extends Component {
    static template = "timer_widget";

    setup() {
        this.state = useState({ seconds: 0, isRunning: false });
        this.interval = null;

        // Reset timer state when a new record is created
        onWillUpdateProps(() => {
            this.resetTimer();
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
            this.state.isRunning = false;
        }
    }

    resetTimer() {
        this.stopTimer();
        this.state.seconds = 0;
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

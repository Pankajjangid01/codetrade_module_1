import { Component, useState, onWillUpdateProps, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";

const globalTimers = new Map();

class TimerWidget extends Component {
    static template = "timer_widget";

    setup() {
        const recordId = this.props.record.resId;

        if (globalTimers.has(recordId)) {
            const savedState = globalTimers.get(recordId);
            this.state = savedState.state;

            // Agar interval already chal raha hai toh usko dobara start karna
            if (savedState.interval) {
                this.interval = savedState.interval;
                this.startTimer(true); // true se indicate karenge ki naye interval ko create na kare
            }
        } else {
            this.state = useState({ seconds: 0, isRunning: false });
            globalTimers.set(recordId, { state: this.state, interval: null });
        }

        onWillUpdateProps(() => {
            this.resetTimer();
        });

        onWillUnmount(() => {
            globalTimers.set(recordId, { state: this.state, interval: this.interval }); // Interval ko bhi save karte hain
        });
    }

    startTimer(restore = false) {
        if (!this.state.isRunning || restore) {
            this.state.isRunning = true;
            
            if (!restore) { // Agar naye se start ho raha hai tabhi naye interval set kare
                this.interval = setInterval(() => {
                    this.state.seconds++;
                }, 1000);

                globalTimers.get(this.props.record.resId).interval = this.interval; // Interval ko save karte hain
            }
        }
    }

    stopTimer() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
        this.state.isRunning = false;
    }

    resetTimer() {
        this.stopTimer();
        this.state.seconds = 0;
        this.state.isRunning = false;
        globalTimers.get(this.props.record.resId).interval = null; // Interval reset
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

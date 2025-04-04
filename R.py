/** static/src/js/timer_widget.js **/

import { Component, useState, onWillUnmount, onMounted } from "@odoo/owl";
import fieldRegistry from "@web/fields/field_registry";

export class TimerWidget extends Component {
    setup() {
        this.state = useState({ seconds: 0, isRunning: false });
        this.interval = null;

        onMounted(() => {
            if (this.state.isRunning) {
                this.startTimer();
            }
        });

        onWillUnmount(this.stopTimer.bind(this));
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

    get formattedTime() {
        const minutes = Math.floor(this.state.seconds / 60);
        const seconds = this.state.seconds % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
}

TimerWidget.template = `
    <div>
        <div style="font-size: 20px; margin-bottom: 10px;">
            Time: <span><t t-esc="this.formattedTime"/></span>
        </div>
        <div>
            <button t-on-click="startTimer" t-if="!this.state.isRunning" class="btn btn-primary">Start</button>
            <button t-on-click="stopTimer" t-if="this.state.isRunning" class="btn btn-secondary">Stop</button>
        </div>
    </div>
`;

fieldRegistry.add("timer_widget", TimerWidget);

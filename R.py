import { Component, useState} from "@odoo/owl";
import { registry } from "@web/core/registry";

export class TimerWidget extends Component {
    static template = "timer_widget";
    setup() {
        this.state = useState({ seconds: 0, isRunning: false });
        this.interval = null;
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
        const hours = Math.floor(this.state.seconds / 3600)
        const minutes = Math.floor(this.state.seconds / 60);
        const seconds = this.state.seconds % 60;
        return `${hours}${hours}:${minutes < 10 ? '0':''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
}

export const custom_timer = {
    component: TimerWidget,
    supportedType : ["char"]
}

registry.category("fields").add("timer_widget",custom_timer);

<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="timer_widget">
        <div class="d-flex">
            <input id="display" type="text" t-model="props.record.data[props.name]" style="border:none;input[type=text]:focus{border: none;};width:30%"/>
            <div style="font-size: 20px; margin-bottom: 10px;">
                <span><t t-esc="this.formattedTime"/></span>
            </div>
            <div>
                <button t-on-click="startTimer" t-if="!this.state.isRunning" class="btn btn-primary">Start</button>
                <button t-on-click="stopTimer" t-if="this.state.isRunning" class="btn btn-secondary">Stop</button>
            </div>
        </div>
    </t>
</templates>

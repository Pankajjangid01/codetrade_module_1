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

            
            if (savedState.interval) {
                this.interval = savedState.interval;
                this.startTimer(); 
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

    resetTimer() {
        this.stopTimer();
        this.state.seconds = 0;
        this.state.isRunning = false;
        globalTimers.get(this.props.record.resId).interval = null;
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


// in this code initiallly when i open any record and start the timer start button changes to stop and timer start but when i go back to list view and then com back to that record form
// then the timer is not running on ui but in backend it is running means ui not updating and when i click the stop button it change to start but not update on ui means my form ui not updating 

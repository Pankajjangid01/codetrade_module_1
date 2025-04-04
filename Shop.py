import { Component, useState, onWillUpdateProps, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";

const globalTimers = new Map();

class TimerWidget extends Component {
    static template = "timer_widget";

    setup() {
        const recordId = this.props.record.resId;

        if (globalTimers.has(recordId)) {
            this.state = globalTimers.get(recordId);
        } else {
            this.state = useState({ seconds: 0, isRunning: false });
            globalTimers.set(recordId, this.state);
        }

        this.interval = null;

        if (this.state.isRunning) {
            this.startTimer();
        }

        onWillUpdateProps(() => {
            this.resetTimer();
        });

        onWillUnmount(() => {
            this.stopTimer(); 
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
// <?xml version="1.0" encoding="UTF-8"?>
// <templates xml:space="preserve">
//     <t t-name="timer_widget">
//         <div class="d-flex">
//             <input id="display" type="text" t-model="props.record.data[props.name]" style="border:none;input[type=text]:focus{border: none;};width:30%"/>
//             <div style="font-size: 20px; margin-bottom: 10px;">
//                 <span><t t-esc="this.formattedTime"/></span>
//             </div>
//             <div>
//                 <button t-on-click="startTimer" t-if="!this.state.isRunning" class="btn btn-primary">Start</button>
//                 <button t-on-click="stopTimer" t-if="this.state.isRunning" class="btn btn-secondary">Stop</button>
//             </div>
//         </div>
//     </t>
// </templates>
// abhi mai from view se list mai jaa rha hu toh time ruk jata hai but mujhe time nhi rokna uss record ka vo chalta rhna chachiye or hab wapas uss record ka form kholu toh ui bhi update hona chachiye jese initially hota hai 

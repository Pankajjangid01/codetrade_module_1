import { Component, xml,useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class TimerWidget extends Component {
    static template = "custom_timer_widget";

    countDownDate = new Date("Jan 5, 2030 15:37:25").getTime();
    x = setInterval(function() {
    var now = new Date().getTime();
    var distance = countDownDate - now;
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    document.getElementById("demo").innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("demo").innerHTML = "EXPIRED";
    }
    }, 1000);
}

export const timer_id = {
    component:TimerWidget,
    supportedType:["char"]
}

registry.category("fields").add("custom_timer_widget", timer_id);
<templates>
    <t t-name="custom_timer_widget">
        <div class="stopwatch">
            <div id="display">00:00:00</div>
            <button id="startBtn">Start</button>
            <button id="stopBtn">Stop</button>
            <button id="resetBtn">Reset</button>
        </div>
    </t>
</templates>
i want to set the timer value and then the timer will start from there how can i do it in odoo 18 using js 

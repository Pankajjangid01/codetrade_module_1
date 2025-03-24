import { FormController } from "@web/views/form/form_controller";
import { formView } from '@web/views/form/form_view';
import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";

export class HrFormController extends FormController{

    setup() {
        super.setup();
        this.actionService = useService("action");
    }
    OnTestClick() {
        console.log("---------------------Testing-----------------------------")
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'office.register',
            name:'Open Wizard',
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_id: false,
        });
    }
}
HrFormController.template = 'json_button_test';

export const modelInfoView = {
    ...formView,
    Controller: HrFormController,
};
registry.category("views").add("button_in_form", modelInfoView);
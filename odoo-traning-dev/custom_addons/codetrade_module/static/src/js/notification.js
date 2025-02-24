import { FormController } from "@web/views/form/form_controller";
import { formView } from '@web/views/form/form_view';
import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class EmployeeFormController extends FormController{

    setup() {
        super.setup();
        this.actionService = useService("action");
        this.notification = useService("notification")
    }
    
    async onSaveButton(record) {
        console.log("---------------------Testing-----------------------------")
        await this.operations._onSave(record).then((record)=>{this.notification.add(
            _t("Message detail."), 
            { 
                title: _t("Record saved successfully"), 
                type: "success", 
                sticky: false
            }
        );})
        
    }
}
EmployeeFormController.template = 'save_button_test';

export const modelInfoView = {
    ...formView,
    Controller: EmployeeFormController,
};
registry.category("views").add("button_in_employee_form", modelInfoView);
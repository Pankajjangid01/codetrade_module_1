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
        this.orm = useService("orm");
    }
    
    async onSaveButton(data) {
        console.log("---------------------Testing-----------------------------")
        return this.orm.call("company.employee", "create",["data",{
            email:"pankaj@gmail.com",
            contact:6377589985,
            name:"Pankaj"
        }]);

        // await this.notification.add(
        //     _t("Message detail."), 
        //     { 
        //         title: _t("Record saved successfully"), 
        //         type: "success", 
        //         sticky: false
        //     }
        // );
        
    }
}
EmployeeFormController.template = 'save_button_test';

export const modelInfoView = {
    ...formView,
    Controller: EmployeeFormController,
};
registry.category("views").add("button_in_employee_form", modelInfoView);
//  error-->>File "/usr/lib/python3/dist-packages/odoo/api.py", line 517, in call_kw
//     result = getattr(recs, name)(*args, **kwargs)
//     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
// TypeError: create() takes 2 positional arguments but 3 were given


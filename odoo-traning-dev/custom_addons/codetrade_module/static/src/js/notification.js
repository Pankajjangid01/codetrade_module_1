import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class EmployeeFormController extends FormController {
    setup() {
        super.setup();
        this.notification = useService("notification");
        this.orm = useService("orm");
    }

    async onRecordSave(record) {
        console.log("Overriding onRecordSave...");

        try {
            const result = await super.onRecordSave(record); // Calls the original save method

            this.notification.add(_t("Employee record saved successfully!"), {
                title: _t("Success"),
                type: "success",
            });

            return result;
        } catch (error) {
            this.notification.add(_t("Error saving employee record."), { type: "danger" });
            console.error("Error saving record:", error);
            throw error;
        }
    }
}

EmployeeFormController.template = "save_button_test";

export const modelInfoView = {
    ...formView,
    Controller: EmployeeFormController,
};

registry.category("views").add("button_in_employee_form", modelInfoView);

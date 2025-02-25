import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { redirect } from "@web/core/utils/urls";

export class EmployeeFormController extends FormController {
    setup() {
        super.setup();
        this.notification = useService("notification");
        this.orm = useService("orm");
    }

    async onRecordSaved(record) {
        console.log("Overriding onRecordSave...");
        try {
            const result = await super.onRecordSaved(record);
            console.log("Printing result data------>>>>>>>",result)
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

    async onSaveButton() {
        console.log("Fetching form data...");
        const recordData = this.model.root.data;
        const params={
            name:recordData.name,
            contact : recordData.contact,
            email : recordData.email,
            employee_id : recordData.employee_id,
            salary : recordData.salary,
            tech_stack : recordData.tech_stack,
            image : recordData.image,
            joining_date : recordData.joining_date,
            address : recoradData.address,
        }
        console.log("printing record data--->>>",typeof(params))
        debugger;
        if (!recordData.email || !recordData.contact || !recordData.name) {
            this.notification.add(_t("All fields are required!"), { type: "danger" });
                return;
            }

        try {
            const record = this.orm.call("company.employee", "create", [params]);
            console.log("Record data ------>>>>>",record)

            this.notification.add(("Record saved successfully!"), {
                title: ("Success"),
                    type: "success",
                });

            record.then((response)=>{
                console.log("printing response",response)
                redirect("/odoo/action-602/"+response)
            })

        } catch (error) {
            this.notification.add(("Error saving record."), { type: "danger" });
                console.error("Error creating record:", error);
        }
    }
}

EmployeeFormController.template = "save_button_test";

export const modelInfoView = {
    ...formView,
    Controller: EmployeeFormController,
};

registry.category("views").add("button_in_employee_form", modelInfoView);
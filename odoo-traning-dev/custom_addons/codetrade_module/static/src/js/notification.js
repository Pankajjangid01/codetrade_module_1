export class EmployeeFormController extends FormController {
    setup() {
        super.setup();
        this.actionService = useService("action");
        this.notification = useService("notification");
        this.orm = useService("orm");
    }

    async onSaveButton() {
        console.log("Fetching form data...");

        // Fetch form data dynamically
        const recordData = this.model.root.data;

        if (!recordData.email || !recordData.contact || !recordData.name) {
            this.notification.add(_t("All fields are required!"), { type: "danger" });
            return;
        }

        try {
            await this.orm.call("company.employee", "create", [recordData]);

            this.notification.add(_t("Record saved successfully!"), {
                title: _t("Success"),
                type: "success",
            });

        } catch (error) {
            this.notification.add(_t("Error saving record."), { type: "danger" });
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






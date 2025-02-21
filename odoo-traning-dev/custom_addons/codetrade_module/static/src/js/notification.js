import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
class SomeComponent extends Component {
    onButtonClick(){
    this.notification.add({
        title: _t("Success"),
        message: _t("Your signature request has been sent.")
    });}
}
registry.category("action").add("company_employee_form",SomeComponent)
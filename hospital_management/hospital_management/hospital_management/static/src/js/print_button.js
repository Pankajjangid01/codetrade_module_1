import { ListController } from "@web/views/list/list_controller";
import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";

export class PrintController extends ListController {
    setup() {
        super.setup();
    }
}

PrintController.template = "print_button_test";

registry.category("views").add("print_button_in_list", {
    ...listView,
    Controller: PrintController,
 });
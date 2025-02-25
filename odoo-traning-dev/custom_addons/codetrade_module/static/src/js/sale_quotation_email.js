import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { redirect } from "@web/core/utils/urls";

export class SaleQuotationController extends FormController {
    setup() {
        super.setup();
        this.notification = useService("notification");
        this.orm = useService("orm");
    }

    async onRecordSaved(record) {
        console.log("Overriding onRecordSave...");
        try {
            const result = await super.onRecordSaved(record);
            const recordData = this.props.resId;

            // Get the PDF report action URL
            const pdfAction = await this.orm.call('sale.order', 'action_download_invoice', [recordData]);

            console.log("Generated PDF action:", pdfAction);

            // Redirect to download the report
            if (pdfAction && pdfAction.report_type === 'qweb-pdf') {
                const downloadUrl = `/report/pdf/${pdfAction.report_name}/${recordData}`;
                window.open(downloadUrl, '_blank'); // Open the PDF in a new tab
            }

            // Send notification
            await this.orm.call('sale.order', 'display_notification', [recordData]);
            this.notification.add(_t("Sale Quotation created successfully!"), {
                title: _t("Success"),
                type: "success",
            });

            return result;
        } catch (error) {
            this.notification.add(_t("Error saving sale record."), { type: "danger" });
            console.error("Error saving record:", error);
            throw error;
        }
    }
}

export const modelInfoView = {
    ...formView,
    Controller: SaleQuotationController,
};

registry.category("views").add("button_in_sale_quotation_form", modelInfoView);

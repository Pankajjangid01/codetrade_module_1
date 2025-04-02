<?xml version="1.0" encoding="UTF-8"?>
<template xml:space="preserve">
    <t t-name="filter_assessment_button">
        <button t-if='widget.modelName == "hms.patient"' type="button" class="btn btn-secondary oe_new_custom_button">
            Patient Assessments
        </button>
    </t>
    <t t-extend="KanbanView.buttons">
        <t t-jquery="button[class='open_custom_wizard']" t-operation="after">
            <t t-call="filter_assessment_button" />
        </t>
    </t>
</template>
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <template id="assets_backend" name="saned_custome_assets" inherit_id="web.assets_backend">
            <xpath expr="." position="inside">
                <script type="text/javascript" src="/saned_custome/static/src/js/add_assessment_button.js"></script>
            </xpath>
        </template>
    </data>
</odoo>
<?xml version="1.0" encoding="UTF-8"?>
<template xml:space="preserve">
    <t t-name="verified_patient_button">
        <button t-if='widget and widget.verified_patient or widget and widget.verified_case_patient' type="button" class="btn btn-secondary open_custom_wizard">
            Verify Patient
        </button>
    </t>
    <t t-extend="KanbanView.buttons">
        <t t-jquery="button" t-operation="after">
            <t t-call="verified_patient_button" />
        </t>
    </t>
    <t t-extend="ListView.buttons">
        <t t-jquery="div.o_list_buttons" t-operation="append">
            <t t-call="verified_patient_button"/>
        </t>
    </t>
</template>
<?xml version="1.0" encoding="utf-8"?>
<odoo>

        <template id="assets_backend" inherit_id="web.assets_backend">
            <xpath expr="." position="inside">
                <script type="text/javascript" src="/saned_patient_details/static/src/js/vertical_page.js"/>
                <script type="text/javascript" src="/saned_patient_details/static/src/js/custom_button.js"/>
                <link rel="stylesheet" type="text/css" href="/saned_patient_details/static/src/css/vertical_pages.css"/>
            </xpath>
        </template>

</odoo>

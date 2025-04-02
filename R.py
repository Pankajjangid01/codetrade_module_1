<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data>
        <!-- JavaScript and CSS Assets -->
        <template id="assets_backend" name="saned_custome_assets" inherit_id="web.assets_backend">
            <xpath expr="." position="inside">
                <script type="text/javascript" src="/saned_custome/static/src/js/add_assessment_button.js"></script>
                <script type="text/javascript" src="/saned_patient_details/static/src/js/vertical_page.js"/>
                <script type="text/javascript" src="/saned_patient_details/static/src/js/custom_button.js"/>
                <link rel="stylesheet" type="text/css" href="/saned_patient_details/static/src/css/vertical_pages.css"/>
            </xpath>
        </template>
        
        <!-- Verify Patient Button -->
        <template id="verified_patient_button" name="Verified Patient Button">
            <button t-if='widget and (widget.verified_patient or widget.verified_case_patient)' type="button" class="btn btn-secondary open_custom_wizard">
                Verify Patient
            </button>
        </template>
        
        <!-- Patient Assessments Button -->
        <template id="filter_assessment_button" name="Patient Assessment Button">
            <button t-if='widget.modelName == "hms.patient"' type="button" class="btn btn-secondary oe_new_custom_button">
                Patient Assessments
            </button>
        </template>
        
        <!-- Extend KanbanView.buttons -->
        <template inherit_id="KanbanView.buttons">
            <xpath expr="//button[@class='open_custom_wizard']" position="after">
                <t t-call="filter_assessment_button"/>
            </xpath>
        </template>
        
        <!-- Extend ListView.buttons -->
        <template inherit_id="ListView.buttons">
            <xpath expr="//div[@class='o_list_buttons']" position="append">
                <t t-call="verified_patient_button"/>
                <t t-call="filter_assessment_button"/>
            </xpath>
        </template>
    </data>
</odoo>

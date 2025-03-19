<odoo>
    <!-- Student Tree View -->
    <record id="view_school_student_tree" model="ir.ui.view">
        <field name="name">school.student.tree</field>
        <field name="model">school.student</field>
        <field name="arch" type="xml">
            <tree string="Students">
                <field name="name"/>
            </tree>
        </field>
    </record>

    <!-- Student Form View -->
    <record id="view_school_student_form" model="ir.ui.view">
        <field name="name">school.student.form</field>
        <field name="model">school.student</field>
        <field name="arch" type="xml">
            <form string="Student">
                <sheet>
                    <group>
                        <field name="name"/>
                    </group>
                    <notebook>
                        <page string="Subjects">
                            <field name="subject_ids">
                                <tree editable="bottom">
                                    <field name="name"/>
                                    <field name="marks"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Subject Tree View -->
    <record id="view_school_subject_tree" model="ir.ui.view">
        <field name="name">school.subject.tree</field>
        <field name="model">school.subject</field>
        <field name="arch" type="xml">
            <tree string="Subjects">
                <field name="name"/>
                <field name="marks"/>
                <field name="student_id"/>
            </tree>
        </field>
    </record>

    <!-- Subject Form View -->
    <record id="view_school_subject_form" model="ir.ui.view">
        <field name="name">school.subject.form</field>
        <field name="model">school.subject</field>
        <field name="arch" type="xml">
            <form string="Subject">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="marks"/>
                        <field name="student_id"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Actions -->
    <record id="action_school_student" model="ir.actions.act_window">
        <field name="name">Students</field>
        <field name="res_model">school.student</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_school_subject" model="ir.actions.act_window">
        <field name="name">Subjects</field>
        <field name="res_model">school.subject</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>

<odoo>
    <menuitem id="school_management_menu_root" name="School Management"/>

    <menuitem id="menu_school_students" name="Students"
              parent="school_management_menu_root"
              action="action_school_student"/>

    <menuitem id="menu_school_subjects" name="Subjects"
              parent="school_management_menu_root"
              action="action_school_subject"/>
</odoo>

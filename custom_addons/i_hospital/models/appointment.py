from odoo import api,fields,models


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit=['mail.thread']
    _description = 'Hospital Appointment'
    _rec_names_search = ['reference', 'patient_id']
    _rec_name = 'patient_id'

    reference = fields.Char(string="Reference",default="New")
    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete='restrict') #ondelete="cascade", ondelete="set null"
    #date_appointment = fields.Date(string="Date")
    phone = fields.Char(string="Mobile")
    date_time = fields.Datetime(string="Date & Time")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    note = fields.Text(string="Note")
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('ongoing','Ongoing'),
                              ('done','Done'),('cancel','Cancelled')], default='draft',tracking=True)
    appointment_line_ids = fields.One2many('hospital.appointment.line','appointment_id',string='Lines')
    # naming convention should be like _compute_field_name
    #total_qty = fields.Float(compute='_compute_total_qty', string='Total Quantity', store=True)
    date_of_birth = fields.Date(related='patient_id.date_of_birth', store=True)

    # @api.depends('appointment_line_ids','appointment_line_ids.qty')
    # def _compute_total_qty(self):
    #     # Method 1
    #     # for rec in self:
    #         # total_qty=0
    #         # for line in rec.appointment_line_ids:
    #         #     total_qty+=line.qty
    #         #     rec.total_qty=total_qty
    #     # Method 2
    #     for rec in self:
    #         rec.total_qty = sum(rec.appointment_line_ids.mapped('qty'))

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}] {rec.patient_id.name}"

    #inherited from models.Model..it creates a record inside postgres table based on value entered into form
    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            rec.state='confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state='ongoing'

    def action_done(self):
        for rec in self:
            rec.state='done'

    def action_cancel(self):
        for rec in self:
            rec.state='cancel'


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Lines'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    qty = fields.Float(string="Quantity")

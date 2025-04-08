from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit=['mail.thread']
    _description = 'Patient Master'

    #appointment_count_all = fields.Integer(string="Total Count", compute="total_counts")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')

    name = fields.Char(string="Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="DOB",tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender",tracking=True)
    tag_ids = fields.Many2many('patient.tag','patient_tag_rel','patient_id','tag_id', string='Tags')

    # Method 1
    #inheriting unlink (delete) method of hospital.patient model
    def unlink(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise UserError(_("You cannot delete patient now!\nAppointments existing for this patient: %s" % rec.name)) # _ is used for translation according to end user need
        return super().unlink()

    # Method 2
    # @api.ondelete(at_uninstall=False)
    # def check_patient_appointments(self):
    #     for rec in self:
    #         domain = [('patient_id', '=', rec.id)]
    #         appointments = self.env['hospital.appointment'].search(domain)
    #         if appointments:
    #             raise UserError(_("You cannot delete patient now!\nAppointments existing for this patient: %s" % rec.name))


    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     # for rec in self:
    #     #     rec.appointment_count = self.env['hospital.appointment'].search_count([
    #     #         ('patient_id','=', rec.id),
    #     #         ('state','not in',['cancel'])
    #     for record in self:
    #         record.id = len(record.appointment_count)
    #         #])

    # @api.depends('appointment_ids')
    # def total_counts(self):
    #     for r in :
    #         if r.appointment_ids:
    #             domain = [('id', 'in', r.patient_id)]
    #             appointment_count_all = self.env['hospital.patient'].search_count(domain)
    #             r.appointment_count_all = appointment_count_all
    #         else:
    #             r.appointment_count_all = 0

    # def total_counts(self):
    #     for r in self:
    #         r.appointment_count_all = self.env['hospital.patient'].count
    #
    # def action_view_appointments(self):
    #     #self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Appointments',
    #         'view_mode': 'tree,form',
    #         'res_model': 'hospital.appointment',
    #         'domain': [('patient_id','=', self.id)],
    #         'context': {'default_patient_id': self.id},
    #
    #     }
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Task'  # The display name in chatter and any place

    name = fields.Char('Task Name')
    due_date = fields.Date('Due Date')
    description = fields.Text()
    assign_to_ids = fields.Many2many('res.partner')  # from my own it was Many2one
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], default='new')
    estimated_time = fields.Float()
    total_time = fields.Float(compute='_compute_total_time', store=True)
    line_ids = fields.One2many('timesheet.line', 'todo_task_id')
    active = fields.Boolean(default=1)
    is_late = fields.Boolean()

    # @api.depends('line_ids.time_taken_per_line')
    # def _compute_total_time(self):
    #     """Compute total time by summing time_taken_per_line in related timesheet lines."""
    #     for rec in self:
    #         result = sum(line.time_taken_per_line for line in rec.line_ids)
    #         rec.total_time = result

    @api.depends('line_ids.time_taken_per_line')
    def _compute_total_time(self):
        """Compute total time by summing time_taken_per_line in related timesheet lines."""
        for rec in self:
            total_time = 0  # Start with zero total time
            for line in rec.line_ids:  # Go through each timesheet line
                total_time += line.time_taken_per_line  # Add the time for this line to the total
                rec.total_time = total_time  # Set the total time (this is for the outer or first for loop )



    @api.constrains('total_time')
    def _check_total_time(self):
        """Check if total_time exceeds estimated_time and raise ValidationError."""
        for rec in self:
            if rec.total_time > rec.estimated_time:
                raise ValidationError("Total time  exceeds the estimated time")






    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'


    def action_new(self):
        for rec in self:
            rec.state = 'new'


    def action_completed(TodoTask):
        for rec in TodoTask:
            rec.state = 'completed'

    def action_closed(TodoTask):
        for rec in TodoTask:
            rec.state = 'closed'

    def check_if_date_is_late(self):
        todo_task_ids = self.search([])  #todo_task_ids not defined before ?!! but lets try
        for rec in todo_task_ids:        # ماكتبناش in self لأنها فاضيه في وقت التعامل مع ال cron jobs
            if rec.due_date and rec.due_date < fields.date.today() and rec.state in ['new','in_progress']:
               rec.is_late = True


class TimesheetLine(models.Model):
    _name = "timesheet.line"
    todo_task_id = fields.Many2one('todo.task')
    description = fields.Text()
    date = fields.Date()
    time_taken_per_line = fields.Float()


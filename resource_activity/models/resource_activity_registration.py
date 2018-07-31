# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import pytz
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class ActivityRegistration(models.Model):
    _name = 'resource.activity.registration'

    def _get_activity_booking_type(self):
        if self.resource_activity_id.booking_type:
            self.booking_type = self.resource_activity_id.booking_type

    def _get_activity_activity_date_lock(self):
        if self.resource_activity_id.booking_type:
            self.booking_type = self.resource_activity_id.booking_type

    @api.onchange('resource_category')
    def onchange_resource_category(self):
        self.product_id = False

    @api.onchange('quantity')
    def onchange_quantity(self):
        if not self.bring_bike and self.state not in ['option', 'booked']:
            self.quantity_needed = self.quantity

    @api.onchange('quantity_needed')
    def onchange_quantity_needed(self):
        if self.state not in ['booked', 'option', 'draft']:
            if self.quantity_needed > self.quantity_allocated:
                self.state = 'waiting'

    @api.onchange('bring_bike')
    def onchange_bring_bike(self):
        if self.bring_bike:
            self.quantity_needed = 0
        else:
            self.quantity_needed = self.quantity

    @api.onchange('booking_type')
    def onchange_booking_type(self):
        if self.booking_type == 'booked':
            self.date_lock = None

    @api.multi
    @api.depends('quantity_needed', 'product_id', 'state')
    def _compute_need_push(self):
        for registration in self:
            if registration.resource_activity_id.sale_order_id or registration.sale_order_id:
                registration.need_push = True

    resource_activity_id = fields.Many2one('resource.activity',string="Activity")
    order_line_id = fields.Many2one(
        'sale.order.line',
        string="Sale order line")
    partner_id = fields.Many2one(
        related='resource_activity_id.partner_id')
    attendee_id = fields.Many2one(
        'res.partner',
        string="Attendee",
        domain=[('customer', '=', True)])
    sale_order_id = fields.Many2one(
        'sale.order',
        string="Sale order",
        readonly=True,
        copy=False)
    quantity = fields.Integer(
        string="Number of participant",
        default=1)
    quantity_needed = fields.Integer(
        string="Quantity needed",
        default=1)
    quantity_allocated = fields.Integer(
        string="Quantity allocated",
        readonly=True)
    product_id = fields.Many2one(
        'product.product',
        string="Product")
    resource_category = fields.Many2one(
        'resource.category',
        string="Category")
    resources_available = fields.One2many(
        'resource.available',
        'registration_id',
        string="Resource available")
    allocations = fields.One2many(
        'resource.allocation',
        'activity_registration_id',
        string="Activity registration")
    date_lock = fields.Date(
        string="Date lock")
    booking_type = fields.Selection(
        [('option', 'Option'), ('booked', 'Booking')],
        string="Booking type",
        required=True)
    state = fields.Selection(
        [('draft', 'Draft'),
          ('waiting', 'Waiting'),
          ('available', 'Available'),
          ('option', 'Option'),
          ('booked', 'Booked'),
          ('cancelled', 'Cancelled')],
        string="State",
        default='draft',
        readonly=True)

    # depends of the resource type
    date_start = fields.Datetime(
        related='resource_activity_id.resource_allocation_start',
        string="Date start")
    date_end = fields.Datetime(
        related='resource_activity_id.resource_allocation_end',
        string="Date end")
    location_id = fields.Many2one(
        related='resource_activity_id.location_id',
        string="Location")
    bring_bike = fields.Boolean(
        string="Bring his bike")
    registrations_max = fields.Integer(
        string="Maximum registration")
    registrations_expected = fields.Integer(
        string="Expected registration")
    activity_type = fields.Many2one(
        'resource.activity.type',
        string="Activity type")
    need_push = fields.Boolean(
        string="Need to be pushed to sales order",
        compute='_compute_need_push',
        store=True)

    def create_resource_available(self, resource_ids, registration):
        for resource_id in resource_ids:
            self.env['resource.available'].create({
                'resource_id': resource_id,
                'registration_id': registration.id,
                'state': 'free'})

    @api.multi
    def search_resources(self):
        registrations = self.filtered(lambda record: record.state in ['draft', 'waiting', 'available'])
        for registration in registrations:
            if registration.quantity_allocated < registration.quantity_needed:
                # delete free and unfree resource when running.
                res_to_delete = registration.resources_available.filtered(lambda record: record.state in ['free', 'not_free'])
                res_to_delete.unlink()
                if registration.resource_category:
                    # we complete with the group resources
                    cat_resource_ids = (
                        registration
                        .resource_category
                        .resources
                        .check_availabilities(registration.date_start,
                                              registration.date_end,
                                              registration.location_id)
                    )
                    self.create_resource_available(cat_resource_ids, registration)

                    if len(registration
                           .resources_available
                           .filtered(lambda record: record.state != 'cancelled')
                           ) >= registration.quantity_needed:
                        registration.state = 'available'
                    else:
                        registration.state = 'waiting'
                        self.env.cr.commit()
                        raise UserError(("Not enough resource found for the "
                                         "registration %s with category %s. "
                                         "%s resources found") %
                                            (registration.attendee_id.name,
                                             registration.resource_category.name,
                                             len(registration.resources_available)))

        return True

    @api.multi
    def action_refresh(self):
        for registration in self:
            resources_available = (
                registration
                .resources_available
                .filtered(lambda record: record.state == 'free')
            )
            still_avai_res = (
                resources_available
                .mapped('resource_id')
                .check_availabilities(registration.date_start,
                                      registration.date_end,
                                      registration.location_id)
            )
            for resource_available in resources_available:
                if resource_available.resource_id.id not in still_avai_res:
                    resource_available.state = 'not_free'
        return True

    @api.multi
    def reserve_needed_resource(self):
        for registration in self:
            qty_needed = registration.quantity_needed - registration.quantity_allocated
            free_resources = (
                registration
                .resources_available
                .filtered(lambda record: record.state == 'free')
            )
            for resource_available in free_resources:
                resource_available.action_reserve()
                qty_needed -= 1
                if qty_needed == 0:
                    break
            (registration
             .resource_activity_id
             .registrations.action_refresh())
        return True

    @api.multi
    def action_cancel(self):
        for registration in self:
            for resource_available in registration.resources_available:
                resource_available.action_cancel()
            registration.write({'state': 'cancelled', 'quantity_allocated': 0})

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_unlink(self):
        self.unlink()

    @api.multi
    def unlink(self):
        for registration in self:
            if registration.state not in ('draft', 'cancelled', 'free'):
                raise UserError(_('You cannot delete a registration which is '
                                  'not draft or cancelled. You should first '
                                  'cancel it.'))
        return super(ActivityRegistration, self).unlink()

    @api.multi
    @api.depends('quantity', 'quantity_allocated')
    def compute_state(self):
        for subscription in self:
            if self.quantity_allocated == self.quantity:
                self.state = self.booking_type
            elif self.state != 'draft' and self.quantity_allocated < self.quantity:
                self.state = 'waiting'

    @api.multi
    def view_registration_form(self):
        self.action_refresh()
        context = dict(self.env.context or {})
        context['active_id'] = self.id

        return {
            'name': 'view activity registration',
            'res_model': 'resource.activity.registration',
            'view_id': self.env.ref('resource_activity.view_activity_registration_form', False).id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': context,
        }

    @api.model
    def create(self, vals):
        if vals.get('registrations_max') > 0 and vals.get('registrations_max') < vals.get('registrations_expected') + vals.get('quantity_needed'):
            raise ValidationError("Maximum registration capacity reached")
        return super(ActivityRegistration,self).create(vals)

    @api.multi
    def write(self, vals):
        for registration in self:
            if (registration.registrations_max
                    and vals.get('quantity')
                    and registration.registrations_max < (
                            registration.registrations_expected
                            - registration.quantity
                            + vals.get('quantity'))):
                raise ValidationError("Maximum registration capacity reached")
        return super(ActivityRegistration,self).write(vals)


class ResourceAvailable(models.Model):
    _name = 'resource.available'

    name = fields.Char(related='resource_id.serial_number',string='Name')
    resource_id = fields.Many2one('resource.resource', string="Resource", required=True)
    registration_id = fields.Many2one('resource.activity.registration', string="Registration")
    activity_id = fields.Many2one(related='registration_id.resource_activity_id', string="Activity", readonly=True)
    state = fields.Selection([('free', 'Free'),
                              ('not_free', 'Not free'),
                              ('selected', 'Selected'),
                              ('cancelled', 'Cancelled')], string="State", readonly=True)

    @api.multi
    def action_reserve(self):
        for resource_available in self.filtered(lambda record: record.state == 'free'):
            allocation_ids = (
                resource_available
                .resource_id
                .allocate_resource(resource_available.registration_id.booking_type,
                                   resource_available.registration_id.date_start,
                                   resource_available.registration_id.date_end,
                                   resource_available.registration_id.attendee_id,
                                   resource_available.registration_id.location_id,
                                   resource_available.registration_id.date_lock)
            )
            if allocation_ids:
                allocations = self.env['resource.allocation'].browse(allocation_ids)
                allocations.write({'activity_registration_id': resource_available.registration_id.id})
                resource_available.state = 'selected'
                resource_available.registration_id.quantity_allocated += 1
                resource_available.registration_id.state = resource_available.registration_id.booking_type
            else:
                print "no resource found for : " + str(resource_available.resource_id.ids)
            self.activity_id.registrations.action_refresh()
        return True

    @api.multi
    def action_cancel(self):
        allocation = (
            self
            .registration_id
            .allocations
            .filtered(
                lambda record: record.resource_id.id == self.resource_id.id
                               and record.state != 'cancel')
        )
        allocation.action_cancel()
        if self.state == 'selected':
            self.registration_id.quantity_allocated -= 1
            if (self.registration_id.quantity_needed > self.registration_id.quantity_allocated
                    and self.registration_id.quantity_allocated > 0):
                self.registration_id.state = 'waiting'
            elif self.registration_id.quantity_allocated == 0:
                self.registration_id.state = 'cancelled'
        self.state = 'cancelled'

        return True


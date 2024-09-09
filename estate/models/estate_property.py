from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate"

    active = fields.Boolean(default=True)
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
                                        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
                                        )
    state = fields.Selection( default='new', required=True, copy=False,
                                        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancel', 'Cancelled')]
                                        )
    
    type = fields.Many2one("estate.property.type", string="Type")
    
    salesman = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer('Total Area', compute="_compute_total_area")
    best_price = fields.Float('Best Price', compute="_compute_best_price")
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
    
    class EstatePropertyType(models.Model):
        _name= "estate.property.type"
        _description="Estate Property Types"
        
        name = fields.Char()
        
    class EstatePropertyTag(models.Model):
        _name="estate.property.tag"
        _description = "Estate Property Tags"
        
        name = fields.Char()
        
    class EstatePropertyOffer(models.Model):
        _name = "estate.property.offer"
        _description = "Estate Property Offer"
        
        price = fields.Float()
        status = fields.Selection(copy=False, selection=[('accept', 'Accepted'),('refuse', 'Refused')])
        partner_id = fields.Many2one('res.partner', string="Potential Buyer", required=True)
        property_id = fields.Many2one('estate.property', string="Estate Property", required=True)
        
        validity = fields.Integer('Validity', default=7)
        date_deadline = fields.Date('Date Deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline")
        
        @api.depends("validity")
        def _compute_date_deadline(self):
            for record in self:
                create_date = record.create_date if record.id else date.today()
                record.date_deadline = create_date + relativedelta(days=record.validity)
        
        def _inverse_date_deadline(self):
            for record in self:
                create_date = record.create_date if record.id else date.today()
                record.validity = abs((record.date_deadline - create_date).days)
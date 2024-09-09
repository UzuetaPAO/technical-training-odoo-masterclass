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
    
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
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
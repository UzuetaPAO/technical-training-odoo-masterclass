from odoo import models
from logging import getLogger
_logger = getLogger(__name__)

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        _logger.warning("INHERIT WORKS")
        invoice = self.env['account.move'].create({
            'name': 'INV - ' + self.name,
            'move_type': 'out_invoice',
            'partner_id': self.buyer.id
        })
        
        invoice_line_6_percent = self.env['account.move.line'].create({
            'name': self.name,
            'quantity': 1,
            'price_unit': self.selling_price * 0.06,
            'move_id': invoice.id,
        })
        
        invoice_line_fees = self.env['account.move.line'].create({
            'name': 'Fees',
            'quantity': 1,
            'price_unit': 100,
            'move_id': invoice.id,
        })
        return super().action_sold_property()
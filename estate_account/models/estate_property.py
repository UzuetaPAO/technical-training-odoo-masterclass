from odoo import models
from logging import getLogger
_logger = getLogger(__name__)

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        _logger.warning("INHERIT WORKS")
        return super().action_sold_property()
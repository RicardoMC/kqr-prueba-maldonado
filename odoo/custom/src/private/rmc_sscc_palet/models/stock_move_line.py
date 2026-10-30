from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _put_in_pack(
        self,
        package_id=False,
        package_type_id=False,
        package_name=False,
    ):
        move_lines = self
        return super(
            StockMoveLine,
            move_lines.with_context(sscc_move_line_ids=move_lines.ids),
        )._put_in_pack(
            package_id=package_id,
            package_type_id=package_type_id,
            package_name=package_name,
        )

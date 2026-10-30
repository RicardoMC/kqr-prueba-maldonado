from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    prefijo_gs1 = fields.Char(
        string="Prefijo GS1",
        copy=False,
        help="Prefijo numérico GS1 asignado a esta compañía.",
    )
    sscc_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Secuencia SSCC",
        copy=False,
        readonly=True,
    )

    @api.constrains("prefijo_gs1")
    def _check_prefijo_gs1(self):
        for company in self:
            prefix = company.prefijo_gs1
            if prefix and (not prefix.isdigit() or len(prefix) > 15):
                raise ValidationError(
                    self.env._(
                        "El prefijo GS1 debe contener únicamente dígitos "
                        "y tener como máximo 15 caracteres."
                    )
                )

    def _get_sscc_sequence(self):
        self.ensure_one()
        prefix = self.prefijo_gs1 or ""
        if not prefix or not prefix.isdigit():
            raise ValidationError(
                self.env._(
                    "Configure un prefijo GS1 numérico en la compañía "
                    "antes de crear paquetes."
                )
            )
        serial_length = 16 - len(prefix)
        if serial_length < 1:
            raise ValidationError(
                self.env._("El prefijo GS1 no deja espacio para la referencia serial.")
            )
        self.env.cr.execute(
            "SELECT pg_advisory_xact_lock(%s, %s)",
            (728193, self.id),
        )
        self.invalidate_recordset(["sscc_sequence_id"])
        sequence = self.sscc_sequence_id
        sequence_code = f"rmc.sscc.company.{self.id}"
        Sequence = self.env["ir.sequence"].sudo()
        if not sequence:
            sequence = Sequence.search(
                [
                    ("code", "=", sequence_code),
                    ("company_id", "=", self.id),
                ],
                limit=1,
            )
        sequence_values = {
            "padding": serial_length,
            "prefix": "",
            "company_id": self.id,
        }
        if not sequence:
            sequence = Sequence.create(
                {
                    "name": f"SSCC - {self.display_name}",
                    "code": sequence_code,
                    "implementation": "standard",
                    "number_next": 1,
                    "number_increment": 1,
                    **sequence_values,
                }
            )
        elif (
            sequence.padding != serial_length
            or sequence.prefix
            or sequence.company_id.id != self.id
        ):
            sequence.write(sequence_values)

        if self.sscc_sequence_id != sequence:
            self.sudo().write({"sscc_sequence_id": sequence.id})

        return sequence

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockPackage(models.Model):
    _inherit = "stock.package"

    sscc = fields.Char(
        string="SSCC",
        size=18,
        readonly=True,
        copy=False,
        index=True,
    )
    _sscc_unique = models.Constraint(
        "UNIQUE(sscc)",
        "El SSCC debe ser único.",
    )

    @api.model
    def _gs1_check_digit(self, payload):
        """Calculate the GS1 Mod-10 check digit."""
        if not payload or not payload.isdigit():
            raise ValueError("The GS1 payload must contain only digits.")
        weighted_sum = sum(
            int(digit) * (3 if (len(payload) - index) % 2 else 1)
            for index, digit in enumerate(payload)
        )
        return str((-weighted_sum) % 10)

    @api.model
    def _build_sscc(self, gs1_prefix, serial):
        """Build an 18-digit SSCC."""
        if not gs1_prefix or not gs1_prefix.isdigit():
            raise ValueError("The GS1 company prefix must contain only digits.")
        if not serial or not serial.isdigit():
            raise ValueError("The serial reference must contain only digits.")

        payload = f"0{gs1_prefix}{serial}"
        if len(payload) != 17:
            raise ValueError(
                "The SSCC payload must contain exactly 17 digits "
                "before the check digit."
            )
        return payload + self._gs1_check_digit(payload)

    @api.model
    def _get_sscc_company(self, vals):
        """Determine the company used to generate the package SSCC."""
        move_line_ids = self.env.context.get("sscc_move_line_ids", [])
        if move_line_ids:
            move_lines = self.env["stock.move.line"].browse(move_line_ids).exists()
            companies = move_lines.mapped("company_id")
            if len(companies) > 1:
                raise ValidationError(
                    self.env._(
                        "No se puede generar un SSCC para líneas "
                        "de distintas compañías."
                    )
                )
            if companies:
                return companies
        package_type = (
            self.env["stock.package.type"].browse(vals.get("package_type_id")).exists()
        )
        if package_type and package_type.company_id:
            return package_type.company_id
        location = self.env["stock.location"].browse(vals.get("location_id")).exists()
        if location and location.company_id:
            return location.company_id
        parent_package = self.browse(vals.get("parent_package_id")).exists()
        if parent_package and parent_package.company_id:
            return parent_package.company_id

        return self.env.company

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            company = self._get_sscc_company(vals)
            sequence = company._get_sscc_sequence()
            serial = sequence.next_by_id()
            serial_length = 16 - len(company.prefijo_gs1 or "")
            if not serial or not serial.isdigit():
                raise ValidationError(
                    self.env._(
                        "La secuencia SSCC debe generar una referencia numérica."
                    )
                )
            serial = serial.zfill(serial_length)
            if len(serial) != serial_length:
                raise ValidationError(
                    self.env._(
                        "Se agotó el rango de la secuencia SSCC para esta compañía."
                    )
                )
            vals["sscc"] = self._build_sscc(
                company.prefijo_gs1,
                serial,
            )
        return super().create(vals_list)

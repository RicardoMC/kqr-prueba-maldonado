from odoo.addons.base.tests.common import BaseCommon


class TestSSCC(BaseCommon):
    def test_gs1_g01_reference_example(self):
        """Validate the GS1 G01 reference example."""
        package_model = self.env["stock.package"]
        self.assertEqual(
            package_model._gs1_check_digit("10614141123456789"),
            "7",
        )

    def test_sscc_company_a(self):
        """Validate SSCC generation for company A."""
        company = self.env.company
        company.prefijo_gs1 = "123456"

        package = (
            self.env["stock.package"]
            .with_company(company)
            .create(
                {
                    "name": "SSCC Company A",
                }
            )
        )

        sscc = package.sscc
        package_model = self.env["stock.package"]
        self.assertEqual(len(sscc), 18)
        self.assertTrue(sscc.isdigit())
        self.assertTrue(sscc.startswith("0123456"))
        self.assertEqual(sscc[-1], package_model._gs1_check_digit(sscc[:-1]))

    def test_sscc_company_b(self):
        """Validate SSCC generation for company B."""
        company = self._create_company(
            name="SSCC Test Company B",
            prefijo_gs1="654321",
        )

        package = (
            self.env["stock.package"]
            .with_company(company)
            .create(
                {
                    "name": "SSCC Company B",
                }
            )
        )

        sscc = package.sscc
        package_model = self.env["stock.package"]
        self.assertEqual(len(sscc), 18)
        self.assertTrue(sscc.isdigit())
        self.assertTrue(sscc.startswith("0654321"))
        self.assertEqual(sscc[-1], package_model._gs1_check_digit(sscc[:-1]))

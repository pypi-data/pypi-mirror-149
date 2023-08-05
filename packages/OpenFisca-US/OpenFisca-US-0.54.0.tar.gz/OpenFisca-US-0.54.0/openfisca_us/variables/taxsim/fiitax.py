from openfisca_us.model_api import *


class fiitax(Variable):
    value_type = float
    entity = TaxUnit
    label = "Federal income tax"
    unit = "currency-USD"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return tax_unit("income_tax", period)

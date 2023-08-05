from openfisca_us.model_api import *


class v25(Variable):
    value_type = float
    entity = TaxUnit
    label = "EITC"
    unit = "currency-USD"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return tax_unit("eitc", period)

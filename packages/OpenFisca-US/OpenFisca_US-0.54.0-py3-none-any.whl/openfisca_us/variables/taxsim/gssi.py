from openfisca_us.model_api import *


class gssi(Variable):
    value_type = float
    entity = TaxUnit
    label = "Gross Social Security Income"
    unit = "currency-USD"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return add(tax_unit, period, ["social_security"])

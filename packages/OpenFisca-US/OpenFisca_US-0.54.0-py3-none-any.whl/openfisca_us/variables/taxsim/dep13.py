from openfisca_us.model_api import *


class dep13(Variable):
    value_type = float
    entity = TaxUnit
    label = "Children under 13"
    unit = "currency-USD"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        age = tax_unit.members("age", period)
        return tax_unit.sum(age < 13)

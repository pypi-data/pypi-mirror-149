from decimal import Decimal
from typing import NamedTuple


class SpendException(Exception):
    """Raised when an exception occurs in Spend."""


class CostFragment(NamedTuple):
    cost: Decimal
    cost_type: str
    currency: str
    target_currency: str
    extension: str = ''

    @staticmethod
    def from_formula(formula):
        """Returns a CostFragment from a cost formula.

        The cost formula is expected to be a string containing the cost, currency, target currency,
        and cost type, each separated by an underscore. The cost type may include an extension.

            {cost}_{currency}{target_currency}_{cost_type[.extension]}

        """
        try:
            value, currencies, cost_type = tuple(formula.split('_'))
        except ValueError:
            raise SpendException(f'Invalid cost formula: {formula}')

        if len(currencies) != 6:
            raise SpendException(f'Invalid cost currency: {formula}')

        cost_type, _, extension = cost_type.partition('.')

        return CostFragment(
            cost=Decimal(value),
            cost_type=cost_type,
            currency=currencies[:3],
            extension=extension,
            target_currency=currencies[3:],
        )


class Spend:
    """Calculate spend from a cost formula."""

    def __init__(self, cost_formula):
        self.fragments = []
        self.currency = None
        self.target_currency = None

        if cost_formula:
            for formula in cost_formula.split('+'):
                fragment = CostFragment.from_formula(formula=formula)

                if self.currency is None:
                    self.currency = fragment.currency
                if self.target_currency is None:
                    self.target_currency = fragment.target_currency

                if self.currency != fragment.currency:
                    raise SpendException(f'Currencies do not match: {cost_formula}')
                if self.target_currency != fragment.target_currency:
                    raise SpendException(f'Rate Card currencies do not match: {cost_formula}')

                self.fragments.append(fragment)

class Division:
    """
    Instantiate a division operation.
    Numbers will be divided by the given divisor.

    :param divisor: The divisor.
    :type divisor: int, float
    """

    def __init__(self, divisor):
        self.divisor = divisor

    def divide(self, number):
        """
        Divide a given number by the divisor.

        :param number: The number to divide.
        :type number: int, float

        :return: The result of the division.
        :rtype: int, float
        """

        return number / self.divisor

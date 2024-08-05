class IbanError(Exception):
    def __init__(self, message, iban_value=None):
        super().__init__(message)
        self.iban_value = iban_value

    def __str__(self) -> str:
        if self.iban_value is not None:
            return f"IbanError: {super().__str__()}, IBAN: {self.iban_value}"
        else:
            return f"IbanError: {super().__str__()}"
        
class BankError(Exception):
    def __init__(self, message, bank_value=None):
        super().__init__(message)
        self.iban_value = bank_value

    def __str__(self) -> str:
        if self.iban_value is not None:
            return f"BankError: {super().__str__()}, BANK: {self.iban_value}"
        else:
            return f"BankError: {super().__str__()}"

class NormalizationUtils:

    @staticmethod
    def normalize_string(value):

        if value is None:
            return None

        return (
            str(value)
            .strip()
            .lower()
        )

    @staticmethod
    def safe_float(value):

        try:
            return float(value)
        except:
            return None
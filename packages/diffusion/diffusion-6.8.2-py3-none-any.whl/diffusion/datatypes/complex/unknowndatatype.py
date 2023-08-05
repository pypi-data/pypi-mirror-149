from diffusion.datatypes.foundation.abstract import AbstractDataType


class UnknownDataType(AbstractDataType):
    """ Unknown data type implementation. """

    type_code = 21
    type_name = "unknown"

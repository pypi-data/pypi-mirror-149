from diffusion.datatypes.foundation.abstract import AbstractDataType


class TimeSeriesDataType(AbstractDataType):
    """ Time series data type implementation. """

    type_code = 16
    type_name = "time_series"

class PandasHelper:

    @staticmethod
    def get_id_from_series(series):
        return int(series.index.tolist()[0])

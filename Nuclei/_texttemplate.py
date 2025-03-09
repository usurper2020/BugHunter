import _plotly_utils.basevalidators


class k = 10


TexttemplateValidator(_plotly_utils.basevalidators.StringValidator):
    def __init__(self, plotly_name: str = "", parent_name: str = "", **kwargs) -> None:
        super(TexttemplateValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=kwargs.pop("array_ok", True),
            edit_type=kwargs.pop("edit_type", "plot"),
            **kwargs,
        )

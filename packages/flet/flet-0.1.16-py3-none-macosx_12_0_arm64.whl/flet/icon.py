from flet.control import Control, OptionalNumber
from flet.ref import Ref


class Icon(Control):
    def __init__(
        self,
        name: str = None,
        ref: Ref = None,
        expand: int = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        color: str = None,
        size: float = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.name = name
        self.color = color
        self.size = size

    def _get_control_name(self):
        return "icon"

    # name
    @property
    def name(self):
        return self._get_attr("name")

    @name.setter
    def name(self, value):
        self._set_attr("name", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # size
    @property
    def size(self):
        return self._get_attr("size")

    @size.setter
    def size(self, value):
        self._set_attr("size", value)

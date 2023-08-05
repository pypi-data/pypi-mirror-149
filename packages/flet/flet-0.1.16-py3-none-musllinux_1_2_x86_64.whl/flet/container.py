import json
from typing import Optional

from beartype import beartype

from flet import border_radius, margin, padding
from flet.alignment import Alignment
from flet.border import Border
from flet.border_radius import BorderRadius
from flet.constrained_control import ConstrainedControl
from flet.control import BorderStyle, Control, MarginValue, OptionalNumber, PaddingValue
from flet.embed_json_encoder import EmbedJsonEncoder
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class Container(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: int = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        content: Control = None,
        padding: PaddingValue = None,
        margin: MarginValue = None,
        alignment: Alignment = None,
        bgcolor: str = None,
        border: Border = None,
        border_radius: BorderRadius = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.padding = padding
        self.margin = margin
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.border = border
        self.border_radius = border_radius

    def _get_control_name(self):
        return "container"

    def _get_children(self):
        if self.__content == None:
            raise Exception("Container does not have any content set.")
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # alignment
    @property
    def alignment(self):
        return self.__alignment

    @alignment.setter
    @beartype
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value
        self._set_attr("alignment", json.dumps(value, default=vars) if value else None)

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr(
            "padding", json.dumps(value, cls=EmbedJsonEncoder) if value else None
        )

    # margin
    @property
    def margin(self):
        return self.__margin

    @margin.setter
    @beartype
    def margin(self, value: MarginValue):
        self.__margin = value
        if value and isinstance(value, (int, float)):
            value = margin.all(value)
        self._set_attr(
            "margin", json.dumps(value, cls=EmbedJsonEncoder) if value else None
        )

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # border
    @property
    def border(self):
        return self.__border

    @border.setter
    @beartype
    def border(self, value: Optional[Border]):
        self.__border = value
        self._set_attr(
            "border", json.dumps(value, cls=EmbedJsonEncoder) if value else None
        )

    # border_radius
    @property
    def border_radius(self):
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: Optional[BorderRadius]):
        self.__border_radius = value
        if value and isinstance(value, (int, float)):
            value = border_radius.all(value)
        self._set_attr(
            "borderRadius", json.dumps(value, cls=EmbedJsonEncoder) if value else None
        )

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

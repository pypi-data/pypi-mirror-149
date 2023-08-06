"""Container class for cell output."""

from __future__ import annotations

import logging
from functools import partial
from pathlib import PurePath
from typing import TYPE_CHECKING

from prompt_toolkit.filters import has_completions, to_filter
from prompt_toolkit.layout.containers import Float, Window
from prompt_toolkit.layout.margins import ConditionalMargin
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.layout.screen import WritePosition

from euporie.app.current import get_base_app as get_app
from euporie.convert.base import find_route
from euporie.convert.util import data_pixel_size, pixels_to_cell_size
from euporie.filters import has_dialog, has_menus
from euporie.margins import ScrollbarMargin
from euporie.widgets.output.control import (
    FormattedOutputControl,
    ItermGraphicControl,
    KittyGraphicControl,
    SixelGraphicControl,
)

if TYPE_CHECKING:
    from typing import Any, Callable, Optional, Type, Union

    from prompt_toolkit.filters import FilterOrBool
    from prompt_toolkit.layout.containers import AnyContainer
    from prompt_toolkit.layout.dimension import AnyDimension
    from prompt_toolkit.layout.screen import Screen

    from euporie.widgets.output.control import OutputControl

log = logging.getLogger(__name__)


MIME_FORMATS = {
    "image/svg+xml": "svg",
    "image/png": "base64-png",
    "image/jpeg": "base64-jpeg",
    "application/pdf": "base64-pdf",
    "text/html": "html",
    "text/latex": "latex",
    "text/markdown": "markdown",
    "text/x-markdown": "markdown",
    "text/*": "ansi",
    "stream/std*": "ansi",
}


BLING_SCORES = {
    "image/*": 0,
    "application/pdf": 1,
    "text/html": 2,
    "text/latex": 3,
    "text/markdown": 4,
    "text/x-markdown": 4,
    "text/x-python-traceback": 5,
    "text/stderr": 6,
    "text/*": 7,
    "*": 8,
}


def _calculate_bling(item: tuple[str, str]) -> int:
    """Scores the richness of mime output types."""
    mime, _ = item
    for bling_path, score in BLING_SCORES.items():
        if PurePath(mime).match(bling_path):
            return score
    else:
        return 999


class GraphicWindow(Window):
    """A window responsible for displaying terminal graphics content.

    The graphic will be displayed if:
    - a completion menu is not being shown
    - a dialog is not being shown
    - a menu is not being shown
    - the output it attached to is fully in view
    """

    content: "OutputControl"

    def __init__(
        self,
        content: "OutputControl",
        target_window: "Window",
        *args: "Any",
        **kwargs: "Any",
    ):
        """Initiates a new :py:class:`GraphicWindow` object.

        Args:
            content: A control which generates the graphical content to display
            target_window: The window this graphic should position itself over
            *args: Positional arguments for :py:method:`Window.__init__`
            **kwargs: Key-word arguments for :py:method:`Window.__init__`
        """
        super().__init__(*args, **kwargs)
        self.target_window = target_window
        self.content = content
        self.float = None

    def write_to_screen(
        self,
        screen: "Screen",
        mouse_handlers: "MouseHandlers",
        write_position: "WritePosition",
        parent_style: "str",
        erase_bg: "bool",
        z_index: "Optional[int]",
    ) -> "None":
        """Draws the graphic window's contents to the screen if required."""
        if (
            not has_completions()
            and not has_dialog()
            and not has_menus()
            and (
                target_wp := screen.visible_windows_to_write_positions.get(
                    self.target_window
                )
            )
        ):
            assert self.target_window.render_info is not None
            rendered_height = self.target_window.render_info.window_height
            # Only draw if the target window is fully visible
            if target_wp.height == rendered_height:
                cpos = screen.get_menu_position(self.target_window)
                new_write_position = WritePosition(
                    xpos=cpos.x,
                    ypos=cpos.y,
                    width=target_wp.width,
                    height=target_wp.height,
                )
                super().write_to_screen(
                    screen,
                    MouseHandlers(),  # Do not let the float add mouse events
                    new_write_position,
                    # Ensure the float is always updated by constantly changing style
                    parent_style + f" class:graphic-{get_app().render_counter}",
                    erase_bg=True,
                    z_index=z_index,
                )
                return
        # Otherwise hide the content (required for kitty graphics)
        self.content.hide()


class OutputWindow(Window):
    """A window sub-class which holds a reference to a graphic float."""

    content: "OutputControl"

    def __init__(self, *args: "Any", **kwargs: "Any") -> "None":
        """Initialise the window, creating an attribute to hold a float reference."""
        Window.__init__(self, *args, **kwargs)
        self.graphic_float: "Optional[Float]" = None

    def _write_to_screen_at_index(
        self,
        screen: Screen,
        mouse_handlers: MouseHandlers,
        write_position: WritePosition,
        parent_style: str,
        erase_bg: bool,
    ) -> None:
        """Ensure the :attr:`horizontal_scroll` is recorded."""
        super()._write_to_screen_at_index(
            screen,
            mouse_handlers,
            write_position,
            parent_style,
            erase_bg,
        )
        if self.render_info:
            setattr(self.render_info, "horizontal_scroll", self.horizontal_scroll)

    def _scroll_right(self) -> None:
        """Scroll window right."""
        info = self.render_info
        if info is None:
            return
        content_width = self.content.content_width
        if self.horizontal_scroll < content_width - info.window_width:
            if info.cursor_position.y <= info.configured_scroll_offsets.right:
                self.content.move_cursor_right()

            self.horizontal_scroll += 1

    def _scroll_left(self) -> None:
        """Scroll window left."""
        info = self.render_info
        if info is None:
            return
        horizontal_scroll = getattr(self.render_info, "horizontal_scroll")  # noqa B009
        if horizontal_scroll > 0:
            if (
                info.cursor_position.x
                >= info.window_width - 1 - info.configured_scroll_offsets.left
            ):
                self.content.move_cursor_left()

            self.horizontal_scroll -= 1


class CellOutput:
    """A container for rendered cell outputs."""

    def __init__(
        self,
        json: "dict[str, Any]",
        height: "AnyDimension" = None,
        width: "AnyDimension" = None,
        focusable: "FilterOrBool" = False,
        focus_on_click: "FilterOrBool" = False,
        show_scrollbar: "FilterOrBool" = False,
        wrap_lines: "FilterOrBool" = False,
        always_hide_cursor: "FilterOrBool" = True,
        style: "Union[str, Callable[[], str]]" = "",
    ) -> "None":
        """Instantiate an Output container object.

        Args:
            json: A reference to the notebook json branch corresponding to this output
            height: The height of the output
            width: The width of the output
            focusable: If the output should be focusable
            focus_on_click: If the output should become focused when clicked
            show_scrollbar: If the output should have a scrollbar
            wrap_lines: If the output's lines should be wrapped
            always_hide_cursor: When true, the cursor is never shown
            style: The style to apply to the output

        """
        self.json = json
        self.show_scrollbar = to_filter(show_scrollbar)
        self.style = style
        self.window = OutputWindow(
            height=height,
            width=width,
            right_margins=[
                ConditionalMargin(
                    ScrollbarMargin(
                        display_arrows=True,
                        up_arrow_symbol="▲",
                        down_arrow_symbol="▼",
                        smooth=True,
                    ),
                    filter=self.show_scrollbar,
                ),
            ],
            wrap_lines=wrap_lines,
            always_hide_cursor=always_hide_cursor,
            dont_extend_height=False,
            style=self.style,
        )

        metadata = json.get("metadata", {})
        fg_color = get_app().color_palette.fg.base_hex
        bg_color = {"light": "#FFFFFF", "dark": "#000000"}.get(
            metadata.get("needs_background")
        )

        # Sort data first so there is more bling first
        datum = ""
        for mime, datum_ in sorted(self.data.items(), key=_calculate_bling):
            mime_path = PurePath(mime)
            format_ = None
            for data_mime, data_format in MIME_FORMATS.items():
                if mime_path.match(data_mime):
                    if mime_path.name == "stderr":
                        self.window.style = "fg:red"
                    if find_route(data_format, "formatted_text") is not None:
                        format_ = data_format
                        datum = datum_
                        break
            else:
                continue
            break
        else:
            if self.data:
                format_ = "ansi"
                datum = sorted(self.data.items(), key=_calculate_bling)[-1][1]
            else:
                return

        mime_meta = metadata.get(mime, {})

        # We create a function to calculate the size of the output so it can be
        # called when actually needed - it can be quite expensive to calculate

        # Get data pixel dimensions
        px = mime_meta.get("width")
        py = mime_meta.get("height")
        if px is None or py is None:
            px, py = data_pixel_size(
                datum,
                format_,
                fg=fg_color,
                bg=bg_color,
            )
        sizing_func = partial(pixels_to_cell_size, px, py)

        # Create the control
        self.window.content = FormattedOutputControl(
            datum,
            format_=format_,
            fg_color=fg_color,
            bg_color=bg_color,
            sizing_func=sizing_func,
            focusable=focusable,
            focus_on_click=focus_on_click,
        )

        # Add graphic
        self.graphic_float: "Optional[Float]" = None
        GraphicControl: "Optional[Type[OutputControl]]" = None

        term_info = get_app().term_info
        if term_info.kitty_graphics_status.value and find_route(format_, "base64-png"):
            GraphicControl = KittyGraphicControl
        elif term_info.iterm_graphics_status.value and find_route(
            format_, "base64-png"
        ):
            GraphicControl = ItermGraphicControl
        elif term_info.sixel_graphics_status.value and find_route(format_, "sixel"):
            GraphicControl = SixelGraphicControl

        if GraphicControl is not None:
            self.graphic_float = Float(
                content=GraphicWindow(
                    target_window=self.window,
                    content=GraphicControl(
                        datum,
                        format_=format_,
                        fg_color=fg_color,
                        bg_color=bg_color,
                        sizing_func=sizing_func,
                    ),
                ),
                left=0,
                top=0,
            )
        if self.graphic_float is not None:
            get_app().add_float(self.graphic_float)
        self.window.graphic_float = self.graphic_float

    @property
    def data(self) -> "dict[str, str]":
        """Return dictionary of mime types and data for this output.

        This generates similarly structured data objects for markdown cells and text
        output streams.

        Returns:
            JSON dictionary mapping mimes type to representation data.

        """
        output_type = self.json.get("output_type", "unknown")
        if output_type == "stream":
            return {f'stream/{self.json.get("name")}': self.json.get("text", "")}
        elif output_type == "error":
            return {
                "text/x-python-traceback": "\n".join(self.json.get("traceback", ""))
            }
        else:
            return self.json.get("data", {})

    def __pt_container__(self) -> "AnyContainer":
        """Return the content of this output."""
        return self.window

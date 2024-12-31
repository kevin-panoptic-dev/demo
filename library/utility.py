from __future__ import annotations
from collections.abc import Callable
from functools import wraps
from typing import Any
import logging
import time
from rich.text import Text
from rich import print as rt

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


def prismelt(
    message: Any, *, color: tuple[int, int, int] | str | None = None, end: str = "\n"
) -> None:
    """
    Prints a message with the specified color, supporting both RGB and hexadecimal formats.
    If `color` is None, the function defaults to standard output without additional styling.
    Note that only integer-based RGB values are supported for RGB tuples.

    Parameters:
    ----------
    message : any
        The content to be printed. If `message` is not already a string, it will be converted to one.

    color : tuple[int, int, int] | str | None, optional
        Specifies the color format:
        - If a tuple, it must contain exactly three integers representing RGB values, each within the range 0-255.
        - If a string, it should be a valid hexadecimal color code starting with '#'.
        - If None, `prismelt` defaults to the standard print function without applying color.
    end : str optional
        - The end part (colorless) user want to print after the color part, default to "\n" as a line terminator.

    Returns:
    -------
    None
        This function does not return any values. It prints directly to the console.

    Raises:
    ------
    TypeError
        - If `message` cannot be converted to a string.
        - If `extension` is not a string.
        - If `end` is not a string.
        - If `color` is neither a tuple, string, nor None.
        - If `color` is a tuple with incorrect length or containing non-integer values.
        - If RGB values are outside the 0-255 range.
        - If `color` is a string but not in valid hexadecimal format or has an invalid length.

    Notes:
    ------
    - This function does not support float RGB values; RGB must contain only integers.
    - For hex color codes, all characters must be valid hexadecimal digits (0-9, A-F, or a-f).

    Examples:
    --------
    ```python
    prismelt("Hello World", color=(255, 0, 0))  # Prints "Hello World" in red using RGB values.
    prismelt("Hello World", color="#00FF00")    # Prints "Hello World" in green using hexadecimal.
    prismelt("Hello World")                     # Prints "Hello World" without color styling.
    ```
    """
    try:
        message = str(message)
    except Exception:
        # Avoid edge cases
        raise TypeError(f"message must be str, not {type(message).__name__}.")

    if not isinstance(color, (tuple, str)) and color is not None:
        raise TypeError(
            f"color must be a tuple (RGB), a string (hexadecimal) or None (default print), not {type(message).__name__}."
        )
    elif not isinstance(end, str):
        raise TypeError(f"`end` must be a string, not {type(end).__name__}.")

    match (color is None, isinstance(color, tuple), isinstance(color, str)):
        case (True, _, _):
            print(message, end=end)
        case (_, True, _):
            # input validation
            assert isinstance(color, tuple)
            if len(color) != 3:
                raise TypeError(
                    f"Invalid input length for color tuple, must be 3, not {len(color)}."
                )
            elif (
                not isinstance(color[0], int)
                or not isinstance(color[1], int)
                or not isinstance(color[2], int)
            ):
                if (
                    isinstance(color[0], float)
                    and isinstance(color[1], float)
                    and isinstance(color[2], float)
                ):
                    logging.error("Sorry, but prismelt don't support float-point RGB.")
                raise TypeError(
                    f"Invalid type {type(color[0]).__name__}, {type(color[1]).__name__}, {type(color[2]).__name__}, must be int, int, int."
                )

            for x in range(3):
                if color[x] < 0 or color[x] > 255:
                    raise TypeError(
                        f"Invalid input {color[x]}, must inside the range of 0 - 255."
                    )

            # This is valid message with valid RGB!
            message = Text(message)
            style: str = f"rgb({color[0]},{color[1]},{color[2]})"
            message.stylize(style)
            rt(message, end=end)

        case (_, _, True):
            # input validation
            assert isinstance(color, str)
            color = color.strip()
            if not color.startswith("#"):
                raise TypeError(
                    f"Hexadecimal color must start with '#', not '{color[:1]}'."
                )

            color_list: list = []
            for characters in iter(color[1:]):
                if characters == " ":
                    continue
                elif characters in "0123456789ABCDEFabcdef":
                    color_list.append(characters)
                    continue
                else:
                    raise TypeError(
                        f"Character '{characters}' in color string {color} is not valid."
                    )

            style = "#" + "".join(color_list)
            if len(style) != 7:
                raise TypeError(f"Length must be 7, not {len(style)}.")

            # This is a valid message with valid hex color!
            message = Text(message)
            message.stylize(style)
            rt(message, end=end)

        case _:
            raise TypeError(
                f"Invalid input for color {color}. Must be RGB or hexadecimal with '#'."
            )


class timing:
    """
    A decorator class to measure and display the average execution time of a function.

    Parameters
    ----------
    times : int, optional
        The number of times the decorated function should be called for timing purposes.
        This allows measuring average execution time over multiple runs. Default is 100.

        - Must be a positive integer.
    fixer : (int, float),  optional
        A scaling factor to adjust the reported execution time, providing flexibility in
        units or custom scaling. Default is 1.
        The final output will be multiplied by fixer.

        - Must be a positive integer or float.
    precise : int, optional
        A precise factor to adjust the precise execution time, providing flexibility in
        precise counting. Default is 2.

        - Must be a positive integer.
    unit: any, optional
        The unit user want to see as the display.

    Methods
    -------
    __call__(function: callable, *args, **kwargs)
        Decorates the specified function, measures its execution time over `times` runs,
        and displays the average time adjusted by the `fixer`.

    Exceptions
    ----------
    TypeError
        Raised if `times` or `fixer` or `precise` is not the right type.
    ValueError
        Raised if `times` or `fixer` is `precise` less than or equal to zero.

    Usage
    -----
    To use the `timing` decorator, instantiate it with desired parameters and apply it to
    a function. The decorator calculates the average execution time over the specified number
    of runs, adjusting the result with the `fixer` parameter. The timing information is
    printed with formatting specified by an external function `prismelt`.

    Example
    -------
    >>> @timing(times=100, fixer=1)
    ... def my_function():
    ...     # function logic
    ...
    The function `my_function` will be called 100 times, and the average execution time per
    call will be calculated and displayed.

    Notes
    -----
    - The `wrapper` function captures the start and end time for executing the decorated
      function over `times` repetitions, calculates the average time, and adjusts it by `fixer`.
    - The timing information is displayed with `prismelt`, which accepts a formatted message
      and a color parameter, where the color is set to a light red.

    Dependencies
    ------------
    - `time.time()`: To capture the start and end times for execution.
    - `wraps`: From `functools`, used to preserve the metadata of the original function.
    """

    def __init__(
        self,
        *,
        times: int = 100,
        fixer: int = 1,
        precise: int = 2,
        unit: Any = "seconds",
    ) -> None:
        if not isinstance(times, int):
            raise TypeError(f"`limitation` must be int, not {type(times).__name__}.")
        elif times <= 0:
            raise ValueError(
                f"`limitation` must be positive integers, not {type(times).__name__}."
            )

        if not isinstance(fixer, (int, float)):
            raise TypeError(
                f"`fixer` must be int or float, not {type(fixer).__name__}."
            )
        elif fixer <= 0:
            raise ValueError(
                f"`fixer` must be positive numbers, not {type(fixer).__name__}."
            )

        if not isinstance(precise, int):
            raise TypeError(f"`precise` must be int, not {type(precise).__name__}.")
        elif fixer <= 0:
            raise ValueError(
                f"`precise` must be positive integers, not {type(precise).__name__}."
            )

        self.called_times: int = times
        self.fixer: int = fixer
        self.precise: int = precise
        self.unit: Any = unit

    def __call__(self, function: Callable, *args, **kwargs) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            result = None
            start_time: float = time.time()
            for _ in range(self.called_times):
                result: Any = function(*args, **kwargs)
            end_time: float = time.time()
            print(
                f"The function {function.__name__} cause {((end_time - start_time) / self.called_times * self.fixer):.{self.precise}f} {self.unit} to execute."
            )
            return result

        return wrapper

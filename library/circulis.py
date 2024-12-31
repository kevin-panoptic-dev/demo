from __future__ import annotations

import math
import logging
import inspect
from copy import copy, deepcopy
from typing import Any, Literal, Self
from collections.abc import Generator, Iterable, Iterator, Callable, Hashable
from collections import deque, defaultdict, Counter
from deprecated import deprecated

try:
    from .meta import metaclarion
except ImportError:
    from library.meta import metaclarion
from random import randint

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


class circulis(metaclass=metaclarion):
    """
    A circular deque-based data structure with enhanced functionality for complex operations.

    The `circulis` class builds on Python's `deque`, offering high performance for operations on both ends of the structure.
    Unlike `deque`, which is limited in its ability to perform slicing or modifications in the middle, `circulis` supports
    comprehensive operations that enable advanced manipulations directly on the object.

    Key Features
    ------------
    1. **Deque Foundation with Advanced Operations**:
       Optimized for both-end operations while extending functionality to include slicing, filtering, sorting, and other
       complex manipulations.

    2. **Enhanced Integration of Dunder Methods**:
       Includes a wide array of magic methods for seamless integration with Python's standard operations. By default,
       `circulis` prints like a regular list, and users can assign a name to the object for improved error tracking
       and debugging.

    3. **Support for Complex Operations**:
       Goes beyond basic inplace operations (e.g., map, filter, sort) to offer advanced methods like `synergy` for merging
       `circulis` objects and `disentangle` for flattening nested structures. These tools enable flexible and powerful
       data processing.

    4. **Rich Operator Overloading**:
       Supports a wide range of operators (`^`, `|`, `&`, `-`, etc.) for interactions with other `circulis` instances
       and list-like objects, allowing for a vast array of composable operations.
    """

    def __init__(
        self,
        iterable: str | list | tuple | deque | Generator = deque(),
        *args,
        name: str | None = None,
        **kwargs,
    ) -> None:
        """
        Initializes a `circulis` object with a given iterable, converting it into a circular deque structure.

        Parameters
        ----------
        iterable : str | list | tuple | deque | Generator
            The iterable data to initialize the circulis object. This can be a string, list, tuple, deque,
            or generator expression. It will be stored as a deque to enable circular indexing.

        name : str, optional
            A name for the circulis object. If not provided, the name will be inferred from the variable name
            in the calling scope. If the variable name cannot be identified, it defaults to "Anonymous Circulist".

        Raises
        ------
        TypeError
            Raised if the provided `iterable` argument is not an instance of an iterable type, or if `name`
            is provided but is not of type `str`.

        Warnings
        --------
        - Logs a `WARNING` if `iterable` is of an unsupported type (not `str`, `list`, `tuple`, or `deque`).
        - Logs an `INFO` if `iterable` is of type `str`, for informational tracking.

        Logging
        -------
        This method will log messages to inform about the type of iterable received and any unsupported data types.
        The logging levels used are as follows:

        - `INFO`: Logged when a string is provided as `iterable`, indicating a common use-case.
        - `WARNING`: Logged if the iterable is a supported type (e.g., a generator) but is not one of the common types
        (`str`, `list`, `tuple`, `deque`).

        Notes
        -----
        If `name` is not provided, the variable name in the calling scope is inferred to assign a unique identifier
        to the circulis object. If no variable name can be inferred, the name defaults to `"Anonymous Circulist"`.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3], name="my_circulis")
        >>> print(circulis_instance.name)
        my_circulis

        >>> unnamed_instance = circulis("ABC")
        INFO:root:A string ABC is passed.
        >>> print(unnamed_instance.name)
        Anonymous Circulist
        """
        if not isinstance(iterable, Iterable):
            raise TypeError(f"Object {iterable} is not an iterable object.")

        if not isinstance(iterable, (str, list, tuple, deque, Generator)):
            logging.warning(
                f"Unexpected datatype {type(iterable).__name__}, excepted to be str, list, tuple or deque."
            )
        elif isinstance(iterable, str):
            logging.info(f"A string {iterable} is passed.")

        self.circulist: deque = (
            deque(iterable) if not isinstance(iterable, deque) else iterable
        )

        match name:
            case None:
                self.name = "Anonymous Circulist"
            case str():
                self.name = name
            case _:
                raise TypeError(
                    f"Invalid input name type {type(name).__name__}, must be str or leave None as default."
                )

    def append(
        self,
        item: Any,
        *,
        mode: Literal["right", "left"] = "right",
        unpack: bool = True,
        unpack_tuple: bool = False,
        filter_None: bool = False,
    ) -> None:
        """
        Appends an item to the `circulis` deque, with options to control the direction, unpacking,
        and filtering behavior.

        Parameters
        ----------
        item : Any
            The item to be appended. This can be a single element or an iterable (e.g., list, tuple, deque, or circulis)
            to be unpacked based on the `unpack` and `unpack_tuple` flags.

        mode : Literal["right", "left"], optional
            Specifies the direction to append the item. set to "right" to append to the end of the deque, or "left"
            to append to the front. Defaults to "right".

        unpack : bool, optional
            Determines whether to unpack items if `item` is a list, deque, or `circulis` object. If `True`, the elements
            within `item` are appended individually. Defaults to `True`.

        unpack_tuple : bool, optional
            Determines whether to unpack `item` if it is a tuple. If `True`, the tuple elements are appended individually.
            Defaults to `False`.

        filter_None : bool, optional
            Filters out `None` values from the appended items if `True`. This option has no effect on a tuple unless
            `unpack_tuple` is set to `True`, since tuples are immutable. Defaults to `False`.

        Raises
        ------
        TypeError
            - Raised if `mode` is not `"right"` or `"left"`.
            - Raised if `unpack`, `unpack_tuple`, or `filter_None` are not of type `bool`.

        Warnings
        --------
        - Logs a `WARNING` if `filter_None` is used with a tuple without `unpack_tuple=True`, since tuples are immutable
        and their contents cannot be modified.

        Notes
        -----
        This method supports flexible appending behavior:

        - **Conditional unpacking**: If `unpack` or `unpack_tuple` is set to `True`, the method will individually append
        each element in the iterable to the circulis deque.
        - **Conditional filtering**: When `filter_None=True`, `None` values are excluded from the appended items. This
        setting is ignored for tuples unless `unpack_tuple=True`.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.append([4, None, 5], unpack=True, filter_None=True)
        >>> print(circulis_instance)
        [1, 2, 3, 4, 5]

        >>> circulis_instance.append((6, None, 7), mode="left", unpack_tuple=True, filter_None=True)
        WARNING:root:'tuple' object is immutable, but 'filter_None' is used.
        >>> print(circulis_instance)
        [6, 7, 1, 2, 3, 4, 5]
        """
        if isinstance(item, tuple) and filter_None:
            logging.warning("'tuple' object is immutable, but 'filter_None' is used.")

        match mode:
            case "right" | "left":
                pass
            case _:
                raise TypeError(
                    f"Invalid input 'mode' {mode}, must be 'right' or 'left'."
                )

        match (unpack, unpack_tuple, filter_None):
            case (bool(), bool(), bool()):  # Ensure all three are boolean
                pass
            case _:
                if not isinstance(unpack, bool):
                    raise TypeError(
                        f"Invalid input type {type(unpack).__name__}, must be bool."
                    )
                elif not isinstance(unpack_tuple, bool):
                    raise TypeError(
                        f"Invalid input type {type(unpack_tuple).__name__}, must be bool."
                    )
                elif not isinstance(filter_None, bool):
                    raise TypeError(
                        f"Invalid input type {type(filter_None).__name__}, must be bool."
                    )

        # identify the type of item, then pass it into specific function.
        match item:
            case list() | deque() | circulis() if unpack:
                self.encrypt_append_list(mode, filter_None, list(item))  # type: ignore

            case tuple() if unpack_tuple:
                self.encrypt_append_list(mode, filter_None, list(item))  # type: ignore

            case _:
                self.encrypt_append_general(mode, item)  # type: ignore

        return None

    def rotate(self, n: int = 1) -> None:
        """
        Rotates the `circulis` deque by a specified number of steps, mimicking the behavior of `deque.rotate`.

        Parameters
        ----------
        n : int, optional
            The number of steps to rotate the deque. A positive value rotates the deque to the right, while a
            negative value rotates it to the left. Defaults to `1`.

        Raises
        ------
        TypeError
            Raised if `n` is not an integer, indicating an invalid input type.

        Warnings
        --------
        logs a warning if the circulist is empty.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 4])
        >>> circulis_instance.rotate(2)
        >>> print(circulis_instance)
        [3, 4, 1, 2]

        >>> circulis_instance.rotate(-1)
        >>> print(circulis_instance)
        [4, 1, 2, 3]
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning("Rotate an empty circulist is unhelpful.")

        if not isinstance(n, int):
            raise TypeError(
                f"Invalid input n {n}, must be int, not {type(n).__name__}."
            )

        self.circulist.rotate(n)
        return None

    def remove(self, start: int, stop: int | None = None, step: int = 1) -> None:
        """
        Removes items from the `circulis` deque based on specified `start`, `stop`, and `step` parameters.

        Parameters
        ----------
        start : int
            The starting index of the removal range. This defines the first index to remove.

        stop : int | None, optional
            The ending index of the removal range (inclusive). If `None`, `stop` is set to equal `start`,
            resulting in the removal of a single item at the `start` index. Defaults to `None`.

        step : int, optional
            The interval between indices to remove. A step of `1` means consecutive elements are removed,
            while larger steps remove elements at specified intervals. Defaults to `1`.

        Raises
        ------
        ValueError
            Raised if the `circulis` deque has a length of zero, indicating that no items are available for removal.

        TypeError
            Raised if any of the parameters (`start`, `stop`, or `step`) are not integers.

        IndexError
            Raised if `start`, `stop`, or `step` exceed the length of the `circulis` deque, making the indices invalid.

        Warnings
        --------
        - Logs a `WARNING` if negative indices are used in `start`, `stop`, or `step`, as they may lead to unintended
        behavior.

        Notes
        -----
        This method uses a generator to yield indices in the specified range based on `start`, `stop`, and `step`.
        As items are deleted from the `circulis` deque, an `index_fixer` is applied to adjust subsequent indices
        dynamically, ensuring the correct elements are removed.

        Examples
        --------
        >>> circulis_instance = circulis([10, 20, 30, 40, 50])
        >>> circulis_instance.remove(1, 3)
        >>> print(circulis_instance)
        [10, 50]

        >>> circulis_instance = circulis([10, 20, 30, 40, 50])
        >>> circulis_instance.remove(0, 4, step=2)
        >>> print(circulis_instance)
        [20, 40]
        """
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError(
                f"Circulist `{self.name}` is empty, nothing can be removed."
            )

        if stop is None:
            stop = start
        if start < 0 or stop < 0 or step < 0:
            logging.warning(
                f"Negative index is used for removing items in circulist {self.name}"
            )

        match (isinstance(start, int), isinstance(stop, int), isinstance(step, int)):
            case (False, _, _):
                raise TypeError(f"Start must be int, not {type(start).__name__}.")
            case (_, False, _):
                raise TypeError(f"Stop must be int, not {type(stop).__name__}.")
            case (_, _, False):
                raise TypeError(f"Step must be int, not {type(step).__name__}.")

        match (
            start >= len(self.circulist),
            stop >= len(self.circulist),
            step >= len(self.circulist),
        ):
            case (True, _, _) | (_, True, _) | (_, _, True):
                raise IndexError(
                    f"Circulist index out of range. For circulist {self.name}, index in {len(self.circulist)-1}."
                )

        # define a generator generates all the values that need to be removed, instead of store them in a list.
        def generator(start: int, stop: int, step: int) -> Generator[int, None, None]:
            for index in range(start, stop + 1, step):
                yield index

        # algorithm that can successfully delete the right index
        index_fixer = 0
        generator_object: Generator[int, None, None] = generator(start, stop, step)
        for index in generator_object:
            del self.circulist[
                index - index_fixer
            ]  # generator yield the right index, index fixer fix it.
            index_fixer += 1

        return None

    def insert(
        self, item: Any, start: int, stop: int | None = None, step: int = 1
    ) -> None:
        """
        Inserts an item into the `circulis` deque at specified intervals defined by `start`, `stop`, and `step`.

        Parameters
        ----------
        item : Any
            The item to insert into the `circulis` deque at each specified index.

        start : int
            The starting index for the insertion process.

        stop : int, optional
            The ending index for insertion (inclusive). If `None`, `stop` is set to the value of `start`,
            resulting in a single insertion at `start`. Defaults to `None`.

        step : int, optional
            The interval between insertions. A `step` of `1` means every index between `start` and `stop`
            is considered, while larger steps insert at intervals. Defaults to `1`.

        Raises
        ------
        ValueError
            Raised if the `circulis` deque is empty. Suggests `append()` as an alternative.

        TypeError
            Raised if `start`, `stop`, or `step` are not integers, indicating invalid input types.

        Warnings
        --------
        - Logs a `WARNING` if negative indices are provided in `start`, `stop`, or `step`, as they may lead
        to unexpected insertion behavior.

        Notes
        -----
        If `stop` is `None`, it is automatically set to the value of `start`, leading to a single insertion.
        The loop iterates from `start` to `stop` by `step`, inserting `item` at each specified index.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 4, 5])
        >>> circulis_instance.insert(0, start=1, stop=3)
        >>> print(circulis_instance)
        [1, 0, 2, 0, 3, 4, 5]


        >>> circulis_instance.insert(9, start=0, stop=4, step=2)
        >>> print(circulis_instance)
        [9, 1, 0, 9, 2, 0, 3, 4, 5]
        """
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError(
                "Circulist has a length of zero, using `append` to push values"
            )

        if stop is None:
            stop = start

        if (
            not isinstance(start, int)
            or not isinstance(stop, int)
            or not isinstance(step, int)
        ):
            raise TypeError(
                f"Invalid input type {type(start).__name__}, {type(stop).__name__}, {type(step).__name__}, must be int."
            )
        if start < 0 or stop < 0 or step < 0:
            logging.warning(
                f"Negative index is used in inserting circulist `{self.name}`."
            )
        stop += 1

        for index in range(start, stop, step):
            self.circulist.insert(index, item)
        return None

    def discard(self, element: Any) -> None:
        """
        Removes the first occurrence of a specified element from the `circulis` deque, if present.

        Parameters
        ----------
        element : Any
            The element to be removed from the `circulis` deque. Only the first matching occurrence is removed.

        Raises
        ------
        ValueError
            - Raised if the `circulis` deque is empty, indicating no items are available for removal.
            - Raised if `element` is not found in the `circulis` deque, meaning no matching item exists.

        Notes
        -----
        - This method attempts to remove only the first occurrence of `element`. If successful, the method exits
        early after removal.
        - If `element` is not found, a `ValueError` is raised with an appropriate message.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 4])
        >>> circulis_instance.discard(3)
        >>> print(circulis_instance)
        [1, 2, 4]

        >>> circulis_instance.discard(5)
        ValueError: Element 5 not in the circulist `circulis_instance`
        """
        if not len(self.circulist):
            raise ValueError(f"Circulist `{self.name}` has a length of zero.")

        try:
            self.circulist.remove(element)
            return  # break the function
        except ValueError:
            # Failure in remove the item.
            raise ValueError(f"Element {element} not in the circulist `{self.name}`.")

    def disentangle(self) -> None:
        """
        Flattens all nested iterable structures (exclude string) within the `circulis` deque, expanding any nested sequences
        (lists, tuples, or other supported iterable types) into a single, non-nested sequence of elements.

        Returns
        -------
        None

        Notes
        -----
        - This method recursively traverses any list-like (iterable) elements within the `circulis` deque,
        collecting non-iterable items in a flattened order.
        - Nested lists within lists are fully expanded, so each item is moved to a single, flat level within
        the `circulis` deque.
        - The `circulis` deque is cleared after extraction, and the flattened list is then reinserted to update
        `circulis` with the disentangled structure.

        Examples
        --------
        >>> circulis_instance = circulis([1, [2, 3], [4, [5, 6]], 7])
        >>> circulis_instance.disentangle()
        >>> print(circulis_instance)
        [1, 2, 3, 4, 5, 6, 7]
        """
        store_list: list = []

        def recursive_flatten(list_object) -> None:
            for items in list_object:
                if isinstance(items, Iterable) and not isinstance(items, str):
                    store_list.append(items)
                    continue
                else:
                    # this items is a list-like object:
                    recursive_flatten(items)

        recursive_flatten(self.circulist)
        self.circulist.clear()
        self.circulist.extend(store_list)
        return None

    def curatesort(self, func: Callable, reverse=False) -> None:
        """
        Sorts the `circulis` deque based on a custom sorting function, with optional reverse sorting.

        Parameters
        ----------
        func : callable
            A function that takes an element of the `circulis` as input and returns a value to use for sorting.

        reverse : bool, optional
            If `True`, sorts in descending order. If `False` (default), sorts in ascending order.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If `func` is not a callable function.
            - If `reverse` is not a boolean.

        Warnings
        --------
        - Logs a `WARNING` if the `circulis` deque is empty, as there are no elements to sort.

        Notes
        -----
        - The `func` parameter allows custom sorting logic. For example, `func` could be a lambda expression or
        a defined function that returns a specific attribute or transformation of each item.
        - Sorting is done on a temporary list conversion of the `circulis`, and the sorted list is then reassigned
        to `circulis`, preserving the sorted order.

        Examples
        --------
        >>> circulis_instance = circulis([3, 1, 4, 1, 5, 9])
        >>> circulis_instance.curatesort(lambda x: x)
        >>> print(circulis_instance)
        [1, 1, 3, 4, 5, 9]

        >>> circulis_instance.curatesort(lambda x: x, reverse=True)
        >>> print(circulis_instance)
        [9, 5, 4, 3, 1, 1]
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning(
                f"Circulist {self.name} is empty, sort function may lead to unexpected behavior."
            )

        if not callable(func):
            raise TypeError(f"{type(func).__name__} is not callable.")
        elif not isinstance(reverse, bool):
            raise TypeError(f"'reverse' must be bool, not {type(reverse).__name__}.")

        self.circulist = deque(sorted(self.circulist, key=func, reverse=reverse))

        return None

    def curtail(self, amount: int, *, mode: Literal["left", "right"] = "right") -> None:
        """
        Removes a specified number of elements from either the beginning or the end of `circulis`.

        Parameters
        ----------
        amount : int
            The number of elements to remove from the `circulis` deque.

        mode : {"left", "right"}, optional
            Specifies the direction from which to remove elements:
            - "left": Removes elements from the start (beginning).
            - "right": Removes elements from the end.
            Defaults to "right".

        Returns
        -------
        None
            This method modifies `circulis` in place and does not return a value.

        Raises
        ------
        TypeError
            If `amount` is not an integer.

        ValueError
            - If `amount` is not a positive integer.
            - If `mode` is not "left" or "right".
            - If the length of the circulist is zero.

        Notes
        -----
        - This method will remove up to `amount` elements from the `circulis` deque based on the specified `mode`.
        - If `circulis` has fewer elements than `amount`, it will clear the deque without raising an error.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 4, 5])
        >>> circulis_instance.curtail(2, mode="left")
        >>> print(circulis_instance)
        [3, 4, 5]

        >>> circulis_instance.curtail(1, mode="right")
        >>> print(circulis_instance.circulist)
        [3, 4]

        >>> empty_circulis = circulis([])
        >>> circulis_instance.curtail(1)
        ValueError("Curtail an empty circulis is invalid.")
        """
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError("Curtail an empty circulis is invalid.")

        if not isinstance(amount, int):
            raise TypeError(f"`amount` must be int, not {type(amount).__name__}.")
        elif amount <= 0:
            raise ValueError(f"`amount must be a positive integer.")
        match mode:
            case "left":
                for _ in range(amount):
                    self.circulist.popleft()
            case "right":
                for _ in range(amount):
                    self.circulist.pop()
            case _:
                raise ValueError(f"`mode` must be either 'left' or 'right'.")

    def fragmentize(self, fragment_size: int) -> list:
        """
        Divides the `circulis` deque into fixed-size chunks and returns them as a list of lists.

        Parameters
        ----------
        fragment_size : int
            The number of elements each chunk should contain.

        Returns
        -------
        list of lists
            A list where each element is a sublist representing a chunk of the original `circulis` deque.
            The final chunk may contain fewer than `fragment_size` elements if there are not enough remaining items.

        Raises
        ------
        TypeError
            If `fragment_size` is not an integer.

        Warnings
        --------
        Logs a warning if the `circulis` deque is empty, as there will be no chunks to return.

        Notes
        -----
        - If `fragment_size` is greater than the length of `circulis`, a single chunk with all elements will be returned.
        - The function does not modify `circulis` but returns a new list of chunks.
        - A zero or negative `fragment_size` will raise a `TypeError` to ensure valid chunking behavior.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 4, 5, 6, 7])
        >>> fragments = circulis_instance.fragmentize(3)
        >>> print(fragments)
        [[1, 2, 3], [4, 5, 6], [7]]

        >>> circulis_instance.fragmentize(10)
        [[1, 2, 3, 4, 5, 6, 7]]
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning(
                f"Circulist {self.name} has an length of zero, fragmentize an empty circulist may lead to unexpected behavior."
            )

        if not isinstance(fragment_size, int):
            raise TypeError(f"Must be int, not {type(fragment_size).__name__}.")

        return list(
            list(self.circulist)[index : index + fragment_size]
            for index in range(0, len(self.circulist), fragment_size)
        )

    def indicesof(self, element: Any) -> list[int]:
        """
        Finds all indices of a specified element in the circulist.

        Parameters
        ----------
        element : any
            The element whose indices are to be found in the circulist.

        Returns
        -------
        list of int
            A tuple containing all the indices where the element is found in the circulist.
            If the element is found only once, an integer representing that index is returned.
            If the element is not found, returns 0.


        Warnings
        ------
        Logs a warning if the length of the circulist is zero, as no indices can be found.

        Notes
        -----
        - The returned tuple will contain the indices of all occurrences of the element in the circulist.
        - If only one index is found, the function will return that index as an integer, rather than a tuple.
        - If no occurrences of the element are found, the function returns an empty list.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 1, 2, 1])
        >>> circulis_instance.indicesof(1)
        [0, 3, 5]

        >>> circulis_instance.indicesof(2)
        [1, 4]

        >>> circulis_instance.indicesof(4)
        []
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning(
                f"Circulist {self.name} has an length of zero, indicesof will only return an empty list."
            )
            return []

        if element in self.circulist:
            all_indices: list[int] = [
                index for index, value in enumerate(self.circulist) if value is element
            ]
            return all_indices
        else:
            return []

    def count(self, item: Any) -> int:
        """
        Counts the number of occurrences of a specified item in the circulist.

        Parameters
        ----------
        item : any
            The item to be counted in the circulist.

        Returns
        -------
        int
            The number of times the specified item appears in the circulist.
            Returns `0` if the item is not found.

        Warnings
        ------
        Logs a warning if the length of the circulist is zero, as no items can be counted.

        Notes
        -----
        - This method uses the `Counter` class from the `collections` module to efficiently count occurrences.
        - If the circulist is empty, the method will return `0` without attempting to count any items.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 1, 2, 1])
        >>> circulis_instance.count(1)
        3

        >>> circulis_instance.count(2)
        2

        >>> circulis_instance.count(4)
        0
        """
        if self.encrypt_is_empty:  # type: ignore
            logging.warning("Count an empty circulist is unhelpful, 0 is returned.")
            return 0
        return Counter(self.circulist)[item]

    def clear(self) -> None:
        """
        Removes all elements from the circulist, effectively resetting it to an empty state.

        Returns
        -------
        None
            This method modifies the circulist in place and does not return any value.

        Notes
        -----
        - The circulist will be emptied after this method is called.
        - The circulist can be repopulated by appending or inserting elements as needed.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.clear()
        >>> print(circulis_instance)
        []  # The circulist is now empty.
        """
        self.circulist.clear()

    def sum(
        self,
        start: int | float = 0,
        *,
        error: Literal["raise", "coerce", "terminate"] = "raise",
    ) -> int | float:
        """
        Calculates the sum of elements in the circulist, starting from the given `start` value.
        Non-numerical elements are excluded from the sum.

        Parameters
        ----------
        start : int, float, optional
            The initial value to start the sum with (default is 0).

        error : Literal["raise", "coerce", "terminate"], optional
            What happens if the sum process undergo an error:
            raise: this choice will raise a ValueError, indicate invalid values inside the circulist.
            coerce: all the non-numerical values will be ignored.
            terminate: the function will return the existing sum immediately when it encounters an error.

        Returns
        -------
        int | float
            The sum of the circulist elements.

        Raises
        ------
        TypeError
            If the `start` value is not an integer or float.
        ValueError
            If error=raise and any value inside the circulist is invalid.
            If the error input is invalid.

        Warnings
        ------
        - Logs a warning if the circulist is empty, 0 will be returned.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.sum()
        6

        >>> circulis_instance.sum(5)
        11

        >>> circulis_instance.sum("invalid")
        TypeError: Invalid type for `start`.
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning("Sum an empty circulis is unhelpful, 0 is returned.")
            return 0

        if not isinstance(start, (int, float)):
            raise TypeError(
                f"Invalid type for `start`, must be int, not {type(start).__name__}."
            )
        elif error not in ["raise", "coerce", "terminate"]:
            raise ValueError(
                f"Invalid error input {error}, must be 'raise', 'coerce' or 'terminate'."
            )

        accumulate: int | float = start
        if error == "raise":
            try:
                accumulate += sum(self.circulist)
                return accumulate
            except TypeError as e:
                risky_type: str = str(e).split(" ")[7]
                raise ValueError(
                    f"Invalid adding operation between type {risky_type} and number during sum."
                )

        elif error == "coerce":
            for items in self.circulist:
                try:
                    accumulate += items
                except TypeError:
                    pass
            return accumulate

        else:
            for items in self.circulist:
                try:
                    accumulate += items
                except TypeError:
                    return accumulate
            return accumulate

    def map(self, func: Callable) -> None:
        """
        Apply a function to each item in the circulist, modifying the circulist in-place.

        Parameters
        ----------
        func : callable
            A function that will be applied to each item in the circulist.

        Returns
        -------
        None
            The circulist is modified in place, and no value is returned.

        Raises
        ------
        TypeError
            If the `func` parameter is not a callable function.

        Warnings
        ------
        - Logs a warning if the circulist is empty.

        Notes
        -----
        - This method directly modifies the circulist, replacing its elements with the results of applying `func`.
        - Ensure that `func` can handle the data types within the circulist, as it will be applied to every element.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.map(lambda x: x * 2)
        >>> print(circulis_instance)
        [2, 4, 6]

        >>> circulis_instance.map(str)
        >>> print(circulis_instance)
        ['2', '4', '6']
        """
        if not callable(func):
            raise TypeError(
                f"Invalid input type {type(func).__name__}, must be callable."
            )
        if self.encrypt_is_empty():  # type: ignore
            logging.warning("Map a function to an empty circulis is unhelpful.")
            return

        self.circulist = deque([func(items) for items in self.circulist])

    def filter(self, func: Callable) -> None:
        """
        Filter the items in the circulist, keeping only those that satisfy the condition imposed by the given function.

        Parameters
        ----------
        func : callable
            A function that is applied to each item in the circulist. Only items for which `func(item)` returns a truthy value are kept.

        Returns
        -------
        None
            The circulist is modified in place, retaining only the items that meet the condition specified by `func`.

        Raises
        ------
        TypeError
            If the `func` parameter is not callable.

        Warnings
        ------
        - Logs a warning if the circulist is empty.

        Notes
        -----
        - This method directly modifies the circulist by removing elements that do not satisfy the condition set by `func`.
        - The `func` must be designed to accept an individual item from the circulist and return a boolean value indicating whether the item should remain.

        Examples
        --------
        >>> circulis_instance = circulis([1, 2, 3, 4, 5])
        >>> circulis_instance.filter(lambda x: x % 2 == 0)
        >>> print(circulis_instance)
        [2, 4]

        >>> circulis_instance.filter(lambda x: x > 3)
        >>> print(circulis_instance)
        [4, 5]
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning("Filter an empty circulis is unhelpful.")
            return
        elif not callable(func):
            raise TypeError(
                f"Invalid input type {type(func).__name__}, must be callable."
            )

        self.circulist = deque([items for items in self.circulist if func(items)])
        return None

    def convene(self, function: Callable) -> defaultdict:
        """
        Groups elements of the circulist based on the result of a given key function.

        This method iterates over all elements in the circulist, applies the provided function to each element,
        and returns a `defaultdict` where each key corresponds to a unique category (the return value of the function).
        Elements that result in the same key are grouped together in the same list.

        Parameters
        ----------
        function : callable
            A function that takes one argument (an element of the circulist) and returns a key.
            This key is used to group the elements in the resulting dictionary.

        Returns
        -------
        defaultdict
            A dictionary-like object where:
            - Keys are the results of applying the `function` to each element.
            - Values are lists of elements that returned the same key.
            If a requested key does not exist, the dictionary will return a message:
            "Requested category hasn't been created."

        Raises
        ------
        TypeError
            If the `function` parameter is not callable.
        ValueError
            If the `function` returns `None` for any element.

        Warnings
        ------
        - Logs a warning if the circulist is empty.

        Notes
        -----
        - This method uses a `defaultdict` to return the grouped items. If a key is accessed that hasn’t been created yet, it returns a default message.
        - The `function` parameter must not return `None` for any element; if it does, a `ValueError` is raised.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3, 4, 5, 6])
        >>> result = circulis_instance.convene(lambda x: x % 2)  # Group by even or odd
        >>> result
        defaultdict({1: [1, 3, 5], 0: [2, 4, 6]})
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning("Convene an empty circulis is unhelpful.")

        if not callable(function):
            raise TypeError(
                f"function {function} must be callable, not {type(function).__name__}."
            )

        return_dict: dict = {}
        for items in self.circulist:
            new_key: Any = function(items)
            if new_key is None:
                raise ValueError(f"Function {function} must not return `None`.")
            elif new_key not in return_dict:
                return_dict[new_key] = []

            return_dict[new_key].append(items)

        def message() -> Literal["Requested category hasn't been created."]:
            return "Requested category hasn't been created."

        return defaultdict(message, return_dict)

    def shuffle(self) -> None:
        """
        Shuffle the circulist in place.

        This method randomly shuffles the elements of the circulist using the Fisher-Yates shuffle algorithm.
        The shuffle is performed in place, meaning that the circulist is modified directly.

        Returns
        -------
        None
            This method does not return any value; it modifies the circulist in place.

        Raises
        ------
        ValueError
            If the circulist is empty (this case is silently handled).

        Warnings
        ------
        - Logs a warning if the length of the circulist is zero (indicating that there is nothing to shuffle).

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3, 4])
        >>> circulis_instance.shuffle()  # The elements are shuffled in place
        >>> print(circulis_instance)
        [4, 2, 1, 3]  # Example of shuffled order
        """
        length: int = len(self.circulist)
        if not length:
            logging.warning("Filter an empty circulis is unhelpful.")
            return

        swapped_index: list[int] = (
            []
        )  # avoid shuffle a single element multiple times due to changed index.
        for index in range(length):
            if index in swapped_index:
                continue
            swap_index: int = randint(index, length - 1)
            swapped_index.append(swap_index)
            self.circulist[index], self.circulist[swap_index] = (
                self.circulist[swap_index],
                self.circulist[index],
            )
        del swapped_index

    def synergy(
        self, other_list: circulis | list | deque | tuple, function: Callable
    ) -> list:
        """
        Zip the circulist with another list-like object and apply a function to each pair of elements.

        This method combines the elements from the circulist and another provided list-like object
        (such as a list, deque, tuple, or circulis), and applies the provided function to each pair of
        elements from the two lists. The result of the function is collected in a new list.

        Parameters
        ----------
        other_list : circulis | list | deque | tuple
            A list-like object that will be zipped with the circulist. It should have the same length as the circulist.

        function : callable
            A function that accepts two arguments (one from the circulist and one from `other_list`) and returns a value
            other than None. This function will be applied to each pair of elements from the two lists.

        Returns
        -------
        list
            A new list containing the result of applying the function to each pair of elements from the two lists.

        Raises
        ------
        TypeError
            If `other_list` is not a valid list-like object (such as circulis, list, deque, or tuple), or if `function`
            is not callable.

        ValueError
            If the provided `function` does not accept exactly two arguments.

        Warnings
        ------
        Logs a warning if the lengths of the circulist and `other_list` do not match.
        Logs a warning if the circulist is empty.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> other_list = [4, 5, 6]
        >>> circulis_instance.synergy(other_list, lambda x, y: x + y)
        [5, 7, 9]
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning("Synergy an empty circulis is unhelpful.")
            return []

        self.encrypt_list_check(other_list)  # type: ignore
        if not callable(function):
            raise TypeError(f"Function {function} must be callable.")
        if len(inspect.signature(function).parameters) != 2:
            raise ValueError(
                f"Function {function} must take exactly two arguments, not {len(inspect.signature(function).parameters)}."
            )
        if len(self.circulist) != len(list(other_list)):
            logging.warning("Length of two zipped lists isn't congruent.")

        return [function(a, b) for a, b in zip(self.circulist, list(other_list))]

    def voidfilter(self) -> None:
        """
        Inplace remove all the None.

        This property filters out any `None` values in the circulist.

        Returns
        -------
        None
            Inplace operation

        Example
        -------
        >>> circulis_instance = circulis([1, None, 3, None, 5])
        >>> print(circulis_instance.voidfilter())
        [1, 3, 5]
        """
        self.circulist = deque(filter(lambda x: x is not None, self.circulist))
        return None

    def reduce(
        self,
        function: Callable,
        start: Any,
        type: Literal["int", "float", "bool", "str", "any"],
    ):
        step: int = len(inspect.signature(function).parameters)
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError("Reduce an empty circulis is invalid.")
        elif not callable(function):
            raise TypeError(f"Function {function} must be callable.")
        elif step <= 2:
            raise ValueError(
                f"Function {function} must take more than two arguments, not {step}."
            )
        match type:
            case "any":
                ...
            case "int":
                if not isinstance(start, int):
                    raise ValueError(
                        "Start value's type and return type isn't congruent."
                    )
            case "float":
                if not isinstance(start, float):
                    raise ValueError(
                        "Start value's type and return type isn't congruent."
                    )
            case "str":
                if not isinstance(start, str):
                    raise ValueError(
                        "Start value's type and return type isn't congruent."
                    )
            case "bool":
                if not isinstance(start, bool):
                    raise ValueError(
                        "Start value's type and return type isn't congruent."
                    )
            case _:
                raise ValueError("Type must be `int`, `float`, `bool` or `int`.")

        converted_deque = list(deepcopy(self.circulist))
        result = start
        step -= 1
        for index in range(0, len(converted_deque), step):
            items = converted_deque[index : step + index]
            if len(items) != step:
                return result
            result = function(result, *items)

        return result

    def pop(self, direction: Literal["left", "right"] = "right") -> Any:
        """Standardized pop method

        Args:
            direction (Literal[&quot;left&quot;, &quot;right&quot;], optional): _description_. Defaults to "right".

        Raises:
            ValueError: _description_

        Returns:
            Any: the pop value
        """
        match direction:
            case "left":
                return self.circulist.pop()
            case "right":
                return self.circulist.popleft()
            case _:
                raise ValueError(
                    f"Invalid input type {type(direction).__name__}, must be `left` or `right`."
                )

    @deprecated(
        reason="using sort + index",
        version="1.1.4",
    )
    def percentile(self, percentage: float) -> float | int:
        if not isinstance(percentage, float):
            raise TypeError(
                f"`percentage` must be float, not {type(percentage).__name__}."
            )
        elif not (0 < percentage < 0.99):
            raise ValueError("Percentage must be between 0 and 0.99 (exclusive).")

        elif len(self.circulist) <= 1:
            raise ValueError(
                f"Only {len(self.circulist)} value inside the circulist? Maybe you intend to use other methods?"
            )

        length: int = len(self.circulist)
        above: int = math.ceil(length * percentage) + 1
        below: int = length - above

        percentile_dictionary: dict[str, Any] = {
            "status": ["dominant", "recess"],
            "peak": 100_000_000,
            "trough": -100_000_000,
            "above": above,
            "below": below,
        }

        complete: bool | float | int = False

        def pioneer_obtain() -> Generator:
            nonlocal complete
            for elements in self.circulist:
                # Active the debug message if an error occurs.
                # logging.debug(f"Checking element: {element}, Range: ({percentile_dictionary['trough']}, {percentile_dictionary['peak']})")

                if (
                    percentile_dictionary["trough"]
                    < elements
                    < percentile_dictionary["peak"]
                ):
                    # valid item, stop looping
                    yield elements
                    break
            else:
                # an unexpected error occurred here
                logging.warning(
                    f"{percentage} is too close to 1, do you mean the biggest element?"
                )
                complete = max(self.circulist) if max(self.circulist) else 0.01
                # raise Exception("An unexpected error occurred, enable debug message or connect developer.")

        def comparison(pioneer) -> None:
            nonlocal percentile_dictionary, complete
            aggregate_surplus: int = sum(
                1 for elements in self.circulist if pioneer >= elements
            )
            aggregate_shortage: int = sum(
                1 for elements in self.circulist if pioneer <= elements
            )

            if (
                percentile_dictionary["above"] == aggregate_surplus
                or percentile_dictionary["below"] == aggregate_shortage
            ):
                # This is the exact value in the circulist, set complete to True
                complete = pioneer if pioneer else 0.01
            else:
                match (
                    aggregate_surplus > percentile_dictionary["above"],
                    aggregate_shortage > percentile_dictionary["below"],
                ):
                    case (True, True):
                        # This pioneer is the expected element, set complete to True
                        complete = pioneer if pioneer else 0.01

                    case (True, False):
                        # This pioneer is too big, the percentile between trough and pioneer
                        percentile_dictionary["peak"] = pioneer

                    case (False, True):
                        # This pioneer is too small, the percentile between pioneer and peak
                        percentile_dictionary["trough"] = pioneer

                    case _:
                        raise NotImplementedError("Error in comparison algorithm.")

        while not complete:
            try:
                pioneer: int | float = next(pioneer_obtain())
            except StopIteration:
                break
            comparison(pioneer)
        return complete

    # circulis property
    @property
    def stride(self) -> list:
        """
        Calculate the difference between adjacent items in the circulist.

        This property calculates the difference between each pair of adjacent values in the circulist.
        The circulist must only contain numerical values for this calculation to be valid. If the list
        contains fewer than two elements or non-numerical values, an exception will be raised.

        Returns
        -------
        list
            A list of differences between adjacent items in the circulist.

        Raises
        ------
        ValueError
            - If the circulist contains fewer than two elements.
            - If the circulist contains non-numerical values.

        Example
        -------
        >>> circulis_instance = circulis([10, 20, 30])
        >>> circulis_instance.stride
        [10, 10]
        """
        if len(self.circulist) <= 1:
            raise ValueError(
                f"Length of the circulist must be 2 or more, not {len(self.circulist)}."
            )
        if not self.encrypt_is_numeric(self.circulist):  # type: ignore
            raise ValueError("The circulist contains non-numerical values.")

        return [
            self.circulist[index + 1] - self.circulist[index]
            for index in range(len(self.circulist) - 1)
        ]

    @property
    def mean(self) -> float:
        """
        Calculate the mean (average) of the numerical values in the circulist.

        This property filters out non-numerical items from the circulist and then calculates
        the mean (average) of the remaining values. The result is rounded to two decimal places.

        Returns
        -------
        float
            The mean of the numerical values in the circulist, rounded to two decimal places.

        Raises
        ------
        ValueError: if the length of the circulist is zero or the length of the circulist after filter is zero.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.mean
        2.0

        >>> circulis_instance = circulis([None, "string", 5])
        >>> circulis_instance.mean
        5.0
        """
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError("An empty circulis doesn't have a mean value")
        numerical_circulist: list = self.encrypt_filter(self.circulist)  # type: ignore
        if len(numerical_circulist):
            return round(sum(numerical_circulist) / len(numerical_circulist), 2)
        else:
            raise ValueError(
                "An empty circulis (after filter) doesn't have a mean value."
            )

    @property
    def median(self) -> Any:
        """
        Calculate the median value of the circulist.

        This property calculates the median of the circulist. If the circulist has an odd
        number of elements, the middle element is returned.

        Returns
        -------
        Any
            The median value of the circulist.

        Raises
        ------
        ValueError
            If the length of the circulist is zero.

        Warnings
        ------
        Logs a warning if the length of the circulist is zero.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3, 4, 5])
        >>> circulis_instance.median
        3

        >>> circulis_instance = circulis([1, 2])
        >>> circulis_instance.median
        2
        """
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError(
                f"A circulist with a length of zero do not have a median value."
            )
        return self.circulist[len(self.circulist) // 2]

    @property
    def dominant(self) -> tuple[Any, int]:
        """
        Return the most frequent element in the circulist and its occurrence count.

        This property uses the `Counter` class to find the most common element in the circulist and
        returns a tuple containing the most frequent element and the number of times it appears.

        Returns
        -------
        tuple[any, int]
            A tuple with two values: the most frequent element and its frequency (the count of occurrences).

        Raises
        ------
        ValueError: if the length of the circulist is zero.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 2, 3, 3, 3])
        >>> circulis_instance.dominant
        (3, 3)
        """
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError(
                "An circulist with a length of zero do not have a dominant value."
            )
        return Counter(self.circulist).most_common(1)[0]

    @property
    def pair(self) -> list:
        """
        Group the items inside the circulist into tuples of two.

        This property groups the items in the circulist into pairs of two items. If the number of items
        in the circulist is odd, a `None` value is appended to the end to complete the last tuple.

        Returns
        -------
        list
            A list of tuples, where each tuple contains two items. If the circulist length is odd, the last tuple
            contains one element and `None`.

        Raises
        ------
        ValueError: if the length of the circulist is zero.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3, 4])
        >>> circulis_instance.pair
        [(1, 2), (3, 4)]

        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.pair
        [(1, 2), (3, None)]
        """
        if self.encrypt_is_empty():  # type: ignore
            raise ValueError("Pair an empty circulist is invalid.")
        if len(self.circulist) % 2 == 1:
            self.circulist.append(None)

        return [
            tuple(list(self.circulist)[index : index + 2])
            for index in range(0, len(self.circulist), 2)
        ]

    @property
    def empty(self) -> bool:
        """
        Check if the circulist is empty.

        This property checks if the circulist contains any elements. It returns `True` if the circulist is empty
        (i.e., has no elements), otherwise it returns `False`.

        Returns
        -------
        bool
            `True` if the circulist is empty, `False` if it is not empty.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.empty
        False

        >>> circulis_instance = circulis([])
        >>> circulis_instance.empty
        True
        """
        return not bool(len(self.circulist))

    def reverse(self) -> None:
        """
        Reverse the circulis inplace.

        Returns
        -------
        None
            Inplace operation

        Warnings
        ------
        Logs a warning if the length of the circulist is zero.

        Example
        -------
        >>> circulis_instance = circulis([1, 2, 3])
        >>> circulis_instance.reverse()
        >>> print(circulis_instance)
        [3, 2, 1]
        """
        if self.encrypt_is_empty():  # type: ignore
            logging.warning("Reverse an empty circulist doesn't change anything.")
        self.circulist = deque(list(self.circulist)[::-1])
        return None

    # ancillary method
    def _append_list(self, mode, filter_None, arguments) -> None:
        """
        - Private method, don't use it outside the class.
        """
        if filter_None:
            arguments = list(filter(lambda item: item is not None, arguments))

        if mode == "right":
            self.circulist.extend(arguments)
        else:
            self.circulist.extendleft(reversed(arguments))

    def _append_general(self, mode, argument) -> None:
        """
        - Private method, don't use it outside the class.
        """
        if mode == "right":
            self.circulist.append(argument)
        else:
            self.circulist.appendleft(argument)

    def _list_check(self, input_object) -> None:
        """
        - Private method, don't use it outside the class.
        """
        if not isinstance(input_object, (deque, circulis, list, tuple)):
            raise TypeError(
                f"Invalid input type {type(input_object).__name__}, must be deque, circulis, list or tuple."
            )

    def _is_numeric(self, lst) -> bool:
        """
        - Private method, don't use it.
        """
        return all(
            isinstance(item, (int, float)) and not isinstance(item, bool)
            for item in lst
        )

    def _compare_lists(self, self_list, other_list, operator) -> bool:
        """
        - Private method, don't use it outside the class.
        """
        self.encrypt_list_check(other_list)  # type: ignore
        other: list = (
            list(other_list) if not isinstance(other_list, list) else other_list
        )
        match (self.encrypt_is_numeric(self_list), self.encrypt_is_numeric(other_list)):  # type: ignore
            case (True, True):
                self_sum: int = sum(self_list)
                other_sum: int = sum(other)
            case _:
                self_sum = sum(bool(item) for item in self_list)
                other_sum = sum(bool(item) for item in other)

        match operator:
            case "<":
                return self_sum < other_sum
            case ">":
                return self_sum > other_sum
            case "<=":
                return self_sum <= other_sum
            case ">=":
                return self_sum >= other_sum
            case _:
                raise ValueError(f"Invalid operator: {operator}")

    def _filter(self, circulist) -> list:
        """
        - Private method, don't use it outside the class.
        """
        return list(
            filter(
                lambda x: isinstance(x, (float, int)) and not isinstance(x, bool),
                circulist,
            )
        )

    def _is_empty(self) -> bool:
        """
        - Private method, don't use it outside the class.
        """
        if len(self.circulist):
            return False
        return True

    def _hashify(self, object: Any) -> Hashable:
        """
        - Private method, don't use it outside the class.
        """
        if isinstance(object, Hashable):
            return object
        elif isinstance(object, Iterable):
            return tuple(self.encrypt_hashify(value) for value in object)  # type: ignore
        else:  # bad object
            pass

    def _to_set(self, object: Iterable) -> set:
        """
        - Private method, don't use it outside the class.
        """
        return {self.encrypt_hashify(item) for item in object}  # type: ignore

    # overwrite the dunder method
    def __class_getitem__(cls, item) -> type[Self]:
        return cls

    def __hash__(self) -> int:
        """
        Make the circulist hashable by recursively turning all the items into tuple, then hash them.

        Returns:
            Int: the integer of the final result.
        """
        return hash(self.encrypt_hashify(self.circulist))  # type: ignore

    def __lt__(self, other) -> bool:
        """
        Compare the circulis with another list-like object for 'less than'.

        - If both circulis and other contain only numeric values:
            Returns True if the sum of circulis elements is less than the sum of other elements.
        - If circulis or other contain non-numeric values:
            Returns True if the sum of values that evaluate to True in circulis is less than the sum of values that evaluate to True in other.

        Returns:
        - bool: True if the circulis meets the 'less than' condition, based on the above rules.
        """
        return self.encrypt_compare_lists(list(self.circulist), other, "<")  # type: ignore

    def __gt__(self, other) -> bool:
        """
        Compare the circulis with another list-like object for 'greater than'.

        - If both circulis and other contain only numeric values:
            Returns True if the sum of circulis elements is greater than the sum of other elements.
        - If circulis or other contain non-numeric values:
            Returns True if the sum of values that evaluate to True in circulis is greater than the sum of values that evaluate to True in other.

        Returns:
        - bool: True if the circulis meets the 'greater than' condition, based on the above rules.
        """
        return self.encrypt_compare_lists(list(self.circulist), other, ">")  # type: ignore

    def __le__(self, other) -> bool:
        """
        Compare the circulis with another list-like object for 'less than or equal to'.

        - If both circulis and other contain only numeric values:
            Returns True if the sum of circulis elements is less than or equal to the sum of other elements.
        - If circulis or other contain non-numeric values:
            Returns True if the sum of values that evaluate to True in circulis is less than or equal to the sum of values that evaluate to True in other.

        Returns:
        - bool: True if the circulis meets the 'less than or equal to' condition, based on the above rules.
        """
        return self.encrypt_compare_lists(list(self.circulist), other, "<=")  # type: ignore

    def __ge__(self, other) -> bool:
        """
        Compare the circulis with another list-like object for 'greater than or equal to'.

        - If both circulis and other contain only numeric values:
            Returns True if the sum of circulis elements is greater than or equal to the sum of other elements.
        - If circulis or other contain non-numeric values:
            Returns True if the sum of values that evaluate to True in circulis is greater than or equal to the sum of values that evaluate to True in other.

        Returns:
        - bool: True if the circulis meets the 'greater than or equal to' condition, based on the above rules.
        """
        return self.encrypt_compare_lists(list(self.circulist), other, ">=")  # type: ignore

    def __getitem__(self, index) -> Any:
        """
        Retrieve an element or a slice from the circulist.

        This method allows accessing elements in the circulist by their index or
        obtaining a sublist using slicing. If a slice is provided, it returns a
        new deque containing the sliced elements. If an integer index is provided,
        it returns the corresponding element.

        Parameters:
        ----------
        index : int or slice
            The index of the element to retrieve or a slice object to obtain a subset.

        Returns:
        -------
        Any
            The element at the specified index or a deque containing the sliced elements.

        Raises:
        ------
        TypeError
            If the index is not of type `int` or `slice`.

        Warnings:
        --------
        Logs a warning if a negative index is used. The warning includes the index value
        and the name of the circulist for easier debugging.

        Notes:
        -----
        - Using a slice returns a new `deque` object, not a list.
        - The circulist supports both positive and negative indexing.
        """
        if isinstance(index, slice):
            # deque object is not sliceable
            return deque(list(self.circulist)[index])  # type: ignore

        elif isinstance(index, int):
            if index < 0:
                logging.warning(
                    f"Negative index {index} for circulist object {self.name}."
                )
                return self.circulist[index]
            else:
                return self.circulist[index]
        else:
            raise TypeError(f"Index must be int, not {type(index).__name__}.")

    def __str__(self) -> str:
        """
        Return a string representation of the circulist.

        This method provides a string representation of the circulist's contents
        by converting the underlying deque into a list format.

        Returns:
        -------
        str
            A string representation of the circulist with its elements displayed
            as a list, e.g., "[item1, item2, item3]".
        """
        return str(list(self.circulist))

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the circulist object.

        This method returns a string that includes both the name of the circulist
        and its contents, formatted as a list. It is intended to provide a clear
        and unambiguous representation of the circulist for debugging and logging.

        Returns:
        -------
        str
            A string in the format: "Name: <name>, Circulist: [item1, item2, ...]".
        """
        return f"Name: {self.name}, Circulist: {list(self.circulist)}"

    def __len__(self) -> int:
        """
        Return the number of elements in the circulis.

        This method returns the length of the circulis, which represents the number of elements
        contained in the underlying data structure.

        Returns:
            int: The number of elements in the circulis.
        """
        return len(self.circulist)

    def __iter__(self) -> Iterator:
        """
        Return an iterator over the circulis elements.

        This method allows the circulis to be iterated over in a for-loop or other contexts
        that require an iterable.

        Returns:
            Iterator: An iterator object that iterates over the elements of the circulis.
        """
        return iter(self.circulist)

    def __setitem__(self, index: int | slice, value: Any) -> None:  # type: ignore
        """
        Set an element or a slice of elements in the circulis.

        This method allows setting a single element at a specified index or setting multiple elements
        using a slice. If the index is a slice, the circulis is temporarily converted to a list
        for the assignment, and then converted back to a deque.

        Parameters:
            index (int | slice): The index or slice where the value should be set.
            value (Any): The value to assign at the specified index or slice.

        Raises:
            TypeError: If the index is not an integer or a slice.
        """
        if isinstance(index, slice):
            self.circulist = list(self.circulist)  # type: ignore
            self.circulist[index] = value  # type: ignore
            self.circulist = deque(self.circulist)
        elif isinstance(index, int):
            self.circulist[index] = value
        else:
            raise TypeError(f"Must be int, not {type(index).__name__}.")

    def __delitem__(self, index: int) -> None:  # type: ignore
        """
        Delete an element from the circulis at the specified index.

        This method removes the element at the given index from the circulis. If the index is invalid
        or not an integer, a TypeError will be raised.

        Parameters:
            index (int): The index of the element to delete.

        Raises:
            TypeError: If the index is not an integer.
        """
        if not isinstance(index, int):
            raise TypeError(f"Must be int, nor {type(index).__name__}.")
        del self.circulist[index]

    def __contains__(self, value: Any) -> bool:
        """
        Check if a value is present in the circulis.

        This method checks if the specified value exists within the circulis. It returns True if the value
        is found, and False otherwise.

        Parameters:
            value (Any): The value to check for presence in the circulis.

        Returns:
            bool: True if the value is in the circulis, False otherwise.
        """
        return value in self.circulist

    def __eq__(self, other: object) -> bool:
        """
        Check if two circulis or list-like objects are equal.

        This method compares the current circulis object with another object (such as a deque,
        circulis, list, or tuple). It returns True if both objects are of the same type and contain
        the same elements in the same order. Otherwise, it returns False.

        Parameters:
            other (object): The object to compare against the current circulis object.

        Returns:
            bool: True if the two objects are equal, False otherwise.
        """
        if not isinstance(other, (deque, circulis, list, tuple)):
            return False
        return (
            list(self.circulist) == list(other)
            if not isinstance(other, list)
            else list(self.circulist) == other
        )

    def __add__(self, other: deque | circulis | list | tuple) -> circulis:
        """
        Concatenate another list-like object to the circulis and return a new circulis.

        This method creates a new circulis by concatenating the elements of the current circulis
        with those of another list-like object (deque, circulis, list, or tuple). The result is a new
        circulis instance containing all the elements from both objects.

        Parameters:
            other (deque | circulis | list | tuple): The list-like object to concatenate with the current circulis.

        Returns:
            circulis: A new circulis instance containing the concatenated elements.

        Raises:
            TypeError: If the 'other' object is not a supported list-like type.
        """
        self.encrypt_list_check(other)  # type: ignore
        return (
            circulis(list(self.circulist) + list(other))
            if not isinstance(other, list)
            else circulis(list(self.circulist) + other)
        )

    def __radd__(self, other: deque | circulis | list | tuple) -> circulis:
        """
        Concatenate another list-like object to the circulis and return a new circulis.

        This method creates a new circulis by concatenating the elements of the current circulis
        with those of another list-like object (deque, circulis, list, or tuple). The result is a new
        circulis instance containing all the elements from both objects.

        Parameters:
            other (deque | circulis | list | tuple): The list-like object to concatenate with the current circulis.

        Returns:
            circulis: A new circulis instance containing the concatenated elements.

        Raises:
            TypeError: If the 'other' object is not a supported list-like type.
        """
        self.encrypt_list_check(other)  # type: ignore
        return (
            circulis(list(other) + list(self.circulist))
            if not isinstance(other, list)
            else circulis(other + list(self.circulist))
        )

    def __reversed__(self) -> circulis:
        """
        Return a reversed version of the circulis.

        This method returns a new circulis instance that contains the elements of the current
        circulis in reverse order.

        Returns:
            circulis: A new circulis instance with the elements in reverse order.
        """
        return circulis(list(self.circulist))[::-1]

    def __format__(self, format_spec: str) -> str:
        """
        Format the circulis as a string, list, tuple, or deque based on the format_spec.

        This method allows the `circulis` object to be formatted in different ways, depending on the
        provided `format_spec`. If no `format_spec` is given or if it is an unrecognized value,
        the circulis will be formatted as a list.

        Parameters:
            format_spec (str): The desired format for the circulis object. Valid options are:
                - "str": Formats the circulis as a concatenated string of elements.
                - "list": Formats the circulis as a list of elements (default).
                - "tuple": Formats the circulis as a tuple of elements.
                - "deque": Formats the circulis as a deque (default string representation).
                - "": Formats the circulis as a list (same as "list").

        Returns:
            str: The formatted circulis as a string representation of the requested format.

        Raises:
            ValueError: If the `format_spec` is invalid (not one of the supported values).
        """
        match format_spec:
            case "str":
                return "".join(map(lambda x: str(x), list(self.circulist)))
            case "list":
                return str(list(self.circulist))
            case "tuple":
                return str(tuple(self.circulist))
            case "deque":
                return str(self.circulist)
            case "":
                return str(list(self.circulist))
            case _:
                logging.warning(
                    f"Invalid input {format_spec}, must be regular expression."
                )
                return str(list(self.circulist))

    def __or__(self, other: list | deque | circulis | tuple) -> set:
        """
        Return the union of the circulis and another list-like object.

        This method supports the `|` operator, which computes the union of the current `circulis`
        object and another list-like object (either a `list`, `deque`, `circulis`, or `tuple`).
        The union operation returns a set containing all unique elements from both objects.

        Parameters:
            other (list | deque | circulis | tuple): The list-like object to perform the union with.

        Returns:
            set: A set containing the unique elements from both the circulis and the other object.

        Raises:
            TypeError: If `other` is not a supported list-like type.
        """
        self.encrypt_list_check(other)  # type: ignore
        first: set = self.encrypt_to_set(self.circulist)  # type: ignore
        second: set = self.encrypt_to_set(other)  # type: ignore
        return first | second

    def __and__(self, other: list | deque | circulis | tuple) -> set:
        """
        Return the intersection of the circulis and another list-like object.

        This method supports the `&` operator, which computes the intersection of the current
        `circulis` object and another list-like object (either a `list`, `deque`, `circulis`, or `tuple`).
        The intersection operation returns a set containing only the elements that are present in both
        the circulis and the other object.

        Parameters:
            other (list | deque | circulis | tuple): The list-like object to perform the intersection with.

        Returns:
            set: A set containing the elements that are common to both the circulis and the other object.

        Raises:
            TypeError: If `other` is not a supported list-like type.
        """
        self.encrypt_list_check(other)  # type: ignore
        first: set = self.encrypt_to_set(self.circulist)  # type: ignore
        second: set = self.encrypt_to_set(other)  # type: ignore
        return first & second

    def __xor__(self, other: list | deque | circulis | tuple) -> set:
        """
        Return the symmetric difference between the circulis and another list-like object.

        This method supports the `^` operator, which computes the symmetric difference between
        the current `circulis` object and another list-like object (either a `list`, `deque`,
        `circulis`, or `tuple`). The symmetric difference returns a set containing elements that
        are unique to each object (i.e., elements that are in either the circulis or the other
        object, but not in both).

        Parameters:
            other (list | deque | circulis | tuple): The list-like object to perform the symmetric
                difference with.

        Returns:
            set: A set containing the elements that are unique to each object (i.e., the symmetric
                difference between the circulis and the other object).

        Raises:
            TypeError: If `other` is not a supported list-like type.
        """
        self.encrypt_list_check(other)  # type: ignore
        first: set = self.encrypt_to_set(self.circulist)  # type: ignore
        second: set = self.encrypt_to_set(other)  # type: ignore
        return first ^ second

    def __sub__(self, other: list | deque | circulis | tuple) -> circulis:
        """
        Return the difference between the circulis and another list-like object.

        This method supports the `-` operator, which computes the difference between the
        current `circulis` object and another list-like object (either a `list`, `deque`,
        `circulis`, or `tuple`). The difference operation returns a set containing elements
        that are in the circulis but not in the other object.

        Parameters:
            other (list | deque | circulis | tuple): The list-like object to subtract from
                the circulis.

        Returns:
            circulis: A new circulis instance containing the subtracted elements.

        Raises:
            TypeError: If `other` is not a supported list-like type.
        """
        self.encrypt_list_check(other)  # type: ignore
        first: set = self.encrypt_to_set(self.circulist)  # type: ignore
        second: set = self.encrypt_to_set(other)  # type: ignore
        return circulis(list(first - second))

    def __mul__(self, n: int) -> circulis:
        """
        Repeat the elements of the circulis n times.

        This method supports the `*` operator, which repeats the elements of the
        `circulis` object `n` times. The resulting `circulis` will contain the same
        elements as the original, but repeated `n` times in sequence.

        Parameters:
            n (int): The number of times to repeat the elements of the circulis.
                    Must be a non-negative integer.

        Returns:
            circulis: A new circulis object containing the elements repeated `n` times.

        Raises:
            TypeError: If `n` is not an integer.
            ValueError: If `n` is a negative integer.
        """
        if not isinstance(n, int):
            raise TypeError(f"Must be int, not {type(n).__name__}")
        return circulis(list(self.circulist) * n)

    def __copy__(self) -> deque:  # type: ignore
        """
        Create a shallow copy of the `circulist` attribute.

        This method uses the `copy` function to create a new deque instance
        that shares the same elements as the original `circulist`, without
        duplicating nested or referenced objects.

        Returns:
            deque: A shallow copy of the `circulist` attribute.
        """
        return copy(self.circulist)

    def __deepcopy__(self) -> deque:
        """
        Create a deep copy of the `circulist` attribute.

        This method uses the `deepcopy` function to create a new deque instance
        that is a fully independent copy of the original `circulist`, recursively
        duplicating all nested or referenced objects.

        Returns:
            deque: A deep copy of the `circulist` attribute.
        """
        return deepcopy(self.circulist)

    def __next__(self) -> Any:
        """
        Return the next element in the sequence.

        This method retrieves the next element from the `circulist` attribute's iterator.
        If the `_iterator` attribute does not exist, it initializes it as an iterator
        over `circulist`. When the end of the iterator is reached, a `StopIteration`
        exception is raised, signaling the end of the sequence.

        Returns:
            Any: The next element in the sequence.

        Raises:
            StopIteration: Raised when the iterator has no more elements.
        """
        if not hasattr(self, "_iterator"):
            self._iterator = iter(self.circulist)

        return next(self._iterator)

    def __bool__(self) -> bool:
        return True if len(self.circulist) else False

    def __ne__(self, other) -> bool:
        return not self.circulist.__eq__(other)

    def __iadd__(self, other) -> circulis:
        self.encrypt_list_check(other)  # type: ignore
        self.circulist.extend(other)
        return self

    def __isub__(self, other) -> circulis:
        self.encrypt_list_check(other)  # type: ignore
        for values in other:
            for items in self.circulist:
                if values == items:
                    self.circulist.remove(items)

        return self

    def __neg__(self) -> circulis:
        result = deque([])
        for value in self.circulist:
            if not isinstance(value, (int, float)):
                result.append(...)
            else:
                result.append(-value)
        return circulis(result)

    def __pos__(self) -> circulis:
        result = deque([])
        for value in self.circulist:
            if not isinstance(value, (int, float)):
                continue
            else:
                result.append(value)

        return circulis(result)

    def __abs__(self) -> circulis:
        result = deque([])
        for value in self.circulist:
            if isinstance(value, bool):
                result.append(1 if value else 0)
            elif isinstance(value, (int, float)):
                result.append(abs(value))
            elif isinstance(value, str) or isinstance(value, Iterable):
                if hasattr(value, "__len__"):
                    result.append(len(value))  # type: ignore
                else:
                    result.append(1)
            else:
                result.append(1)

        return circulis(result)

    def __imul__(self, n):
        if not isinstance(n, int):
            raise TypeError(f"Cannot multiply {self.name} by an {type(n).__name__}.")

        for _ in range(n):
            self.circulist.extend(self.circulist)

        return self

    def __pow__(self, n) -> circulis:
        result = deepcopy(self.circulist)
        if not isinstance(n, int):
            raise TypeError(f"Invalid input type {type(n).__name__}, must be int.")
        elif n < 0:
            raise ValueError(f"`n` must be a positive integer.")

        if len(self.circulist) * n >= 50:
            return circulis([math.inf])
        elif n == 0:
            return circulis([1])
        else:
            while n > 0:
                result.append(self.circulist * n)
                n -= 1
        return circulis(result)

    @deprecated(
        reason="Association doesn't work as expected, noticing that the dependent circulist's value will be changed.",
        version="1.1.0",
    )
    def __matmul__(self, dependent_circulist: circulis | None = None) -> None:
        match dependent_circulist:
            case None:
                circulist_copy: deque = self.__copy__(shallow=False)
                self.circulist = circulist_copy

            case circulis():
                # store the information
                circulist_name: str = self.name
                circulist_items: list = [items for items in self.circulist]

                # associate two circulist
                self.circulist: deque = dependent_circulist.circulist
                self.circulist.clear()
                self.circulist.extend(circulist_items)
                self.name: str = circulist_name

            case _:
                raise TypeError(
                    f"Invalid input type {type(dependent_circulist).__name__}, must be circulis or None."
                )

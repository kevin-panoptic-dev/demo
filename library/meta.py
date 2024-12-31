from __future__ import annotations
import logging
import re
import inspect
from time import sleep
from sys import exit as terminate
from os import _exit as disrupt
from copy import copy, deepcopy
from typing import Callable, NoReturn, Any
from rich.text import Text
from rich import print as rt
from pprint import pprint as pt

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


class metaclarion(type):
    """
    A metaclass that enables dynamic behavior and custom handling of class attributes, methods, and dunder methods.

    The `metaclarion` metaclass provides a robust mechanism for dynamically managing class-level attributes, methods, and
    special behavior for private and public attributes. This metaclass enhances the flexibility of class creation by
    enabling custom behavior for initialization, attribute assignment, and method definitions.

    Key Features:
    - Supports dynamic method assignment, including lambda functions.
    - Automatically adds common methods (`static_display`, `dynamic_display`) for class inspection.
    - Customizes the handling of class attributes that start with underscores (`_`) by "encrypting" their names.
    - Adds default `__repr__` and `__copy__` methods if they are not defined in the class.
    - Registers newly created classes in an `inheritance` dictionary for automatic tracking.
    - Provides debugging methods for static and dynamic display of class details and instance methods.

    Attributes:
    - inheritance (dict): A dictionary that keeps track of the classes created with this metaclass, keyed by their names.
    - name_dict (dict): A dictionary mapping Python data types to specific class attributes, e.g., lists to `class_list`.
    - PARENT_CLASS_REPRESENTATION (Callable, optional): A reference to the `__str__` method for the base class, used if
      a subclass does not define its own `__str__`.
    - PARENT_CLASS_DEEPCOPY (Callable, optional): A reference to the `__copy__` method for the base class, used if
      a subclass does not define its own `__copy__`.

    Methods:
    - `__new__(cls, class_name, bases, attrs)`: Creates a new class with encrypted names for private attributes,
      handles base class distinction, and auto-registers the class.
    - `__init__(cls, class_name, bases, attrs)`: Initializes the metaclass, defines default methods (`__init__`,
      `static_display`, `dynamic_display`), and ensures dynamic OOP functionality.
    - `__call__(cls, *args, **kwargs)`: Enables dynamic method assignment and manages the behavior of instance-level
      methods, including custom string representation (`__str__`) and deep copy (`__copy__`).

    Parameters:
    - class_name (str): The name of the class being created.
    - bases (tuple): A tuple of base classes for the new class.
    - attrs (dict): A dictionary containing the attributes and methods of the class being created.

    Returns:
    - Type: The newly created class, with dynamic behavior and additional methods as defined by the metaclass.

    Notes:
    - This metaclass is designed for advanced use cases where dynamic class behavior, private attribute handling,
      and method customization are required.
    - It provides significant flexibility for classes that need custom initialization, dynamic method assignment,
      or debugging utilities.
    """

    inheritance: dict = {}
    name_dict: dict[str, str] = {
        "list": "class_list",
        "dictionary": "class_dictionary",
        "set": "class_set",
        "circulis": "class_circulis",
        "DataFrame": "class_DataFrame",
    }
    __PARENT_CLASS_REPRESENTATION = None  # type: ignore
    __PARENT_CLASS_DEEPCOPY = None  # type: ignore

    def __new__(
        cls, class_name: str, bases: tuple[type, ...], attrs: dict[str, Any]
    ) -> metaclarion:
        """
        Create and return a new class with special handling for private attributes and class registration.

        This method is responsible for constructing a new class using the `public` metaclass. It performs
        several key tasks:
        1. Determines whether the new class is a base class or a subclass, adding an `is_base_class` attribute
        accordingly.
        2. Modifies the names of attributes starting with a single underscore (`_`) by prefixing them with `encrypt`
        to simulate "encryption" of private attributes.
        3. Leaves attributes that begin with double underscores (`__`) unchanged to preserve dunder method behavior.
        4. Automatically registers the newly created class in the `inheritance` dictionary under its class name.

        Parameters:
        - cls (Type["metaclarsion"]): The metaclass used to create the new class.
        - class_name (str): The name of the class being created.
        - bases (tuple[type, ...]): A tuple of the base classes from which the new class inherits.
        - attrs (dict[str, Any]): A dictionary containing the attributes and methods of the class being created.

        Returns:
        - Type: The newly created class, which may have modified attribute names and other adjustments based on its
        status as a base class or subclass.

        Side Effects:
        - Modifies the `attrs` dictionary by "encrypting" attributes starting with a single underscore.
        - Adds a `is_base_class` attribute to distinguish between base and subclass types.
        - Registers the new class in the `inheritance` dictionary using the class name as the key.

        Notes:
        - This method is useful for enforcing certain conventions regarding private attributes and class structures,
        such as dynamically adjusting attribute names and ensuring proper inheritance tracking.
        - The attribute "encryption" (prefixing underscores) is a soft enforcement and does not actually secure the
        attributes; it only modifies their names for aesthetic or organizational purposes.
        """
        modified_attrs: dict[str, Any] = {}
        # attributes that are saved for dunder methods registry purpose
        if not bases or bases == (object,):
            modified_attrs["is_base_class"] = True
        else:
            modified_attrs["is_base_class"] = False

        for key, value in attrs.items():
            if key.startswith("__"):
                modified_attrs[key] = value
            elif key.startswith("_"):  # encrypt private methods.
                key: str = "encrypt" + key
                modified_attrs[key] = value
            else:
                modified_attrs[key] = value

        new_class: metaclarion = super().__new__(cls, class_name, bases, modified_attrs)
        cls.inheritance[class_name] = new_class  # auto-registry
        return new_class

    def __init__(
        cls, class_name: str, bases: tuple[type, ...], attrs: dict[str, Any]
    ) -> None:
        """
        Initialize the metaclass and define essential methods for the new class.

        This method is called after the class has been created by the `__new__` method. It performs the following:
        1. Checks if the `__init__` method is defined in the class being created; if not, it defines a default `__init__` method.
        2. Adds `static_display` and `dynamic_display` methods for debugging purposes if they are not already defined.
        3. The `static_display` method prints the class's name, its base classes, and its attributes in a static format.
        4. The `dynamic_display` method prints the class's name, base classes, and instance methods in a dynamic format, showing instance-specific information.

        Parameters:
        - cls (Type["metaclarsion"]): The metaclass being used to create the new class.
        - class_name (str): The name of the class being created.
        - bases (tuple[type, ...]): A tuple of base classes from which the new class inherits.
        - attrs (dict[str, Any]): A dictionary of the attributes and methods defined in the new class.

        Returns:
        - None: This method does not return anything; it modifies the `cls` object in place by adding or modifying methods.

        Side Effects:
        - Defines a default `__init__` method if the class does not already define one.
        - Adds `static_display` and `dynamic_display` methods to the class if they are not already defined.
        - Modifies the class's `__init__`, `static_display`, and `dynamic_display` attributes as needed.

        Notes:
        - The `__init__` method is essential for ensuring that the newly created class has basic functionality, especially when dynamic object-oriented programming is enabled.
        - The `static_display` and `dynamic_display` methods are primarily for debugging and display class and instance-level information in different formats.
        - This method is crucial for classes created with this metaclass to be fully functional in terms of OOP (Object-Oriented Programming).
        """
        # this __init__ is crucial for fully-functioning OOP
        if "__init__" not in attrs:

            def init(self, *args, **kwargs) -> None:
                pass

            cls.__init__ = init  # type: ignore

        # debug methods
        if "static_display" not in attrs:

            def static_display() -> NoReturn:
                txt = Text("\nStatic Display: >>>>>\n")
                txt.stylize("rgb(255,0,0)")
                rt(txt)
                print(
                    "-------------------------------------------------------------------------"
                )
                print("Display Class Detail: ")
                print(f"Class name: {class_name}")
                print(f"{class_name} inherit from class: {bases}")
                pt(f"Class Attributes: {attrs}")
                terminate()

            cls.static_display: Callable = staticmethod(static_display)

        if "dynamic_display" not in attrs:

            def dynamic_display(self) -> NoReturn:
                txt = Text("\nTraceback: >>>>>\n")
                txt.stylize("rgb(255,0,0)")
                rt(txt)
                print(
                    "-------------------------------------------------------------------------"
                )
                print("Display Class Detail: ")
                print(f"Class name: {class_name}")
                print(f"{class_name} inherit from class: {bases}")
                pt(f"Class has attributes {attrs}")
                instance_attribute: list[str] = [
                    x
                    for x in dir(self)
                    if not x.startswith("__") and callable(getattr(self, x))
                ]
                pt(f"Instance attributes: {instance_attribute}")
                terminate()

            cls.dynamic_display: Callable = dynamic_display

        return super().__init__(class_name, bases, attrs)

    def __call__(cls, *args, **kwargs) -> Any:
        """
        Handles the instantiation of a class created with the `public` metaclass, enabling dynamic method assignments,
        attribute setting, and management of default dunder methods.

        This method is invoked when an instance of a class using the `public` metaclass is created. It extends the standard
        behavior by dynamically assigning methods and attributes, while also handling custom implementations for methods like
        `__str__` and `__copy__`. It is designed to offer flexibility and extensibility for dynamically created classes.

        Key Features:
        1. **Dynamic Initialization**:
            - Calls the class's `__init__` method while handling dynamic assignments of positional and keyword arguments.
        2. **Dynamic Method Assignment**:
            - Supports the assignment of functions, including lambda functions, to class instances. If lambda functions are
            detected, they are assigned unique names to prevent conflicts.
        3. **Default Dunder Method Management**:
            - If the class does not define its own `__str__` method, a default implementation is generated based on a
            'name' attribute or the first string value found in the provided keyword arguments.
            - If the class does not have a custom `__copy__` method, a deep copy implementation is automatically added,
            supporting both shallow and deep copy operations.
        4. **Dynamic Attribute Assignment**:
            - Automatically sets attributes for the class or instance based on the provided keyword arguments. Special handling
            is applied for dictionary-type attributes to expand them into individual instance attributes.

        Parameters:
        - `cls` (Type["public"]): The metaclass being invoked.
        - `*args` (tuple): Positional arguments passed during instantiation, which may include callable functions or
        attributes.
        - `**kwargs` (dict[str, Any]): Keyword arguments used to set instance attributes, methods, or configurations.

        Returns:
        - `Any`: An instance of the dynamically created class, with the assigned methods, attributes, and custom dunder methods.

        Side Effects:
        - Modifies the `__str__` method if the class uses the default or inherited implementation.
        - Adds a `__copy__` method if not already defined to enable both shallow and deep copying.
        - Assigns functions (including lambda functions) dynamically to the class with unique names if needed.
        - Expands dictionary-type keyword arguments into separate instance attributes. ("key" must be "dict")
        - Handles logging for method assignments and unexpected arguments.

        Example:
        ```python
        >>> class Example(metaclass = metaclarion):
        >>>    ...

        >>> def method(self):
        >>>    print("Hello, world!")

        >>> instance = Example(method, name="example", dict={"key": "value"})
        >>> print(instance)  # Outputs: example
        >>> instance.method()  # Outputs: Hello, world!
        >>> print(instance.key) # Outputs: value
        ```

        Notes:
        - If no suitable value is found for the `__str__` method, a default message is used for the `__str__` method.
        - Lambda functions are assigned unique names prefixed with "la_func_" to avoid naming conflicts.
        - Classes can dynamically gain attributes like `class_list`, `class_dictionary`, etc., based on the types of input arguments.
        - Unexpected input types are ignored with a warning, allowing for flexible but controlled behavior.
        """
        instance: Any = super().__call__(*args, **kwargs)
        init_method: Callable = cls.__init__
        init_signature: inspect.Signature = inspect.signature(init_method)
        self_parameter: list[str] = list(init_signature.parameters.keys())[1:]
        # logging.critical(self_parameter) # <--- activate this line if any bug raises.
        pioneer_value: Any = kwargs.get("name")
        if pioneer_value == None:
            for values in kwargs.values():
                if isinstance(values, str):
                    pioneer_value = values
                    break
        elif pioneer_value == None:
            pioneer_value = "Undefined pioneer, please manually implement __str__."

        if (
            cls.__str__ is object.__str__
            or cls.__str__ is cls.__PARENT_CLASS_REPRESENTATION
        ):
            # if the class use default __str__ , registry needed.
            # if the class inherit from parent class's str, registry needed.
            def __str__(self) -> str:
                return str(pioneer_value)

            # only possible value for parent class's representation
            if getattr(cls, "is_base_class"):
                cls.__PARENT_CLASS_REPRESENTATION: Callable = __str__

            cls.__str__ = __str__  # type: ignore

        # check whether the class has a __copy__ , logic similar to __repr__.
        if not hasattr(cls, "__copy__") or cls.__copy__ is cls.__PARENT_CLASS_DEEPCOPY:

            def __copy__(self):
                return deepcopy(self)

            if getattr(cls, "is_base_class"):
                cls.__PARENT_CLASS_DEEPCOPY: Callable = __copy__

            cls.__copy__: Callable = __copy__  # type: ignore

        # dynamic setting attribute, allowing dictionary input
        lambda_function_index: int = 0
        value_index: int = 0
        for key, value in kwargs.items():
            if key == "dict":
                for names, attributes in value.items():
                    setattr(instance, str(names), attributes)
                continue

            setattr(instance, str(key), value)
        for values in args:
            if value_index < len(self_parameter) - 2:  # *args, **kwargs
                value_index += 1
                continue

            elif callable(values):
                # This is a function, set its name into function name(use slice [])
                # If function passed is an anonymous function (lambda), set its name into la_(lambda) + func_n
                function_name: str = str(values).split(" ")[
                    1
                ]  # split the function name by space, and take the second segment
                if (
                    re.search(r"[^a-zA-Z0-9_]", function_name)
                    or function_name[0].isdigit()
                    or function_name[0] == "_"
                ):
                    if function_name != "<lambda>":
                        raise TypeError(
                            f"Invalid function name {function_name}, must be a regular expression."
                        )
                    else:
                        lambda_function_index += 1
                        function_name = "la" + "_func_" + str(lambda_function_index)
                        logging.warning(
                            f"Lambda function {function_name} only exist in this instance."
                        )
                setattr(cls, str(function_name), values)
                logging.info(f"Set function {str(values)} to class as {function_name}")

            # class + type enable for tuple, list, dictionary, set, panda dataframe and native circulis(t)
            elif type(values).__name__ in cls.name_dict.keys():
                setattr(cls, cls.name_dict[type(values).__name__], values)
            # other type of input will be ignored
            else:
                logging.warning(
                    f"Ignore the unexpected argument {values}, with type {type(values).__name__}"
                )
                continue

        return instance

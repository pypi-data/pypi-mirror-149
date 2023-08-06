from dataclasses import dataclass
from typing import Callable, Generic, Iterator, Optional, TypeVar, Union

# Generic types
T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")


@dataclass
class Result(Generic[T, E]):
    value: Union[T, E]

    def is_ok(self) -> bool:
        """
        Returns true if the result is Ok.
        """
        raise NotImplementedError

    def is_err(self) -> bool:
        """
        Returns true if the result is Err.
        """
        raise NotImplementedError

    def ok(self) -> Optional[T]:
        """
        Converts from Result[T, E] to Optional[T].

        Converts self into an Optional[T], consuming self, and discarding the error, if any.
        """
        raise NotImplementedError

    def err(self) -> Optional[E]:
        """
        Converts from Result[T, E] to Optional[E]

        Converts self into an Optional[E], consuming self, and discarding the success value, if any.
        """
        raise NotImplementedError

    def map(self, op: Callable[[T], U]) -> "Result[U, E]":
        """
        Maps a Result[T, E] to Result[U, E] by applying a function to a contained Ok value, leaving an Err value untouched.

        This function can be used to compose the results of two functions.
        """
        raise NotImplementedError

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        Returns the provided default (if Err), or applies a function to the contained value (if Ok),

        Arguments passed to map_or are eagerly evaluated; if you are passing the result of a function call, it is recommended to use map_or_else, which is lazily evaluated.
        """
        raise NotImplementedError

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        """
        Maps a Result[T, E] to U by applying fallback function default to a contained Err value, or function f to a contained Ok value.

        This function can be used to unpack a successful result while handling an error.
        """
        raise NotImplementedError

    def map_err(self, op: Callable[[E], F]) -> "Result[T, F]":
        """
        Maps a Result[T, E] to Result[T, F] by applying a function to a contained Err value, leaving an Ok value untouched.
        """
        raise NotImplementedError

    def iter(self) -> Iterator[Optional[T]]:
        """
        Returns an iterator over the possibly contained value.

        The iterator yields one value if the result is Ok, otherwise none.
        """
        raise NotImplementedError

    def expect(self, msg: str) -> T:
        """
        Returns the contained Ok value, consuming the self value.

        Raises:
            RuntimeError: If the value is an Err, with an error message including the passed message, and the content of the Err.
        """
        raise NotImplementedError

    def unwrap(self) -> T:
        """
        Returns the contained Ok value, consuming the self value.

        Because this function may raise a RuntimeError, its use is generally discouraged. Instead, prefer to use pattern matching and handle the Err case explicitly, or call unwrap_or, unwrap_or_else, or unwrap_or_default.

        Raises:
            RuntimeError: If the value is an Err, with an error message provided by the Err’s value.
        """
        raise NotImplementedError

    def unwrap_or_default(self) -> T:
        """
        Returns the contained Ok value or a default.

        Consumes the self argument then, if Ok, returns the contained value, otherwise if Err, returns the default value for that type.
        """
        raise NotImplementedError

    def expect_err(self, msg: str) -> E:
        """
        Returns the contained Err value, consuming the self value.

        Raises:
            RuntimeError: If the value is an Ok, with an error message including the passed message, and the content of the Ok.
        """
        raise NotImplementedError

    def unwrap_err(self) -> E:
        """
        Returns the contained Err value, consuming the self value.

        Raises:
            RuntimeError: Panics if the value is an Ok, with a custom error message provided by the Ok’s value.
        """
        raise NotImplementedError

    def re_and(self, res: "Result[U, E]") -> "Result[U, E]":
        """
        Returns res if the result is Ok, otherwise returns the Err value of self.

        I would have called this `and` if it weren't already a keyword...
        """
        raise NotImplementedError

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """
        Calls op if the result is Ok, otherwise returns the Err value of self.

        This function can be used for control flow based on Result values.
        """
        raise NotImplementedError

    def re_or(self, res: "Result[T, F]") -> "Result[T, F]":
        """
        Returns res if the result is Err, otherwise returns the Ok value of self.

        Arguments passed to or are eagerly evaluated; if you are passing the result of a function call, it is recommended to use or_else, which is lazily evaluated.

        I would have called this `or` if it weren't already a keyword...
        """
        raise NotImplementedError

    def or_else(self, op: Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        """
        Calls op if the result is Err, otherwise returns the Ok value of self.

        This function can be used for control flow based on result values.
        """
        raise NotImplementedError

    def unwrap_or(self, default: T) -> T:
        """
        Returns the contained Ok value or a provided default.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the result of a function call, it is recommended to use unwrap_or_else, which is lazily evaluated.
        """
        raise NotImplementedError

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        """
        Returns the contained Ok value or computes it from a closure.
        """
        raise NotImplementedError


@dataclass
class Ok(Result):
    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> Optional[T]:
        return self.value

    def err(self) -> Optional[E]:
        return None

    def map(self, op: Callable[[T], U]) -> "Result[U, E]":
        # @TODO: Figure out how to handle this mapping of types
        return Ok(op(self.value))  # type: ignore

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.value)

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return f(self.value)

    def map_err(self, op: Callable[[E], F]) -> "Result[T, F]":
        return self

    def iter(self) -> Iterator[Optional[T]]:
        yield self.value

    def expect(self, msg: str) -> T:
        return self.value

    def unwrap(self) -> T:
        return self.value

    def unwrap_or_default(self) -> T:
        return self.value

    def expect_err(self, msg: str) -> E:
        raise RuntimeError(f"{msg}: {self.value}")

    def unwrap_err(self) -> E:
        raise RuntimeError(f"{self.value}")

    def re_and(self, res: "Result[U, E]") -> "Result[U, E]":
        if res.is_err():
            return res
        return res

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return op(self.value)

    def re_or(self, res: "Result[T, F]") -> "Result[T, F]":
        return self

    def or_else(self, op: Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        return self

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self.value


@dataclass
class Err(Result):
    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> Optional[T]:
        return None

    def err(self) -> Optional[E]:
        return self.value

    def map(self, op: Callable[[T], U]) -> "Result[U, E]":
        return self

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return default(self.value)

    def map_err(self, op: Callable[[E], F]) -> "Result[T, F]":
        # @TODO: Figure out how to handle this mapping of types
        return Err(op(self.value))  # type: ignore

    def iter(self) -> Iterator[Optional[T]]:
        yield None

    def expect(self, msg: str) -> T:
        raise RuntimeError(f"{msg}: {self.value}")

    def unwrap(self) -> T:
        raise RuntimeError(self.value)

    def unwrap_or_default(self) -> T:
        c = self.value.__class__
        try:
            return c()
        except:
            raise RuntimeError(f"Cannot provide default value for: {c}")

    def expect_err(self, msg: str) -> E:
        return self.value

    def unwrap_err(self) -> E:
        return self.value

    def re_and(self, res: "Result[U, E]") -> "Result[U, E]":
        return self

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return self

    def re_or(self, res: "Result[T, F]") -> "Result[T, F]":
        return res

    def or_else(self, op: Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        return op(self.value)

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self.value)

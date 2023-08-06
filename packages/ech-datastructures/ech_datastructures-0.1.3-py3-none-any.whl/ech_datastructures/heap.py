import heapq
from typing import Any, Callable, Generic, Iterable, TypeVar, List


T = TypeVar("T")


class _HeapElem(Generic[T]):
    """
    Helper class for Heap.
    Stores a single value in a way that lets us use the `heapq` package.
    """
    __slots__ = "val", "key", "reverse"

    def __init__(self,
                 val: T,
                 *,
                 key: Callable[[T], Any],
                 reverse: bool):
        """
        Construct a _HeapElem.
        """
        self.val = val
        self.key = key
        self.reverse = reverse

    def __lt__(self, other: "_HeapElem[T]") -> bool:
        """
        Comparison function used by heapq to do sorting
        Returning `True` means `self` comes before `other`.
        """
        natural = self.key(self.val) < self.key(other.val)
        if self.reverse:
            return not natural
        return natural


class Heap(Generic[T]):
    """
    MinHeap or MaxHeap, however you'd like.
    AKA Priority Queue.

    Allows duplicate / equivalent values.

    Elements are not stored in fully sorted order, but as they are retrieved using
    `pop`, they come out sorted.

    `T` represents the type of items being stored in the Heap.
    """
    __slots__ = "_data", "_key", "_reverse"

    def __init__(self,
                 data: Iterable[T] = None,
                 *,
                 key: Callable[[T], Any] = None,
                 reverse: bool = False):
        """
        Construct a Heap.

        Parameters
        ----------
        data: Iterable[T] (optional) - initial values for the Heap to store.
            If `None` (default), the Heap starts with no contents.
        key: Callable[(T) -> Any] - function to determine an element's ordering value.
            Returned values are compared using the "less-than" operator: `key(e1) < key(e2)`.
            If `None` (default), the elements are compared directly.
        reverse: bool - if "high" values should be greater priority in the Heap.
            If `False` (default), elements with lower key values are at the top of the Heap.
            If `True`, elements with higher key values are at the top of the Heap.
        """
        # save provided sorting key, if any
        if key is None:
            self._key = lambda x: x
        else:
            self._key = key
        self._reverse = reverse
        # save provided data, if any
        if data is None:
            self._data = []
        else:
            self._data = [_HeapElem(x, key=self._key, reverse=self._reverse) for x in data]
            heapq.heapify(self._data)

    @property
    def data(self) -> List[T]:
        """
        Get a view of the contents of the Heap. This view represents the raw backing array.
        See more: https://docs.python.org/3/library/heapq.html

        Returns
        -------
        List[T] - simple view of the contents of the Heap.
        """
        return [elem.val for elem in self._data]

    def peek(self) -> T:
        """
        Return the next item from the Heap but leave the Heap unchanged.

        Returns
        -------
        T - next item (still in the Heap).

        Raises
        ------
        IndexError - Heap was empty at the start of the operation; nothing to peek.
        """
        try:
            return self._data[0].val
        except IndexError as e:
            raise IndexError("peek from empty Heap") from e

    def pop(self) -> T:
        """
        Remove the next item from the Heap and return it.

        Returns
        -------
        T - next item (no longer in the Heap).

        Raises
        ------
        IndexError - Heap was empty at the start of the operation; nothing to pop.
        """
        try:
            return heapq.heappop(self._data).val
        except IndexError as e:
            raise IndexError("pop from empty Heap") from e

    def add(self, new_item: T):
        """
        Add a new item to the Heap.

        Parameters
        ----------
        new_item: T - new item to add to the Heap.

        Returns
        -------
        None
        """
        heapq.heappush(self._data, _HeapElem(new_item, key=self._key, reverse=self._reverse))

    def add_pop(self, new_item: T) -> T:
        """
        Add a new item, then pop the next item, and return the popped item.
        More efficient than independent calls to `add` then `pop`.

        Parameters
        ----------
        new_item: T - new item to add to the Heap.

        Returns
        -------
        T - popped item.
        """
        return heapq.heappushpop(
            self._data,
            _HeapElem(new_item, key=self._key, reverse=self._reverse)
        ).val

    def pop_add(self, new_item: T) -> T:
        """
        Pop the next item, then add a new item, and return the popped item.
        More efficient than independent calls to `pop` then `add`.

        Parameters
        ----------
        new_item: T - new item to add to the Heap.

        Returns
        -------
        T - popped item.

        Raises
        ------
        IndexError - Heap was empty at the start of the operation; nothing to pop.
        """
        try:
            return heapq.heapreplace(
                self._data,
                _HeapElem(new_item, key=self._key, reverse=self._reverse)
            ).val
        except IndexError as e:
            raise IndexError("pop_add from empty Heap") from e

    def update(self, new_items: Iterable[T]):
        """
        Add multiple items to the Heap by calling `Heap.add` for each.

        Parameters
        ----------
        new_items: Iterable[T] - items to add to the Heap.

        Returns
        -------
        None
        """
        for item in new_items:
            self.add(item)

    def __len__(self) -> int:
        """
        Check the number of elements in the Heap.

        Returns
        -------
        int - number of elements in the Heap.
        """
        return len(self._data)

    def is_empty(self) -> bool:
        """
        Check if the Heap is empty or not.

        Returns
        -------
        bool - `True` if there is no data in the Heap, `False` otherwise.
        """
        return self.__len__() == 0

    def clear(self):
        """
        Empty all data from the Heap.

        Returns
        -------
        None
        """
        self._data.clear()

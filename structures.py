from typing import Any, Optional, Union


class DoublyLinkedListNodeError(Exception):
    """

    Args:
        Exception (_type_): _description_
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DoublyLinkedList:

    class __Node:
        def __init__(
            self,
            data: Union[Any, None],
            prev=None,
            next=None,
        ) -> None:
            self.data = data
            self.prev = prev
            self.next = next

        def __str__(self) -> str:
            if self.data is None:
                return ""
            if not self.next:
                return f"{self.data}"
            return f"{self.data}"

        def __repr__(self) -> str:
            return self.__str__()

    def __init__(self, data: Union[list[Any], None] = None) -> None:
        self.__tail: Optional[self.__Node] = None
        self.__head: Optional[self.__Node] = None
        if data is None or (isinstance(data, list) and len(data) == 0):
            self._len = 0
            return
        self._len = len(data)
        if len(data) >= 1:
            node = self.__Node(data[0])
            self.__head = node
            self.__tail = node
            node = self.__head
            for i in range(1, len(data)):
                node.next = self.__Node(data[i], prev=node)
                node = node.next
                self.__tail = node

    def __str__(self) -> str:
        if self.__head is None:
            return "DoublyLinkedList([])"
        values = []
        node: self.__Node | None = self.__head
        while node is not None:
            values.append(str(node.data))
            node = node.next
        return f"DoublyLinkedList([{', '.join(values)}])"

    def __len__(self) -> int:
        return self._len

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, index: int) -> Any:
        return self.__get_node(index).data

    def __get_node(self, index: int) -> __Node:
        assert isinstance(index, int), "Index must be an integer"
        if self._len == 0 or index > self._len - 1 or index < -1:
            raise IndexError("Index out of range")
        if self.__head is None or self.__tail is None:
            raise IndexError("__head or _tail is None, fix the code")
        if index == 0:
            return self.__head
        if index == -1 or index == self._len - 1:
            return self.__tail
        if index < len(self) // 2:
            i = 0
            node = self.__head
            while i < index:
                if node.next is None:
                    raise DoublyLinkedListNodeError("Node is None")
                node = node.next
                i += 1
            return node
        i = len(self) - 1
        node = self.__tail
        while index < i:
            if node.prev is None:
                raise DoublyLinkedListNodeError("Node is None")
            node = node.prev
            i -= 1
        return node

    def __setitem__(self, index: int, value: Any) -> None:
        assert isinstance(index, int), "Index must be an integer"
        if value is None:
            raise ValueError("Value cannot be None")
        if index > self._len - 1:
            raise IndexError("Index out of range")
        if isinstance(value, self.__Node):
            self.__get_node(index).data = value.data
        else:
            self.__get_node(index).data = value
        return

    def remove(self, index: Optional[int] = None, value: Optional[Any] = None) -> None:
        assert (index is not None) + (
            value is not None
        ) == 1, "Index and value cannot be None at the same time"
        if value is not None:
            del self[self.index(value)]
            return
        del self[index]
        return

    def __delitem__(self, index) -> None:
        assert isinstance(index, int), "Index must be an integer"
        if index > self._len - 1:
            raise IndexError("Index out of range")
        old_tail = self.__tail
        old__head = self.__head
        if self._len == 1:
            self.__head = None
            self.__tail = None
            del old_tail
            del old__head
            self._len -= 1
            return
        if index == 0 and self.__head is not None:
            self.__head = self.__head.next
            del old__head
            self._len -= 1
            return
        if (index in (-1, self._len - 1)) and self.__tail is not None:
            self.__tail = self.__tail.prev
            if self.__tail is None:
                raise DoublyLinkedListNodeError("__tail is None")
            self.__tail.next = None
            del old_tail
            self._len -= 1
            return
        del_node = self.__get_node(index)
        if del_node.next is None or del_node.prev is None:
            raise DoublyLinkedListNodeError("Node is None")
        del_node.prev.next = del_node.next
        del_node.next.prev = del_node.prev
        del del_node
        self._len -= 1
        return

    def index(self, value: Any) -> int:
        node = self.__head
        i = 0
        while node is not None:
            if node.data == value:
                return i
            node = node.next
            i += 1
        raise ValueError(f"{value} is not in list")

    def insert(self, index: int, value) -> None:
        assert isinstance(index, int), "Index must be an integer"
        if index > self._len or index < -1:
            raise IndexError("index out of range")
        if self._len == 0:
            node = self.__Node(value)
            self.__head = node
            self.__tail = node
        elif index == 0:
            if self.__head is None:
                raise DoublyLinkedListNodeError("__head is None")
            old__head = self.__head
            new_head = self.__Node(value, next=old__head)
            old__head.prev = new_head
            self.__head = new_head
        elif index == self._len or index == -1:
            if self.__tail is None:
                raise DoublyLinkedListNodeError("__tail is None")
            old_tail = self.__tail
            new_tail = self.__Node(value, prev=old_tail)
            old_tail.next = new_tail
            self.__tail = new_tail
        else:
            node = self.__get_node(index - 1)
            if node.next is None:
                raise DoublyLinkedListNodeError("node.next is None")
            next_node = node.next
            new_node = self.__Node(value, next=next_node, prev=node)
            node.next = new_node
            next_node.prev = node.next
        self._len += 1

    def add_left(self, value: Any):
        if value is None:
            raise ValueError("Value cannot be None")
        self.insert(0, value)

    def add_right(self, value: Any):
        if value is None:
            raise ValueError("Value cannot be None")
        self.insert(-1, value)

    def get_right(self):
        return self[-1]

    def get_left(self):
        return self[0]

    def pop_left(self) -> Optional[Any]:
        if self._len == 0:
            raise IndexError("List is empty")
        if self.__head is None:
            raise IndexError("__head is None")
        head_data = self.__head.data
        del self[0]
        return head_data

    def pop_right(self) -> Optional[Any]:
        if self._len == 0 and self.__head is None and self.__tail is None:
            raise IndexError("List is empty")
        if self.__tail is None:
            raise IndexError("Tail is None")
        tail_data = self.__tail.data
        del self[-1]
        return tail_data

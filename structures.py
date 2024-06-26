from typing import Any, Optional, Union


class Linked:
    class _Node:
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
        self._tail: Optional[self._Node] = None
        self._head: Optional[self._Node] = None
        if data is None or (isinstance(data, list) and len(data) == 0):
            self._len = 0
            return
        self._len = len(data)
        if len(data) >= 1:
            node = self._Node(data[0])
            self._head = node
            self._tail = node
            node = self._head
            for i in range(1, len(data)):
                node.next = self._Node(data[i], prev=node)
                node = node.next
                self._tail = node

    def __len__(self) -> int:
        return self._len

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, index: int) -> Any:
        return self.__get_node(index).data

    def __get_node(self, index: int) -> _Node:
        assert isinstance(index, int), "Index must be an integer"
        if self._len == 0 or index > self._len - 1 or index < -1:
            raise IndexError("Index out of range")
        if self._head is None or self._tail is None:
            raise IndexError("_head or _tail is None, fix the code")
        if index == 0:
            return self._head
        if index == -1 or index == self._len - 1:
            return self._tail
        if index < len(self) // 2:
            i = 0
            node = self._head
            while i < index:
                if node.next is None:
                    raise ValueError("Node is None")
                node = node.next
                i += 1
            return node
        i = len(self) - 1
        node = self._tail
        while index < i:
            if node.prev is None:
                raise ValueError("Node is None")
            node = node.prev
            i -= 1
        return node

    def __setitem__(self, index: int, value: Any) -> None:
        assert isinstance(index, int), "Index must be an integer"
        if value is None:
            raise ValueError("Value cannot be None")
        if index > self._len - 1:
            raise IndexError("Index out of range")
        if isinstance(value, self._Node):
            self.__get_node(index).data = value.data
        else:
            self.__get_node(index).data = value
        return

    def __delitem__(self, index) -> None:
        assert isinstance(index, int), "Index must be an integer"
        if index > self._len - 1:
            raise IndexError("Index out of range")
        old_tail = self._tail
        _head = self._head
        if self._len == 1:
            self._head = None
            self._tail = None
            del old_tail
            del _head
            self._len -= 1
            return
        if index == 0 and self._head is not None:
            self._head = self._head.next
            del _head
            self._len -= 1
            return
        if (index in (-1, self._len - 1)) and self._tail is not None:
            self._tail = self._tail.prev
            if self._tail is None:
                raise ValueError("_tail is None")
            self._tail.next = None
            del old_tail
            self._len -= 1
            return
        del_node = self.__get_node(index)
        if del_node.next is None or del_node.prev is None:
            raise ValueError("Node is None")
        del_node.prev.next = del_node.next
        del_node.next.prev = del_node.prev
        del del_node
        self._len -= 1
        return


class DoublyLinkedList(Linked):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        if self._head is None:
            return "DoublyLinkedList([])"
        values = []
        node: self._Node = self._head
        while node is not None:
            values.append(str(node.data))
            node = node.next
        return f"DoublyLinkedList([{', '.join(values)}])"

    def remove(self, index: Optional[int] = None, value: Optional[Any] = None) -> None:
        assert (index is not None) + (
            value is not None
        ) == 1, "Index and value cannot be None at the same time"
        if value is not None:
            del self[self.index(value)]
            return
        del self[index]
        return

    def index(self, value: Any) -> int:
        node = self._head
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
            node = self._Node(value)
            self._head = node
            self._tail = node
        elif index == 0:
            if self._head is None:
                raise ValueError("_head is None")
            _head = self._head
            new_head = self._Node(value, next=_head)
            _head.prev = new_head
            self._head = new_head
        elif index == self._len or index == -1:
            if self._tail is None:
                raise ValueError("_tail is None")
            old_tail = self._tail
            new_tail = self._Node(value, prev=old_tail)
            old_tail.next = new_tail
            self._tail = new_tail
        else:
            node = self.__get_node(index - 1)
            if node.next is None:
                raise ValueError("node.next is None")
            next_node = node.next
            new_node = self._Node(value, next=next_node, prev=node)
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
        if self._head is None:
            raise IndexError("_head is None")
        head_data = self._head.data
        del self[0]
        return head_data

    def pop_right(self) -> Optional[Any]:
        if self._len == 0 and self._head is None and self._tail is None:
            raise IndexError("List is empty")
        if self._tail is None:
            raise IndexError("Tail is None")
        tail_data = self._tail.data
        del self[-1]
        return tail_data


class Queue(Linked):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        if self._head is None:
            return "Queue([])"
        values = []
        node: self._Node = self._head
        while node is not None:
            values.append(str(node.data))
            node = node.next
        return f"Queue([{', '.join(values)}])"

    def enqueue(self, value: Any) -> None:
        if self._len == 0:
            new_node = self._Node(value)
            self._head = new_node
            self._tail = new_node
            self._len += 1
            return
        if self._tail is None:
            raise ValueError("Tail is None")
        old_tail = self._tail
        new_node = self._Node(value, prev=old_tail)
        old_tail.next = new_node
        self._tail = new_node
        self._len += 1
        return

    def dequeue(self) -> Any:
        if self._len == 0:
            raise IndexError("Queue is empty")
        if self._head is None:
            raise ValueError("Head is None")
        old_head = self._head
        head_value = old_head.data
        if self._len == 1:
            self._head = None
            self._tail = None
            self._len -= 1
            return head_value
        self._head = self._head.next
        self._head.prev = None
        self._len -= 1
        return head_value

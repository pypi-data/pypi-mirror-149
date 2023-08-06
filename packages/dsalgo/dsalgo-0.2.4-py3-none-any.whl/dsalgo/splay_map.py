from __future__ import annotations

import dataclasses
import sys
import typing
from typing import Optional

sys.setrecursionlimit(1 << 20)


T = typing.TypeVar("T")
V = typing.TypeVar("V")


@dataclasses.dataclass
class Node(typing.Generic[T, V]):
    key: T
    left: Optional[Node] = None
    right: Optional[Node] = None
    value: Optional[V] = None


T = typing.TypeVar("T")
V = typing.TypeVar("V")


@dataclasses.dataclass
class SplayTreeMap(typing.Generic[T, V]):
    root: typing.Optional[Node[T, V]] = None

    def rotate(self) -> None:
        u = self.root
        if self.__key < u.key:
            v = u.left
            u.left = v.right
            v.right = u
        else:
            v = u.right
            u.right = v.left
            v.left = u
        self.root = v

    def splay(self, key: T) -> None:
        self.__key = key
        us = self.__state()
        if not us:
            return
        u = self.root
        v = u.left if us < 0 else u.right
        self.root = v
        vs = self.__state()
        if not vs:
            self.root = u
            self.rotate()
            return
        self.root = v.left if vs < 0 else v.right
        self.splay(key)
        if vs < 0:
            v.left = self.root
        else:
            v.right = self.root
        if us == vs:
            self.root = u
            self.rotate()
        else:
            self.root = v
            self.rotate()
            if us < 0:
                u.left = self.root
            else:
                u.right = self.root
            self.root = u
        self.rotate()

    def __state(self) -> int:
        u = self.root
        if not u:
            return 0
        k = self.__key
        if k == u.key:
            return 0
        if k < u.key:
            return -1 + 1 * (not u.left)
        return 1 - 1 * (not u.right)

    def __getitem__(self, key: T) -> V:
        self.splay(key)
        return self.root.value

    def __setitem__(self, key: T, v: V) -> None:
        self.splay(key)
        self.root.value = v

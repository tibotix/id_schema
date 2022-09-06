from typing import *
import sys
from .components.base_component import BaseComponent



class IDSchema():
    Components: List[BaseComponent] = list()

    @classmethod
    def generate_n(cls, n: int) -> List[str]:
        return [cls.generate_one() for _ in range(n)]
        
    @classmethod
    def generate_n_unique(cls, n: int, max_retry: int = 20) -> List[str]:
        ids: List[str] = list()
        while len(ids) < n:
            new_id = cls.generate_one()
            if new_id in ids:
                max_retry -= 1
                if max_retry == 0:
                    raise RuntimeError(f"Max Retry exceeded trying to generate {n!s} unique ids.")
                continue
            ids.append(new_id)
        return ids

    @classmethod
    def generate_one(cls) -> str:
        id_ = ""
        for component in cls.Components:
            id_ += component.generate()
        return id_

    @classmethod
    def validate(cls, id_ : str, max_reductions: int = 5000, iterative=True) -> bool:
        if len(cls.Components) == 1:
            return cls.Components[0].validate(id_)
        if not iterative and (rec_limit := sys.getrecursionlimit()) <= len(cls.Components):
            raise ValueError(f"Number of Components must be smaller than recursion limit ({rec_limit!s})")
        if iterative:
            return cls._validate_iterative(id_, max_reductions=max_reductions)
        return cls._validate_recursive(id_, max_reductions=max_reductions)[0]

    @classmethod
    def _validate_recursive(cls, id_ : str, cur_idx: int = 0, max_reductions: int = 5000) -> bool:
        if max_reductions == 0:
            raise RuntimeError("Max Reductions reached! (DoS protection)")
        if cur_idx == len(cls.Components):
            return id_ == "", max_reductions
        sub_ids = cls.Components[cur_idx].reduce_all_matching(id_)
        for sub_id in sub_ids:
            success, max_reductions = cls._validate_recursive(sub_id, cur_idx+1, max_reductions-1)
            if success:
                return True, max_reductions
        return False, max_reductions

    @classmethod
    def _validate_iterative(cls, id_ : str, cur_idx: int = 0, max_reductions: int = 5000) -> bool:
        stack = list((iter((id_, )),))
        sub_ids = stack[cur_idx]
        while True:
            next_id = next(sub_ids, None)
            if (max_reductions := max_reductions-1) == 0:
                raise RuntimeError("Max Reductions reached! (DoS protection)")
            if next_id is None:
                #last sub_id
                if cur_idx == 0:
                    return False
                stack.pop()
                cur_idx -= 1
                sub_ids = stack[cur_idx]
                continue
            if cur_idx == len(cls.Components):
                # last component
                if next_id == "":
                    return True
                continue

            sub_ids = cls.Components[cur_idx].reduce_all_matching(next_id)
            stack.append(sub_ids)
            cur_idx += 1
from __future__ import annotations
#  * Copyright (c) 2021 Push Technology Ltd., All Rights Reserved.
#  *
#  * Use is subject to license terms.
#  *
#  * NOTICE: All information contained herein is, and remains the
#  * property of Push Technology. The intellectual and technical
#  * concepts contained herein are proprietary to Push Technology and
#  * may be covered by U.S. and Foreign Patents, patents in process, and
#  * are protected by trade secret or copyright law.
import copy
import typing

from diffusion.features.control.session_trees.branch_mapping import BranchMapping
import attr


@attr.s(frozen=True, auto_attribs=True, slots=True, hash=True, eq=True, repr=True)
class BranchMappingTable(object):
    """
    A session tree branch mapping table.

    A branch mapping table is a list of `BranchMapping` branch mappings
    assigned to a session tree branch.

    To create a branch mapping table, obtain a new a builder instance using
    BranchMappingTable.Builder, call
    Builder.add_branch_mapping for each branch mapping,
    then Builder.create. The result can then be sent to the
    server using SessionTrees.put_branch_mapping_table.

    Attributes:
        session_tree_branch: the branch of the session tree to which this table is bound
        branch_mappings: the branch mappings

    See Also: SessionTrees
    """
    session_tree_branch: str = attr.ib(validator=attr.validators.instance_of(str))
    branch_mappings: typing.List[BranchMapping]

    class Builder(object):
        def __init__(self):
            """
            Builder for BranchMappingTable instances.
            """
            self._mappings: typing.List[BranchMapping] = []

        def reset(self) -> BranchMappingTable.Builder:
            """
            Reset the builder

            Returns: self
            """
            self._mappings.clear()
            return self

        def add_branch_mapping(
            self, session_filter: str, target_path: str
        ) -> BranchMappingTable.Builder:
            """
            Add a new branch mapping.

            Args:
                session_filter: the session filter
                target_path: the target path

            Returns: self
            """
            self._mappings.append(BranchMapping(session_filter, target_path))
            return self

        def create(self, session_tree_branch: str) -> BranchMappingTable:
            """
            Create a new BranchMappingTable.

            Args:
                session_tree_branch: the session tree branch

            Returns: the table
            """
            return BranchMappingTable(session_tree_branch, copy.deepcopy(self._mappings))

    @classmethod
    def from_fields(cls, *, branch_mappings, **kwargs):
        result = cls(branch_mappings=[BranchMapping(*x) for x in branch_mappings], **kwargs)
        return result

    @classmethod
    def attr_mappings(cls) -> typing.Dict[str, typing.Any]:
        return {
            "branch-mapping-table.path": cls.session_tree_branch,
            "branch-mapping-table": cls.branch_mappings,
        }

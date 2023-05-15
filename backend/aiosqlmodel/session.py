from typing import (Any, Mapping, Optional, Sequence,
                    Type, TypeVar, Union, overload)

from sqlalchemy import util
from sqlalchemy.ext.asyncio import (
    AsyncConnection, AsyncEngine, AsyncSession as _AsyncSession)
from sqlmodel.engine.result import Result, ScalarResult
from sqlmodel.sql.base import Executable
from sqlmodel.sql.expression import Select, SelectOfScalar
from typing_extensions import Literal


_TSelectParam = TypeVar("_TSelectParam")


class AsyncSession(_AsyncSession):
    def __init__(
            self,
            bind: Optional[Union[AsyncConnection, AsyncEngine]] = ...,
            expire_on_commit: bool = ...,
            *args,
            **kwargs) -> None:
        super().__init__(bind, *args,
                         expire_on_commit=expire_on_commit, **kwargs)

    @overload
    async def exec(
        self,
        statement: Select[_TSelectParam],
        *,
        params: Optional[Union[Mapping[str, Any],
                               Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Result[_TSelectParam]:
        ...

    @overload
    async def exec(
        self,
        statement: SelectOfScalar[_TSelectParam],
        *,
        params: Optional[Union[Mapping[str, Any],
                               Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> ScalarResult[_TSelectParam]:
        ...

    async def exec(
        self,
        statement: Union[
            Select[_TSelectParam],
            SelectOfScalar[_TSelectParam],
            Executable[_TSelectParam],
        ],
        *,
        params: Optional[Union[Mapping[str, Any],
                               Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Union[Result[_TSelectParam], ScalarResult[_TSelectParam]]:
        try:
            results = await super().execute(
                statement,
                params=params,
                execution_options=execution_options,
                bind_arguments=bind_arguments,
                _parent_execute_state=_parent_execute_state,
                _add_event=_add_event,
                **kw,
            )
        except:
            return await self.execute(
                statement,
                params=params,
                execution_options=execution_options,
                bind_arguments=bind_arguments,
                _parent_execute_state=_parent_execute_state,
                _add_event=_add_event,
                **kw,
            )
        if isinstance(statement, SelectOfScalar):
            return results.scalars()  # type: ignore
        return results  # type: ignore

    async def get(
        self,
        entity: Type[_TSelectParam],
        ident: Any,
        options: Optional[Sequence[Any]] = None,
        populate_existing: bool = False,
        with_for_update: Optional[Union[Literal[True],
                                        Mapping[str, Any]]] = None,
        identity_token: Optional[Any] = None,
        execution_options: Optional[Mapping[Any, Any]] = util.EMPTY_DICT,
    ) -> Optional[_TSelectParam]:
        return await super().get(
            entity,
            ident,
            options=options,
            populate_existing=populate_existing,
            with_for_update=with_for_update,
            identity_token=identity_token,
            execution_options=execution_options,
        )

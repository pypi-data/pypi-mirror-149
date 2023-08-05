"""The module that defines the ``OAuthToken`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..utils import to_dict
from .oauth_provider import OAuthProvider


@dataclass
class OAuthToken:
    """An OAuth token."""

    #: The id of the token.
    id: "str"
    #: The provider of this token.
    provider: "OAuthProvider"
    #: The user id for this token.
    user_id: "int"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of the token.",
            ),
            rqa.RequiredArgument(
                "provider",
                parsers.ParserFor.make(OAuthProvider),
                doc="The provider of this token.",
            ),
            rqa.RequiredArgument(
                "user_id",
                rqa.SimpleValue.int,
                doc="The user id for this token.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "id": to_dict(self.id),
            "provider": to_dict(self.provider),
            "user_id": to_dict(self.user_id),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["OAuthToken"], d: t.Dict[str, t.Any]
    ) -> "OAuthToken":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            provider=parsed.provider,
            user_id=parsed.user_id,
        )
        res.raw_data = d
        return res

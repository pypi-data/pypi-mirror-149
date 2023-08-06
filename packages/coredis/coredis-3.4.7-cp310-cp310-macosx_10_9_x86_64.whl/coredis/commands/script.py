from __future__ import annotations

import hashlib

from coredis.exceptions import NoScriptError
from coredis.typing import Iterable, Optional, StringT, SupportsScript
from coredis.utils import b


class Script:
    """
    An executable Lua script object returned by :meth:`coredis.Redis.register_script`
    """

    def __init__(
        self,
        registered_client: SupportsScript,
        script: StringT,
    ):
        """
        :param script: The lua script that will be used by :meth:`execute`
        """
        self.registered_client = registered_client
        self.script = script
        self.sha = hashlib.sha1(b(script)).hexdigest()

    async def execute(
        self,
        keys: Optional[Iterable] = None,
        args: Optional[Iterable] = None,
        client: Optional[SupportsScript] = None,
    ):
        """
        Executes the script registered in :paramref:`Script.script`
        """
        from coredis.commands.pipeline import Pipeline

        if client is None:
            client = self.registered_client
        # make sure the Redis server knows about the script
        if isinstance(client, Pipeline):
            # make sure this script is good to go on pipeline
            client.scripts.add(self)

        try:
            return await client.evalsha(self.sha, keys=keys, args=args)
        except NoScriptError:
            # Maybe the client is pointed to a differnet server than the client
            # that created this instance?
            # Overwrite the sha just in case there was a discrepancy.
            self.sha = await client.script_load(self.script)
            return await client.evalsha(self.sha, keys=keys, args=args)

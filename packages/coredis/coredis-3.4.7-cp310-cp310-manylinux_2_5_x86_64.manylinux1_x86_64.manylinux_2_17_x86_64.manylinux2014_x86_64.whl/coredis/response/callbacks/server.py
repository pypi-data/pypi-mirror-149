from __future__ import annotations

import datetime
from typing import ClassVar

from coredis.commands import ResponseCallback
from coredis.response.types import ClientInfo, RoleInfo, SlowLogInfo
from coredis.response.utils import flat_pairs_to_dict
from coredis.typing import Any, AnyStr, List, Mapping, Tuple, Union
from coredis.utils import EncodingInsensitiveDict, nativestr


class TimeCallback(ResponseCallback):
    def transform(self, response: Any, **options: Any) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(int(response[0])) + datetime.timedelta(
            microseconds=int(response[1]) / 1000.0
        )


class SlowlogCallback(ResponseCallback):
    def transform(self, response: Any, **options: Any) -> Tuple[SlowLogInfo, ...]:
        return tuple(
            SlowLogInfo(
                id=item[0],
                start_time=int(item[1]),
                duration=int(item[2]),
                command=item[3],
                client_addr=item[4],
                client_name=item[5],
            )
            for item in response
        )


class ClientInfoCallback(ResponseCallback):
    INT_FIELDS: ClassVar = {
        "id",
        "fd",
        "age",
        "idle",
        "db",
        "sub",
        "psub",
        "multi",
        "qbuf-free",
        "argv-mem",
        "multi-mem",
        "obl",
        "oll",
        "omem",
        "tot-mem",
        "redir",
    }

    def transform(self, response: Any, **options: Any) -> ClientInfo:
        decoded_response = nativestr(response)
        pairs = [pair.split("=", 1) for pair in decoded_response.strip().split(" ")]

        info: ClientInfo = {}  # type: ignore
        for k, v in pairs:
            if k in ClientInfoCallback.INT_FIELDS:
                info[k] = int(v)  # type: ignore
            else:
                info[k] = v  # type: ignore
        return info


class ClientListCallback(ResponseCallback):
    def transform(self, response: Any, **options: Any) -> Tuple[ClientInfo, ...]:
        return tuple(ClientInfoCallback()(c) for c in response.splitlines())


class DebugCallback(ResponseCallback):
    INT_FIELDS: ClassVar = {"refcount", "serializedlength", "lru", "lru_seconds_idle"}

    def transform(
        self, response: Any, **options: Any
    ) -> Mapping[AnyStr, Union[AnyStr, int]]:
        # The 'type' of the object is the first item in the response, but isn't
        # prefixed with a name
        response = nativestr(response)
        response = "type:" + response
        response = dict([kv.split(":") for kv in response.split()])

        # parse some expected int values from the string response
        # note: this cmd isn't spec'd so these may not appear in all redis versions

        for field in DebugCallback.INT_FIELDS:
            if field in response:
                response[field] = int(response[field])

        return response


class InfoCallback(ResponseCallback):
    def transform(self, response: Any, **options: Any) -> Mapping[AnyStr, List[AnyStr]]:
        """Parses the result of Redis's INFO command into a Python dict"""
        info = {}
        response = nativestr(response)

        def get_value(value):
            if "," not in value or "=" not in value:
                try:
                    if "." in value:
                        return float(value)
                    else:
                        return int(value)
                except ValueError:
                    return value
            else:
                sub_dict = {}

                for item in value.split(","):
                    k, v = item.rsplit("=", 1)
                    sub_dict[k] = get_value(v)

                return sub_dict

        for line in response.splitlines():
            if line and not line.startswith("#"):
                if line.find(":") != -1:
                    key, value = line.split(":", 1)
                    info[key] = get_value(value)
                else:
                    # if the line isn't splittable, append it to the "__raw__" key
                    info.setdefault("__raw__", []).append(line)

        return info


class RoleCallback(ResponseCallback):
    def transform(self, response: Any, **options: Any) -> RoleInfo:
        role = nativestr(response[0])

        def _parse_master(response):
            offset, slaves = response[1:]
            res = {"role": role, "offset": offset, "slaves": []}

            for slave in slaves:
                host, port, offset = slave
                res["slaves"].append(
                    {"host": host, "port": int(port), "offset": int(offset)}
                )

            return res

        def _parse_slave(response):
            host, port, status, offset = response[1:]

            return dict(
                role=role,
                host=host,
                port=port,
                status=status,
                offset=offset,
            )

        def _parse_sentinel(response):
            return RoleInfo(role=role, masters=response[1:])

        parser = {
            "master": _parse_master,
            "slave": _parse_slave,
            "sentinel": _parse_sentinel,
        }[role]
        return RoleInfo(**parser(response))  # type: ignore


class LatencyHistogramCallback(ResponseCallback):
    def transform(self, response: Any, **options: Any) -> Mapping[AnyStr, Mapping]:
        histogram = flat_pairs_to_dict(response)
        for key, value in histogram.items():
            histogram[key] = EncodingInsensitiveDict(flat_pairs_to_dict(value))
            histogram[key]["histogram_usec"] = flat_pairs_to_dict(
                histogram[key]["histogram_usec"]
            )
        return histogram

import dataclasses
import enum
import json


class BaseEvent:

    def as_json(self):
        class EnhancedJSONEncoder(json.JSONEncoder):
            def default(self, o):
                if dataclasses.is_dataclass(o):
                    return dataclasses.asdict(o)
                elif isinstance(o, enum.Enum):
                    return {o.name: o.value}
                return super().default(o)

        return json.dumps(self, cls=EnhancedJSONEncoder)

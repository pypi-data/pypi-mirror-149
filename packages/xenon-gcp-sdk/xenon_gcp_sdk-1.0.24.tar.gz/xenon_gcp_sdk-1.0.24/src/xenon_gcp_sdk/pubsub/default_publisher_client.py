from concurrent.futures import Future
from typing import Optional

import google
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future

from .publisher_client import PublisherClient
from .Message import Message
from .errors import exception_mapper

_, project_id = google.auth.default()


@exception_mapper
class DefaultPublisherClient(PublisherClient):
    def __init__(self, publisher: Optional[pubsub_v1.PublisherClient] = None):
        self._publisher: PublisherClient = publisher or pubsub_v1.PublisherClient()

    def topic_path(self, topic_name):
        return self._publisher.topic_path(project_id, topic_name)

    def close(self):
        pass

    def publish(self, message: Message) -> Future:
        future: Future = self._publisher.publish(message.topic_name, message.payload.encode('utf-8'))
        future.result = exception_mapper(future.result)
        return future

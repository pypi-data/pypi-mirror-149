import logging

import google
import google_crc32c
from google.cloud import secretmanager

_, project_id = google.auth.default()


def get_secret(secret_id, version=1):
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"

    response = client.access_secret_version(request={"name": name})

    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        logging.info("Data corruption detected.")

    return response.payload.data.decode("UTF-8")

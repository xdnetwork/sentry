# type:ignore
import uuid
from datetime import datetime
from hashlib import sha1

import msgpack
import pytest
from arroyo import Message, Partition, Topic
from arroyo.backends.kafka import KafkaPayload

from sentry.models import EventAttachment, File
from sentry.replays.consumers.recording.process_recording import ProcessRecordingStrategy


def commit(mapping):
    pass


@pytest.mark.django_db
def test_basic_payload():  # NOQA
    replay_id = uuid.uuid4().hex
    replay_recording_id = uuid.uuid4().hex
    project_id = 1
    chunk1 = {
        "payload": b'{"sequence_id":0}\ntest',
        "replay_id": replay_id,
        "project_id": project_id,
        "id": replay_recording_id,
        "chunk_index": 0,
        "type": "replay_recording_chunk",
    }

    processing_strategy = ProcessRecordingStrategy(commit)
    processing_strategy.submit(
        Message(
            Partition(Topic("ingest-replay-recordings"), 1),
            1,
            KafkaPayload(b"key", msgpack.packb(chunk1), [("should_drop", b"1")]),
            datetime.now(),
        )
    )
    processing_strategy.poll()
    processing_strategy.join(1)

    chunk2 = {
        "payload": b"foobar",
        "replay_id": replay_id,
        "project_id": project_id,
        "id": replay_recording_id,
        "chunk_index": 1,
        "type": "replay_recording_chunk",
    }

    processing_strategy = ProcessRecordingStrategy(commit)
    processing_strategy.submit(
        Message(
            Partition(Topic("ingest-replay-recordings"), 1),
            1,
            KafkaPayload(b"key", msgpack.packb(chunk2), [("should_drop", b"1")]),
            datetime.now(),
        )
    )
    processing_strategy.poll()
    processing_strategy.join(1)

    replay = {
        "type": "replay_recording",
        "replay_id": replay_id,
        "replay_recording": {
            "chunks": 2,
            "id": replay_recording_id,
        },
        "project_id": project_id,
    }

    processing_strategy.submit(
        Message(
            Partition(Topic("ingest-replay-recordings"), 1),
            1,
            KafkaPayload(b"key", msgpack.packb(replay), [("should_drop", b"1")]),
            datetime.now(),
        )
    )
    processing_strategy.poll()
    processing_strategy.join(20000)

    recording = File.objects.get(name=f"rr:{replay_recording_id}")

    assert recording
    assert recording.checksum == sha1(b"testfoobar").hexdigest()

    assert EventAttachment.objects.get(event_id=replay_id)

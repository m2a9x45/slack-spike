import uuid

store = {}


def add_callback(workflow_id, channel, thread_ts, next_step):
    id = str(uuid.uuid4())
    store[id] = {
        "workflow_id": workflow_id,
        "channel": channel,
        "thread": thread_ts,
        "next_step": next_step
    }

    print(store)

    return id


def get_store(id):
    return store[id]

import uuid
import random
import time
import requests


API_URL = "https://voting-api-156574710110.asia-southeast1.run.app/vote"

def generate_vote():
    return {
        "user_id": str(uuid.uuid4()),
        "poll_id": "poll_1",
        "choice": random.choice(["A", "B", "C"]),
        "timestamp": time.time(),
        "edge_id": f"edge-node-{random.randint(1, 4)}"
    }

def send_vote(vote):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json=vote, timeout=5)
            if response.status_code == 200:
                print(f"Vote sent: {vote['user_id']} | Choice: {vote['choice']} | Edge: {vote['edge_id']}")
                return
            else:
                print(f"Unexpected status {response.status_code}, retrying...")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    print(f"Failed to send vote after {max_retries} attempts")

def run_edge_node():
    print("Edge node started...")
    while True:
        vote = generate_vote()
        send_vote(vote)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_edge_node()
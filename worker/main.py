from google.cloud import pubsub_v1, firestore
import json
import time
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

PROJECT_ID = "elegant-canto-495811-h4"
SUBSCRIPTION_ID = "vote-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
db = firestore.Client(project=PROJECT_ID)

# Health check server for Cloud Run
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, *args):
        pass

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("", port), HealthCheck)
    server.serve_forever()

def process_vote(message):
    try:
        vote = json.loads(message.data.decode("utf-8"))
        print(f"Received vote: {vote['user_id']} | Poll: {vote['poll_id']} | Choice: {vote['choice']}")

        doc_id = f"{vote['user_id']}_{vote['poll_id']}"
        db.collection("votes").document(doc_id).set(vote)
        print(f"Processed vote: {vote['user_id']} | Poll: {vote['poll_id']}")
        message.ack()

    except Exception as e:
        print(f"Error processing vote: {e}")

def main():
    # Start health check server in background
    threading.Thread(target=run_health_server, daemon=True).start()
    print("Worker started, listening for votes...")
    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=process_vote
    )
    with subscriber:
        try:
            streaming_pull_future.result()
        except Exception as e:
            streaming_pull_future.cancel()
            print(f"Worker stopped: {e}")

if __name__ == "__main__":
    main()
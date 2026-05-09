# CS323 Distributed Voting System — Group 8

## Members
- Austria Keith L. (Phase 1, 2, 3)
- Saguilayan Hans Aldrich (Phase 4)
- Seth Pals (Phase 5)
- Oga (Phase 6)

## System Overview
A distributed voting system built on Google Cloud Platform (GCP) using an event-driven pipeline architecture:

Edge Nodes → Cloud Run API → Pub/Sub → Worker Service → Firestore



## GCP Services Used
- **Cloud Run** — Hosts the API and Worker services
- **Pub/Sub** — Handles asynchronous message communication
- **Firestore** — Stores processed votes persistently

## Setup Instructions

### Prerequisites
- Google Cloud Platform account
- Python 3.11+
- gcloud CLI installed

### Step 1: Clone the Repository
```bash
git clone https://github.com/RAHHHKETT/voting-system.git
cd voting-system
```

### Step 2: Install Dependencies
```bash
pip install flask google-cloud-pubsub google-cloud-firestore requests
```

### Step 3: Deploy Cloud Run API
```bash
cd api
gcloud run deploy voting-api \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --project elegant-canto-495811-h4
```

### Step 4: Deploy Worker Service
```bash
cd ../worker
gcloud run deploy voting-worker \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --project elegant-canto-495811-h4 \
  --no-cpu-throttling \
  --min-instances 1
```

### Step 5: Run Edge Node
```bash
cd ../edge
python edge_node.py
```

## Cloud Run API Endpoint
https://voting-api-156574710110.asia-southeast1.run.app

## Individual Reflections

### Keith
Setting up the GCP infrastructure was honestly a pain especially with the billing issues and permission errors, but it taught me how cloud services like Cloud Run are configured to handle distributed requests. Deploying the API made me realize how edge nodes independently push data to the cloud without needing to know what happens after, which is what makes distributed systems powerful.

### Hans
Building the worker service showed me how Pub/Sub and Firestore work together to process and store messages asynchronously without blocking other parts of the system. The idempotency logic was something I didn't expect to be important, but it actually prevents duplicate votes from messing up the final data in Firestore.

### Seth
Doing the fault injection testing was actually the most interesting part because I got to see firsthand how the system kept running even when the worker was completely disabled. It was cool watching Pub/Sub silently buffer all the votes and then seeing Firestore instantly catch up the moment the worker was restored.

### Oga
Documenting the system architecture helped me understand how each component has a single clear responsibility, which is what makes the whole system fault tolerant and scalable. Distributed systems seem complex at first but seeing how edge nodes, Cloud Run, Pub/Sub, and Firestore each handle their own layer made it click for me.
# Mini-RAG Project Development History

This document serves as a persistent record of our development journey for the Mini-RAG application. It tracks all the major milestones from the initial setup up until our deployment to the AWS server, ensuring that this history is permanently saved in your project folder.

## Phase 0: Learning the Foundations — Abu Bakr Soliman's Course (Self-Study)
- **Course:** This entire project is based on a YouTube course by **Abu Bakr Soliman**. The full playlist can be found here: [Mini-RAG Course Playlist](https://youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&si=QAApyZ96TzWvkios)
- **Self-Written Code:** Before any AI assistance was involved, all the core application code was written **by hand** by following the course. This includes the foundational RAG architecture, the project structure, the data models, the API routes, and the initial NLP pipeline.
- **AI Assistance Begins at Phase 1:** The Antigravity AI assistant was only brought in starting from Phase 1, to help optimize, extend, and deploy what had already been built from scratch through the course.

## Phase 1: Environment Setup & Core Data Processing (April)
- **Environment Configuration:** We started by resolving initial setup errors related to the Python environment (Python Environment Tools), Conda activation scripts, and Windows terminal configurations to establish a stable development space in VS Code.
- **Data Processing Optimization:** We deeply refined the `ProcessController.py` to handle document ingestion. We replaced a custom text splitter with the more robust `RecursiveCharacterTextSplitter`, fixed logic bugs related to chunk overlaps, improved error logging, and ensured that document metadata is properly preserved during the ingestion phase.

## Phase 2: Advanced RAG & Persistent Conversational Memory (Early May)
- **Context-Aware RAG:** We upgraded the application to handle stateful conversations. We implemented the "Condense Question" strategy (Query Rewriting) within the NLP Controller, allowing the LLM to understand and resolve context-dependent follow-up questions accurately. We also fixed several bugs related to language detection.
- **Persistent Database Memory:** Realizing that client-side memory wasn't enough for external platforms, we transitioned the system to use a PostgreSQL-backed database for memory. We created the necessary database schemas, built the `ChatModel` for CRUD operations, and updated the FastAPI backend to store, fetch, and manage conversation history using unique `session_id`s.

## Phase 3: WhatsApp Webhook Integration (May 5 - May 9)
- **Meta API Configuration:** We registered and configured the Meta Developer application, managing API access tokens securely.
- **Webhook Bridge:** We successfully created and verified the webhook communication bridge between our FastAPI backend and the Meta WhatsApp Cloud API.
- **Message Processing:** We integrated FastAPI background tasks to receive, process, and respond to incoming WhatsApp messages seamlessly. The system now maps a user's WhatsApp number to their database session, retrieving their history and generating context-aware answers using the RAG infrastructure before replying via WhatsApp.

## Phase 4: AWS Server Deployment (May 9 - May 11)

> ⚠️ **Note:** The deployment steps in this phase were also followed from **Abu Bakr Soliman's course deployment videos** (same playlist linked in Phase 0). Both the course steps and AI assistance were used together. This section serves as a **reference guide** — if you ever get stuck or need to redo any deployment step, come back here.

- **Server Provisioning:** We began transitioning the application from your local Windows machine to an AWS Lightsail production server running Ubuntu. *(Course + AI assisted)*
- **Code Synchronization:** We set up SSH keys (fixing a "Permission denied" error along the way) and utilized Git to push the codebase from local development and pull it onto the remote server. *(Course + AI assisted)*
- **Docker Production Setup:** We configured and launched persistent Docker services for the entire stack (FastAPI backend, Streamlit frontend, and PostgreSQL database) on the Ubuntu environment. *(Course + AI assisted)*
- **Secure Tunneling:** We established secure communication tunnels to expose the server's backend to the internet, ensuring the Meta WhatsApp webhook could successfully reach our newly deployed production server. *(Course + AI assisted)*

## Phase 5: HTTPS, Custom Domain & Production Token (May 12)

- **Fixed Git Mess:** Found an accidental `.git` folder in `C:\Users\0b901` (entire home directory was being tracked). Deleted it — Source Control is now clean.
- **DuckDNS Free Domain:** Registered `ibrahem-basem.duckdns.org` and pointed it to the static AWS Lightsail IP `3.110.134.125`.
- **AWS Lightsail Firewall:** Opened ports **80** (HTTP) and **443** (HTTPS) to allow public traffic.
- **SSL Certificate (Let's Encrypt):** Installed Certbot on the server, temporarily stopped the Docker Nginx container, ran `certbot --standalone` to issue a valid SSL certificate for the domain. Auto-renewal was configured by Certbot. Certificate valid until **August 10, 2026**.
  - Cert path: `/etc/letsencrypt/live/ibrahem-basem.duckdns.org/`
- **Nginx Docker Container Reconfigured:** Updated `docker/nginx/default.conf` to:
  - Redirect all HTTP (port 80) → HTTPS (port 443)
  - Terminate SSL using the Let's Encrypt certificate
  - Reverse proxy all HTTPS traffic to the FastAPI container (`fastapi:8000`) — works because both containers share the `backend` Docker network.
  - Kept the hidden telemetry endpoint `/telemetry_x7b92mq`
- **Updated `docker-compose.yml`:** Added port `443:443` and mounted `/etc/letsencrypt` as a read-only volume into the Nginx container.
- **Meta Webhook Updated:** Updated the Callback URL in Meta Developer Console to `https://ibrahem-basem.duckdns.org/api/v1/whatsapp/webhook` with verify token `minirag_secure_token_2026`. Subscribed to the `messages` webhook field.
- **Permanent System User Token:** Instead of the expiring 24-hour temporary token, created a **System User** (`minirag-bot`) in Meta Business Manager with Admin access. Assigned the app and WhatsApp account with Full Access. Generated a **permanent non-expiring token** with `whatsapp_business_messaging` and `whatsapp_business_management` permissions. Updated the token in `docker/env/.env.app` and restarted FastAPI.
- **End-to-End Test:** ✅ Sent a real WhatsApp message → FastAPI received it → RAG processed it → Response sent back successfully.

---
📌 **Reference Reminder:** If you ever get lost or need to redo any of these steps, refer back to:
1. **This file** (`PROJECT_HISTORY.md`) for a high-level overview of what was done.
2. **Abu Bakr Soliman's playlist** for the step-by-step video walkthrough: [Mini-RAG Course Playlist](https://youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&si=QAApyZ96TzWvkios)
3. **The AI assistant** for any extended or custom steps we added on top of the course.

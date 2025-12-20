# ByteBattles

ByteBattles is a competitive programming platform with a custom-built,
distributed judging system inspired by platforms like Codeforces.

The project focuses on **systems design**, **isolation**, and
**asynchronous execution**, rather than UI polish or deployment.

------------------------------------------------------------------------

## 🧠 Architecture Overview

ByteBattles is built using an **asynchronous message-driven
architecture** with a **queue-centric pipeline** coordinated via Redis.

There are no synchronous APIs between components. Each subsystem
communicates exclusively through queues.

### Core Components

-   **Web Layer (Django)**
    -   Handles users, problems, submissions, and metadata
    -   Pushes submissions into Redis queues
-   **Judge Worker**
    -   Listens on Redis submission queues
    -   Spawns language-specific Docker containers
    -   Compiles and executes code inside isolated sandboxes
    -   Measures time and memory usage
-   **Result Worker**
    -   Consumes execution results from Redis
    -   Updates verdicts, statistics, and user profiles in PostgreSQL

------------------------------------------------------------------------

## ⚙️ Key Features

-   Docker-based sandboxing for C, C++, and Python
-   Alpine-based minimal judge images
-   No network access inside execution containers
-   Dropped Linux capabilities and non-root execution
-   Time and memory limit enforcement
-   Deterministic judging using structured test cases
-   Django management-command based workers

------------------------------------------------------------------------

## 🐳 Judge Isolation Model

Each submission is executed in a fresh Docker container with:

-   No network access
-   Restricted process limits
-   User-level execution
-   Explicit timeouts
-   Memory usage tracking

Judge containers are spawned dynamically at runtime rather than being
long-running services.

------------------------------------------------------------------------

## 📁 Project Structure

```
Bytebattles
├── README.md
├── requirements.txt
├── run_local.sh
├── build_images.sh
├── screenshots
├── bytebattles
│   ├── app
│   │   ├── migrations
│   │   └── templates
│   ├── bytebattles
│   ├── judge
│   │   ├── management
│   │   │   └── commands
│   │   └── migrations
│   ├── problems
│   │   ├── migrations
│   │   └── templates
│   ├── profile_
│   │   ├── migrations
│   │   └── templates
│   └── submissions
│       ├── migrations
│       └── templates
├── judge_images
│   ├── c
│   ├── cpp
│   └── python
├── judge_worker
└── test_case_data
    ├── 1CSES
    │   ├── input
    │   └── output
    ├── 2CSES
    │   ├── input
    │   └── output
    ├── 3CSES
    │   ├── input
    │   └── output
    └── 4CSES
        ├── input
        └── output
```

------------------------------------------------------------------------

## ▶️ Running Locally (Development)

This project is not production-deployed.\
Local execution is supported via helper scripts.

``` bash
./build_images.sh
./run_local.sh
```

Workers are started manually as independent processes.

------------------------------------------------------------------------

## 🧪 Test Data

The judging pipeline has been validated using problems from the **CSES
problem set**, with **explicit permission from the CSES author** to use
the data for this project.

------------------------------------------------------------------------

## ⚠️ Notes

-   This repository represents an evolving system
-   Some components are intentionally minimal or experimental
-   Deployment configuration is intentionally omitted
-   The focus is on architecture and execution correctness

Some screenshots showcasing the judging system is included in
the repository at `screenshots/`.

------------------------------------------------------------------------

## 📌 Tech Stack

-   Python, Django
-   Docker
-   Redis
-   PostgreSQL

------------------------------------------------------------------------

## 📄 License

This project is intended for educational and demonstrative purposes.

চলো ভাই, এবার আমরা একটা বাস্তব Production-Level DevOps AI Automation Agent তৈরি করব, যেখানে AI নিজে কাজের সিদ্ধান্ত নিতে পারবে, কিন্তু গুরুত্বপূর্ণ কোনো কাজ Execute করার আগে মানুষের কাছ থেকে Email-এর মাধ্যমে Approval চাইবে।

এই Project-এ আমরা Human-in-the-Loop (HITL) implement করব LangChain এবং LangGraph দিয়ে।

এটা DevOps + AI Engineering ক্যারিয়ারের জন্য খুবই গুরুত্বপূর্ণ একটি Project।
Project: AI-Powered DevOps Automation Agent
Production-oriented project
 LangChain + LangGraph
 Human-in-the-Loop

1. আমরা কী তৈরি করব?
ধরো, তোমার Linux server-এ Disk Usage 90% হয়ে গেছে।

আমাদের AI Agent:
1. Server monitoring করবে।
2. Disk usage 90% দেখলে সমস্যা শনাক্ত করবে।
3. কী কী file cleanup করা নিরাপদ, সেটা Analyze করবে।
4. একটি cleanup plan তৈরি করবে।
5. তোমার Email-এ Approval Request পাঠাবে।
6. তুমি Email থেকে Approve অথবা Reject করবে।
7. Approve হলে তবেই cleanup script Execute হবে।
8. Reject হলে কোনো destructive action হবে না।
9. Execution শেষে Email-এ Report পাঠাবে।
2. Complete Architecture








medium.com


আমাদের Workflow হবে:
1. DevOps Monitoring Agent

CPU, RAM, Disk, Docker, Service Health


2. AI Analysis — LangChain

Problem detection and action planning


3. Human Approval — LangGraph

Workflow pauses and waits for approval


Approved

Execute action


Rejected

Stop workflow




4. Email Notification & Audit Log

Execution result, timestamp, approval history


3. কোন কোন Technology ব্যবহার করব?
Technology	কাজ
Python	Main programming
LangChain	LLM, prompts, tools
LangGraph	Workflow orchestration
FastAPI	Approval API
SMTP / Gmail	Approval email
SQLite / PostgreSQL	Approval history
psutil	Server monitoring
pathlib	File inspection
Docker	Containerization
Linux	Actual DevOps environment

4. Project Folder Structure
আমরা শুরু থেকেই Professional Structure অনুসরণ করব।
devops-ai-agent/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── agents/
│   │   ├── monitoring_agent.py
│   │   └── analysis_agent.py
│   │
│   ├── tools/
│   │   ├── system_monitor.py
│   │   ├── docker_monitor.py
│   │   └── cleanup_tool.py
│   │
│   ├── workflows/
│   │   └── devops_graph.py
│   │
│   ├── approvals/
│   │   ├── email_service.py
│   │   └── approval_api.py
│   │
│   └── database/
│       └── models.py
│
├── tests/
├── .env
├── requirements.txt
├── Dockerfile
└── README.md


5. Human-in-the-Loop কীভাবে কাজ করবে?
ধরো Agent এই Plan তৈরি করল:
DevOps AI Agent
Approval Required

Server Disk Cleanup Request

Server: dev-server-01
- Disk Usage: 92%
- Docker unused images: 4
- Estimated reclaimable space: 2 GB
Proposed Action

docker image prune -f

এই উদাহরণে Email-এ Approval Request যাবে।
APPROVE

REJECT


এটি আমাদের কাঙ্ক্ষিত Email UI-এর একটি Mockup, এখনো কোনো বাস্তব Action চালাচ্ছে না।

এখানে সবচেয়ে গুরুত্বপূর্ণ বিষয়:

LangGraph-এর interrupt() ব্যবহার করে Workflow Pause করব।

তারপর:
- Approval না আসা পর্যন্ত execution বন্ধ থাকবে।
- Email-এর Approve/Reject link FastAPI endpoint-এ যাবে।
- LangGraph-এর Command(resume=...) দিয়ে Workflow আবার শুরু হবে।
- Approved না হলে কোনো cleanup execution হবে না।
আমরা LangGraph Checkpointer ব্যবহার করব, যাতে Server Restart হলেও Pending Approval-এর Workflow হারিয়ে না যায়।

একটি গুরুত্বপূর্ণ Security Rule: AI সরাসরি Shell Command execute করতে পারবে না। শুধু allowlisted action execute হবে। Approval token হবে signed, expiring এবং একবার ব্যবহারযোগ্য। প্রথমে সব action dry-run mode-এ পরীক্ষা করব।
6. আমাদের Learning & Development Roadmap
1. Day 1 — System Monitoring
   
   Python দিয়ে CPU, RAM, Disk এবং Docker monitoring।
2. Day 2 — LangChain Tools
   
   Python functions-কে AI Agent-এর Tools হিসেবে ব্যবহার।
3. Day 3 — LangGraph
   
   State, Nodes, Edges, Conditional Edges এবং Checkpointer।
4. Day 4 — Email Integration
   
   Gmail SMTP দিয়ে Approval Request পাঠানো।
5. Day 5 — Human-in-the-Loop
   
   interrupt() এবং Command(resume=...) দিয়ে approval workflow।
6. Day 6 — FastAPI Integration
   
   Approve/Reject API তৈরি।
7. Day 7 — Production Deployment
   
   Docker, PostgreSQL, logging, security এবং audit trail।
7. আজকের প্রথম কাজ
আমরা একদম Basic থেকে শুরু করব, কিন্তু প্রতিটি কোড Production Engineering-এর দৃষ্টিতে বুঝব।

প্রথমে তোমার Linux server-এর System Monitoring Module তৈরি করব। তারপর সেটিকে LangChain Tool বানাব।

একটা প্রশ্ন: Approval Email পাঠানোর জন্য কোনটি ব্যবহার করতে চাও?
- Gmail SMTP (নিজের Gmail)
- Company SMTP Server
চাইলে আগামীকাল থেকে এই Project-এর প্রতিদিনের পরবর্তী Practical Lesson-ও আমি সাজিয়ে দিতে পারি।









*****************next update ********************

Feature	                        Priority
Multiple server monitoring	      High
Linux + Windows support	         High
Secure authentication (JWT)	   High
Dashboard (React)	               High
Server-wise alert history	      High
Approval audit logs	            High
Role-based access control	      High
Docker deployment	               High
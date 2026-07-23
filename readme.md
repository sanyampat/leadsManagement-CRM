# Outreach CRM

A lightweight CRM built for freelancers to organize leads, track conversations, and manage outreach from one place. Instead of juggling spreadsheets, notes, and messaging apps, this application keeps every prospect in a simple sales pipeline.

---

## Features

### 📋 Lead Management

* Add, edit, and delete contacts
* Store business name, contact details, and notes
* Search leads by name or business
* Filter by service offered

### 📊 Sales Pipeline

Track every lead through a simple workflow:

```
New
   ↓
Contacted
   ↓
Replied
   ↓
Interested
   ↓
Won
```

Leads can also be marked as **Lost**.

### 💬 Outreach Templates

Built-in templates for:

* WhatsApp
* Email

Supported services:

* Web Design
* Video Editing

Templates support placeholders such as:

```
{name}
{business}
```

making each message automatically personalized.

### 📱 Message Composer

Generate outreach messages directly inside the application.

* WhatsApp integration
* Email integration
* Copy message to clipboard
* Open WhatsApp with the generated message
* Open default email client
* Mark a lead as contacted

### 🔍 Search & Filtering

Quickly find contacts using:

* Name
* Business
* Service
* Status

### 💾 Persistent Storage

All contacts and templates are saved locally, so your data remains available after closing the application.

---

# Tech Stack

## Frontend

* React
* JavaScript
* Tailwind CSS
* Lucide React Icons

## Storage

* Local Storage API

---

# Screens

* Contact Dashboard
* Pipeline Overview
* Add/Edit Contact
* Message Composer
* Template Manager

---

# Contact Information

Each lead stores:

```
Name

Business

Phone

Email

Service

Status

Notes

Last Contacted

Created Date
```

---

# Supported Services

* Web Design
* Video Editing

Additional services can easily be added by extending the service configuration.

---

# Project Structure

```
src/
│
├── OutreachTracker.jsx
│
├── Components
│   ├── ContactCard
│   ├── ContactForm
│   ├── ComposeModal
│   ├── PipelineBar
│   ├── TemplateCard
│   └── StatusBadge
│
└── Storage
```

---

# Workflow

```
Add Lead
      │
      ▼
Select Service
      │
      ▼
Generate Message
      │
      ▼
Send via WhatsApp / Email
      │
      ▼
Mark as Contacted
      │
      ▼
Update Pipeline
      │
      ▼
Win or Lose Client
```

---

# Future Improvements

* AI-generated personalized outreach
* Website audit integration
* Follow-up reminders
* Calendar scheduling
* Proposal generator
* Invoice generator
* Revenue dashboard
* Chrome extension for saving leads
* CRM export/import
* Multi-user support
* Analytics and conversion tracking

---

# Getting Started

Clone the repository:

```bash
git clone https://github.com/yourusername/outreach-crm.git
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

---

# Vision

This project is designed to be more than a contact manager. The long-term goal is to evolve it into an AI-powered freelance operating system that helps users discover potential clients, organize leads, personalize outreach, track conversations, generate proposals, and manage the complete client acquisition workflow from first contact to project completion.

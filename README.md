
# 🌾 KisaanMitra — AI Agents for Smarter Farming



---

### 🌱 Overview

Agriculture remains the livelihood of millions in India, yet farmers often struggle with unreliable weather forecasts, inconsistent soil data, and fluctuating market prices. Most advisory platforms are not localized, hard to access, or fail to adapt to changing regional conditions — leaving small farmers without timely, data-driven insights for critical decisions.

**KisaanMitra** reimagines agricultural intelligence through a **multi-agent AI system** where agents collaborate to gather, analyze, and interpret weather, soil, and market information to provide **personalized, real-time farming guidance**.

The system empowers farmers to:

* 🌾 Choose the right crops for the season
* 🌦️ Plan sowing and irrigation schedules
* 💰 Track market demand and pricing trends
* 🧠 Make informed, sustainable decisions

---

### 🎯 Challenge

**Goal:**
Design a multi-agent system where specialized AI agents coordinate seamlessly using **Google’s Agent Development Kit (ADK)** and the **Agent-to-Agent (A2A)** protocol to deliver actionable agricultural insights.

---

### 🧩 System Architecture

**Architecture Overview:**
The system consists of **three specialized sub-agents** managed by a **Root Orchestrator Agent**.

Each agent performs a domain-specific task and communicates through the A2A protocol to ensure synchronized data flow and context sharing.

```
Root Orchestrator Agent
├── Soil Agent     → Analyzes soil nutrients, pH, and moisture data
├── Weather Agent  → Fetches and interprets local weather and rainfall forecasts
└── Market Agent   → Tracks market prices, crop demand, and trading insights
```

All agents run under a single ADK service and communicate internally via the A2A protocol.

---

### 🤖 Agents Description

| Agent                       | Function                                                                                                                               |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Root Orchestrator Agent** | Acts as the central controller; receives user queries, delegates tasks to sub-agents, and compiles responses into actionable insights. |
| **Soil Agent**              | Analyzes real-time and historical soil data (nutrient content, pH, moisture) and suggests optimal crop types.                          |
| **Weather Agent**           | Integrates weather APIs to forecast rainfall, temperature, and humidity trends for precise sowing and irrigation planning.             |
| **Market Agent**            | Monitors local and regional market trends to recommend profitable crops and selling periods.                                           |

---

### 🏗️ Technology Stack

* **Backend Framework:** Google Agent Development Kit (ADK)
* **Communication Protocol:** Agent-to-Agent (A2A)
* **Language:** Python 3.10+
* **AI Model:** Gemini 2.5 Flash (for reasoning and response generation)
* **Package Manager:** pip

---

### ⚙️ Setup & Execution

#### 1. Prerequisites

Make sure you have the following installed:

* **Python 3.10+**
* **pip** (Python package manager) → already included with Python; verify using:

  ```bash
  pip --version
  ```
* **Google API Key** with **Gemini API access**

---

#### 2. Configure Environment Variables

Each agent directory should contain a `.env` file with your API key:

```
GOOGLE_API_KEY=your_api_key_here
```

Example paths:

```
agents/root_agent/.env
agents/soil_agent/.env
agents/weather_agent/.env
agents/market_agent/.env
```

---

#### 3. Run the Agents

You can start and manage all agents using **Google ADK Web**.

1. Open a terminal and navigate to your project directory:

   ```bash
   cd agents
   ```
2. Launch the **ADK Web interface**:

   ```bash
   adk web
   ```
3. Once the web console opens (default: [http://localhost:8000](http://localhost:8000)), start all agents — **Root, Soil, Weather, and Market** — from the dashboard.

✅ All agents run under a **single ADK service**, communicating internally through the **A2A protocol**.

---

### 💡 How It Works

1. **Data Gathering:**
   The sub-agents collect soil, weather, and market data from external APIs and databases.

2. **Collaboration via A2A Protocol:**
   The Root Agent communicates with all sub-agents using Google’s **A2A protocol**, ensuring synchronized and modular operation.

3. **Analysis & Reasoning:**
   Each sub-agent processes its data using **Gemini’s reasoning** capabilities to generate actionable insights.

4. **Unified Response:**
   The Root Orchestrator compiles these insights into a consolidated recommendation for the farmer.

---

### 🧠 Features

* 🌾 **Localized Agricultural Intelligence** — Tailored insights for regional conditions
* 🌦️ **Real-Time Weather-Aware Advice** — Forecast-based crop scheduling
* 💰 **Market-Driven Recommendations** — Predictive crop value analysis
* 🧩 **Multi-Agent Collaboration** — Modular and scalable design using Google ADK
* ⚙️ **Agent Interoperability** — Seamless coordination through A2A protocol

---

### 🧪 Project Status

**Status:** ✅ Working Demo
All agents successfully communicate and generate integrated farming insights through orchestrated reasoning.

---

### 📝 Notes

* All agents must be running inside the ADK Web console before the orchestrator compiles responses.
* Use **Ctrl+C** to stop the ADK service.
* Ensure your Google API key is valid for Gemini API access.

---

### 📚 References & Credits

* **Google ADK Workshop** – *Introduction to Google-ADK* (used as a learning reference for building and structuring the multi-agent system)
* **Google AI Agent Bake Off 2025** – Challenge inspiration for developing KisaanMitra’s multi-agent architecture
* **Gemini API Documentation** – For integrating Gemini 2.5 Flash model reasoning and data analysis

---

### 🏆**Built for a Hackathon Project (Inspired by Google AI Agent Bake Off 2025)**

This project was developed as part of a hackathon, inspired by Google’s AI Agent Bake Off 2025 challenge. It showcases how multi-agent systems built with the Google Agent Development Kit (ADK) and Gemini API can revolutionize farming through intelligent collaboration.

Built with ❤️ and innovation by the **KisaanMitra Team**
---





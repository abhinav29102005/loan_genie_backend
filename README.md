# Loan Agent System

Multi-agent loan processing system built with CrewAI and Google Gemini.

## 🚀 Getting Started

### Step 1: Create a Virtual Environment

From the project root directory:

**Windows (PowerShell)**
```bash
python -m venv venv
```

**macOS / Linux**
```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment

**Windows (PowerShell)**
```bash
.\venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal prompt.

### Step 3: Install Dependencies

> ⚠️ Always use `python -m pip` to avoid path issues
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 4: Environment Variables

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

> ⚠️ **Never commit `.env` files to version control**

### Step 5: Run the Project
```bash
python main.py
```

## 📝 Usage

Type your loan queries when prompted. Type `exit`, `quit`, or `bye` to end the conversation.

## 📂 Project Structure
```
loan-agent-system/
├── .env
├── requirements.txt
├── agents/
│   └── sales_agent.py
├── tools/
└── main.py
```

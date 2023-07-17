# intent_classification

Classify intent and objects of real-state queries.

## Installation

### Step 1: Clone the project

```powershell
git clone https://github.com/beicodewarrior/intent_classification.git
```

### Step 2: Create virtual environment with `Python 3.10.8` and install dependencies

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Add OpenAI API Key in `.env` file

Create `.env` file inside `project` directory and add the following environment variables:

```plaintext
OPENAI_API_KEY=sk-238dd3...
```

### Step 4: Run the Script

```powershell
python classification.py
```

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

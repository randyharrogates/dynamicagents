# dynamicagents
A microservice to create agents and langgraph workflows

* Note: This service does not provide the LLM logic. This service will only create Agents with a set of logic provided to the service

## To run API

1. Create virtual environment

```bash
python3 -m venv venv
```
2. Activate virtual environment

For windows:

```bash
.\venv\Scripts\activate
```

For Mac/Linux:

```bash
source venv/bin/activate
```

3. Go into source directory:

```bash
cd src
```

4. Run the following command:

```bash
uvicorn main:app --reload
```

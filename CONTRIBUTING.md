# Contributing guide

How this repo is organised and how we work in it. Read this before your first pull request.

---

## 1. Repo map

```
airbnb-investment-app/
├── app/                  Streamlit website (display only)
│   ├── Home.py           Entry point: streamlit run app/Home.py
│   └── pages/            One .py file per extra page (auto-added to sidebar)
├── src/                  All logic as reusable functions (NO Streamlit code)
│   ├── cleaning.py       Price parsing, outliers, "active listing" rules
│   ├── metrics.py        Occupancy proxy, revenue, yield
│   ├── scoring.py        Investment score + persona weights
│   └── ai/               Prompts, JSON schema checks, LLM client, cost logging
├── notebooks/            Databricks pipeline notebooks (01_bronze ... 05_export)
├── data/
│   └── gold/             Small Parquet files the app reads (exported from Databricks)
├── tests/                Pytest tests for src/ (test_cleaning.py, etc.)
├── docs/                 Documentation pack, decisions log, kickoff notes
├── .github/              CI workflows and the pull request template
├── .streamlit/           config.toml (theme). secrets.toml is NEVER committed
├── requirements.txt      Python packages (Streamlit Cloud installs from this)
├── .env.example          Which secrets you need (copy to .env, fill in, never commit)
└── README.md             Project overview, live app link, how to run
```

### The golden rule

**Logic lives in `src/`, display lives in `app/`.**
If you're writing a calculation, it goes in a function in `src/` and gets a test in `tests/`.
The app and the Databricks notebooks both import it. One calculation, one place to fix it.

### Where does my file go?

| I'm writing...                                  | Put it in                  |
|-------------------------------------------------|----------------------------|
| A new app page                                  | `app/pages/N_Page_Name.py` |
| A cleaning / metric / scoring calculation       | `src/` + a test in `tests/`|
| An AI prompt or LLM call                        | `src/ai/`                  |
| A Databricks pipeline step                      | `notebooks/`               |
| An output file the app needs                    | `data/gold/` (Parquet)     |
| Documentation, notes, a decision                | `docs/`                    |

---

## 2. Setting up

```bash
git clone https://github.com/louiss1010/airbnb-investment-app.git
cd airbnb-investment-app
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env               # then fill in your own values
python -m streamlit run app/Home.py
```

In VS Code, select the `.venv` interpreter (Ctrl/Cmd+Shift+P → "Python: Select Interpreter").

---

## 3. Workflow

1. **Pick an issue** on the project board and assign yourself. No issue? Create one first.
2. **Start from an up-to-date `main`:** switch to `main` and Sync / `git pull`.
3. **Create a new branch** for that one task (see naming below).
4. **Commit small and often** with clear messages.
5. **Push and open a pull request** into `main`.
6. **Get one approval**, fix any comments, then merge.
7. **Delete the branch**, switch back to `main`, and pull.

Never reuse a branch after it has been merged. Start a fresh one from `main`.

### Branch names

| Type        | Pattern                  | Example                      |
|-------------|--------------------------|------------------------------|
| New feature | `feature/<short-name>`   | `feature/price-filter`       |
| Bug fix     | `fix/<short-name>`       | `fix/emr-calculation`        |
| Docs        | `docs/<short-name>`      | `docs/data-dictionary`       |
| Pipeline    | `data/<short-name>`      | `data/silver-cleaning`       |

Lowercase, hyphens, no spaces.

### Commit messages

Say what changed, in the present tense:

- ✅ `Add minimum review count filter to sidebar`
- ✅ `Fix revenue estimate using lifetime reviews instead of monthly`
- ❌ `update`, `stuff`, `final version 2`

---

## 4. Pull request rules

**Before opening a PR:**
- [ ] The app still runs locally (`python -m streamlit run app/Home.py`)
- [ ] Tests pass (`python -m pytest`)
- [ ] No secrets, `.env`, API keys or raw data files in the changes
- [ ] New calculations in `src/` have at least one test
- [ ] Any new package is added to `requirements.txt`

**The PR itself:**
- Keep it small: one task, ideally under ~200 lines changed.
- Title says what it does. Description says why, and includes `Closes #<issue number>`.
- Add a screenshot if you changed anything visible in the app.
- Request a reviewer.

**Merging:**
- `main` is protected: nobody pushes to it directly.
- Every PR needs **1 approval** from a teammate who didn't write it.
- The author merges after approval (so they can deal with any last conflicts).
- Delete the branch after merging.

**Reviewing someone's PR:**
- Aim to review within one working day.
- Check: does it do what the issue says, does it run, is the logic in the right place?
- Be specific and kind. Suggest, don't just criticise.
- Approve when it's good enough, not perfect. Small follow-ups can be new issues.

---

## 5. Data rules

- **Never commit raw Inside Airbnb files.** They're large, and GitHub rejects files over 100 MB. Keep them in `data/raw/` (git-ignored) or in Databricks.
- Only small, cleaned outputs go in `data/gold/`, as Parquet.
- When you export new gold files, say in the PR which notebook produced them and the snapshot date.

## 6. Secrets rules

- API keys go in `.env` (local), Databricks secrets, or Streamlit Cloud secrets. **Never in code, notebooks or chat.**
- If a key is ever committed, tell the team immediately, revoke it, and create a new one. Deleting the file is not enough: it stays in Git history.

## 7. Notebooks

- Notebooks conflict badly when two people edit the same one. **Each notebook has one owner** (see the table in `docs/kickoff.md`).
- Need a change in someone else's notebook? Ask them, or put the logic in `src/` where it can be shared.
- Clear large outputs before committing.

## 8. Decisions

Any choice that affects the numbers or the design (assumptions, thresholds, model choice, cities)
gets an entry in `docs/decisions.md`: what we decided, why, and what we considered instead.

---

Stuck? Ask in the team chat. Nobody should be blocked for more than an hour without saying so.

# dbl-domainrunner-governance-failure

**This Domainrunner is a witness, not a participant.**

---

## Purpose

Demonstrate, in a reproducible and concrete way, why AI governance fails even with good data when no deterministic boundary exists — and how DBL prevents that failure.

---

## What This Demo Shows

| Scenario | What Happens | What You See |
|----------|--------------|--------------|
| `happy_path` | INTENT → ALLOW → EXECUTION (success) | Clean audit trail |
| `invalid_request` | INTENT → ALLOW → EXECUTION (error: 400) | Failure correctly classified |
| ~~`policy_deny`~~ | *(Phase 2: requires policy pack)* | — |

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      DOMAINRUNNER                              │
│  • Sends INTENTs to Gateway                                    │
│  • Reads events from Gateway /snapshot                         │
│  • Reads projections from Observer /threads, /signals          │
│  • DOES NOT write to Observer                                  │
│  • DOES NOT make decisions                                     │
│  • DOES NOT store authoritative state                          │
└────────────────────────────────────────────────────────────────┘
         │                                    │
         │ POST /ingress/intent               │ GET /threads (READ ONLY)
         │ GET /snapshot                      │ GET /signals (READ ONLY)
         ▼                                    ▼
┌─────────────────────┐              ┌─────────────────────┐
│    DBL-GATEWAY      │              │    DBL-OBSERVER     │
│   (NORMATIVE)       │              │   (NON_NORMATIVE)   │
│                     │              │                     │
│ • Emits DECISION    │              │ • Projects events   │
│ • Executes (or not) │              │ • Generates signals │
│ • Appends to ledger │              │ • Read-only API     │
└─────────────────────┘              └─────────────────────┘
```

### Communication Rules (HARD)

| From | To | Allowed |
|------|----|---------|
| Domainrunner → Gateway `/ingress/intent` | ✅ Write |
| Domainrunner → Gateway `/snapshot` | ✅ Read |
| Domainrunner → Observer `/threads`, `/signals` | ✅ Read |
| Domainrunner → Observer `/ingest` | ❌ **FORBIDDEN** |

---

## Quick Start (60 seconds)

### Prerequisites

```powershell
# Gateway running on localhost:8010
# Observer running on localhost:8020 (optional, for projections)
```

### Run Demo

```powershell
cd dbl-domainrunner-governance-failure

# Install
pip install -e .

# Run all Phase 1 scenarios
python -m domainrunner
```

### Expected Output

```
┌──────────────────────────────────────────────────────────────────┐
│ Scenario: invalid_request                                        │
│ Thread:   dr-invalid-001                                         │
├──────────────────────────────────────────────────────────────────┤
│ RAW LEDGER (Gateway /snapshot)                                   │
│ ─────────────────────────────────────────────────────────────────│
│  #0  INTENT      turn=t001  message="trigger 400"                │
│  #1  DECISION    result=ALLOW  reason=[allow_all]                │
│  #2  EXECUTION   status=ERROR  code=invalid_request_error        │
├──────────────────────────────────────────────────────────────────┤
│ PROJECTION (Observer /threads/dr-invalid-001)                    │
│ ─────────────────────────────────────────────────────────────────│
│  turns_total: 1                                                  │
│  allow_total: 1                                                  │
│  execution_error_total: 1                                        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Why This Demo Matters

| Without DBL | With DBL |
|-------------|----------|
| "AI failed" (opaque) | DECISION: ALLOW, EXECUTION: ERROR (invalid_request) |
| "AI refused" (opaque) | DECISION: DENY, reason: [policy.X] |
| "AI worked" (opaque) | DECISION: ALLOW, EXECUTION: OK |

**The demo forces the viewer to see:**
- Each event has exactly one kind (INTENT, DECISION, EXECUTION)
- Responsibility is explicit (Gateway decided; Provider failed; Observer reported)
- Failure is classified, not guessed
- Replay is trivial

---

## Constraints (NON_NEGOTIABLE)

1. **No policy logic inside domainrunner**
2. **No decision inference**
3. **No state that claims to be authoritative**
4. **No writes to Observer**

---

## Phases

| Phase | Scenarios | Status |
|-------|-----------|--------|
| **1** | happy_path, invalid_request | ✅ Ready |
| **2** | policy_deny | Requires policy pack |



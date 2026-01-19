2026-01-19T14:31:53+01:00
# Inventory: dbl-domainrunner-governance-failure

## Tree

- .gitignore
- pyproject.toml
- README.md
- src/dbl_domainrunner_governance_failure.egg-info/dependency_links.txt
- src/dbl_domainrunner_governance_failure.egg-info/entry_points.txt
- src/dbl_domainrunner_governance_failure.egg-info/PKG-INFO
- src/dbl_domainrunner_governance_failure.egg-info/requires.txt
- src/dbl_domainrunner_governance_failure.egg-info/SOURCES.txt
- src/dbl_domainrunner_governance_failure.egg-info/top_level.txt
- src/domainrunner/__init__.py
- src/domainrunner/__main__.py
- src/domainrunner/__pycache__/__init__.cpython-311.pyc
- src/domainrunner/__pycache__/__main__.cpython-311.pyc
- src/domainrunner/__pycache__/bridge.cpython-311.pyc
- src/domainrunner/__pycache__/client.cpython-311.pyc
- src/domainrunner/__pycache__/main.cpython-311.pyc
- src/domainrunner/__pycache__/observer_client.cpython-311.pyc
- src/domainrunner/__pycache__/proof_renderer.cpython-311.pyc
- src/domainrunner/__pycache__/visualizer.cpython-311.pyc
- src/domainrunner/bridge.py
- src/domainrunner/client.py
- src/domainrunner/main.py
- src/domainrunner/observer_client.py
- src/domainrunner/proof_renderer.py
- src/domainrunner/scenarios/__init__.py
- src/domainrunner/scenarios/__pycache__/__init__.cpython-311.pyc
- src/domainrunner/scenarios/__pycache__/happy_path.cpython-311.pyc
- src/domainrunner/scenarios/__pycache__/invalid_request.cpython-311.pyc
- src/domainrunner/scenarios/happy_path.py
- src/domainrunner/scenarios/invalid_request.py
- src/domainrunner/visualizer.py

## File Contents

### .gitignore
```
__pycache__/
*.pyc
.venv/
.env

```

### pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "dbl-domainrunner-governance-failure"
version = "0.2.0"
description = "Domainrunner demo: witness AI governance failure and DBL prevention"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }

dependencies = [
  "httpx>=0.27",
  "rich>=13.0",
]

[project.scripts]
domainrunner = "domainrunner.main:main"

[tool.setuptools]
package-dir = { "" = "src" }

[tool.setuptools.packages.find]
where = ["src"]
include = ["domainrunner*"]

```

### README.md
```markdown
# dbl-domainrunner-governance-failure

**This Domainrunner is a witness, not a participant.**

It does not decide.
It does not correct.
It does not infer.

It shows what happened.

---

## Purpose

This repository demonstrates, in a reproducible and concrete way, why AI governance fails even with good data when no deterministic boundary exists — and how DBL makes those failures **explicit, attributable, and auditable**.

This is not a framework.
This is not an agent.
This is a demonstration artifact.

---

## What This Demo Proves

Most AI systems collapse three concerns into one opaque flow:
1. **Decision**
2. **Execution**
3. **Interpretation**

This demo shows them separated and visible.

![Domainrunner Failure Demo](pictures/failure_demo.png)

### What You Are Looking At

The screenshot above shows three layers at once:

**1. RAW LEDGER (Panel A)**
Exact events as recorded by the Gateway.
(INTENT → DECISION → EXECUTION)

**2. PROJECTION (Panel B)**
Aggregated, non-authoritative view from the Observer.
(Eventually consistent by design)

**3. SIGNALS (Panel C)**
NON_NORMATIVE attention markers across the system.
They do not affect decisions.

**Nothing in this view is reconstructed.**
**Nothing is inferred.**
**Everything shown existed as an event.**

---

## Scenarios

| Scenario | Outcome | What becomes explicit |
|----------|---------|-----------------------|
| `happy_path` | DECISION = ALLOW, EXECUTION = OK or ERROR | Governance correctness is independent of execution success |
| `invalid_request` | DECISION = ALLOW, EXECUTION = ERROR (400) | Failure is classified, not guessed |
| `policy_deny` | DECISION = DENY, no execution | Policy refusal is explicit and auditable (Phase 2) |

---

## Architecture (Read This First)

```
┌────────────────────────────────────────────────────────────────┐
│                      DOMAINRUNNER                              │
│                                                                │
│  • Sends INTENTs to Gateway                                    │
│  • Reads raw ledger from Gateway (/snapshot)                   │
│  • Reads projections from Observer (/threads, /signals)        │
│                                                                │
│  • DOES NOT make decisions                                     │
│  • DOES NOT interpret outcomes                                 │
│  • DOES NOT store authoritative state                          │
│  • DOES NOT write to Observer                                  │
└────────────────────────────────────────────────────────────────┘
         │                                    │
         │ POST /ingress/intent               │ GET /threads, /signals
         │ GET /snapshot                      │ (read-only)
         ▼                                    ▼
┌─────────────────────┐              ┌─────────────────────┐
│    DBL-GATEWAY      │              │    DBL-OBSERVER     │
│   (NORMATIVE)       │              │   (NON_NORMATIVE)   │
│                     │              │                     │
│ • Emits DECISION    │              │ • Projects state    │
│ • Executes (or not) │              │ • Aggregates events │
│ • Appends ledger    │              │ • Emits signals     │
└─────────────────────┘              └─────────────────────┘
```

### Communication Rules (HARD)

| From | To | Method | Allowed |
|------|----|--------|---------|
| Domainrunner | Gateway | `/ingress/intent` | ✅ |
| Domainrunner | Gateway | `/snapshot` | ✅ |
| Domainrunner | Observer | `/threads`, `/signals` | ✅ |
| **Domainrunner** | **Observer** | **`/ingest`** | ❌ **FORBIDDEN** |

If the domainrunner ever writes to the Observer, the demo is invalid.

---

## Quick Start (≈ 60 seconds)

### Prerequisites

- **DBL Gateway** running on `http://127.0.0.1:8010`
- **DBL Observer** running on `http://127.0.0.1:8020` (optional but recommended)

### Run

1. **Start Bridge** (Gateway → Observer sync)
   ```powershell
   python -m domainrunner.bridge
   ```

2. **Run Scenarios**
   ```powershell
   python -m domainrunner
   ```

The domainrunner will:
- Submit INTENTs
- Wait for outcomes
- Fetch ledger and projections
- Render results to the terminal

---

## Why This Matters

Without deterministic boundaries, systems report outcomes like:
- "the AI failed"
- "the AI refused"
- "the AI worked"

These statements are meaningless.

With DBL, the same situations become:

| Situation | What DBL shows |
|-----------|----------------|
| Quota exceeded | **DECISION: ALLOW**, **EXECUTION: ERROR** (insufficient_quota) |
| Invalid request | **DECISION: ALLOW**, **EXECUTION: ERROR** (invalid_request) |
| Policy violation | **DECISION: DENY**, reason recorded |
| Success | **DECISION: ALLOW**, **EXECUTION: OK** |

This is not better logging.
This is responsibility separation.

---

## Constraints (NON-NEGOTIABLE)

1. **No policy logic inside the domainrunner**
2. **No decision inference**
3. **No authoritative state**
4. **No writes to Observer**

Violation of any of these invalidates the demo.

---

## Phases

| Phase | Scenarios | Status |
|-------|-----------|--------|
| **1** | `happy_path`, `invalid_request` | ✅ Ready |
| **2** | `policy_deny` | Requires policy pack |

---

## Final Note

This repository does not try to fix failures.
It makes failures legible.

**That is the point.**
```

### src/dbl_domainrunner_governance_failure.egg-info/dependency_links.txt
```


```

### src/dbl_domainrunner_governance_failure.egg-info/entry_points.txt
```
[console_scripts]
domainrunner = domainrunner.main:main

```

### src/dbl_domainrunner_governance_failure.egg-info/PKG-INFO
```
Metadata-Version: 2.4
Name: dbl-domainrunner-governance-failure
Version: 0.1.0
Summary: Domainrunner demo: witness AI governance failure and DBL prevention
License: MIT
Requires-Python: >=3.11
Description-Content-Type: text/markdown
Requires-Dist: httpx>=0.27
Requires-Dist: rich>=13.0

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



```

### src/dbl_domainrunner_governance_failure.egg-info/requires.txt
```
httpx>=0.27
rich>=13.0

```

### src/dbl_domainrunner_governance_failure.egg-info/SOURCES.txt
```
README.md
pyproject.toml
src/dbl_domainrunner_governance_failure.egg-info/PKG-INFO
src/dbl_domainrunner_governance_failure.egg-info/SOURCES.txt
src/dbl_domainrunner_governance_failure.egg-info/dependency_links.txt
src/dbl_domainrunner_governance_failure.egg-info/entry_points.txt
src/dbl_domainrunner_governance_failure.egg-info/requires.txt
src/dbl_domainrunner_governance_failure.egg-info/top_level.txt
src/domainrunner/__init__.py
src/domainrunner/client.py
src/domainrunner/main.py
src/domainrunner/observer_client.py
src/domainrunner/visualizer.py
src/domainrunner/scenarios/__init__.py
src/domainrunner/scenarios/happy_path.py
src/domainrunner/scenarios/invalid_request.py
```

### src/dbl_domainrunner_governance_failure.egg-info/top_level.txt
```
domainrunner

```

### src/domainrunner/__init__.py
```python
"""Domainrunner: Witness, not participant."""

```

### src/domainrunner/__main__.py
```python
from .main import main

if __name__ == "__main__":
    main()

```

### src/domainrunner/__pycache__/__init__.cpython-311.pyc
```
�
    O&ni/   �                   �
   � d Z dS )z'Domainrunner: Witness, not participant.N)�__doc__� �    �PD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\__init__.py�<module>r      s   �� -� -� -� -r   
```

### src/domainrunner/__pycache__/__main__.cpython-311.pyc
```
�
    )niB   �                   �6   � d dl m Z  edk    r e �   �          dS dS )�   )�main�__main__N)r   �__name__� �    �PD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\__main__.py�<module>r	      s9   �� � � � � � ��z����D�F�F�F�F�F� �r   
```

### src/domainrunner/__pycache__/bridge.cpython-311.pyc
```
�
    �)ni�  �                   �l   � d Z ddlZddlZddlZddlmZ  e�   �         Zd� Zedk    r e�   �          dS dS )z�Bridge Service.

Synchronizes Gateway events to Observer.
This simulates the 'infrastructure' that ensures the Observer is up to date.
�    N)�Consolec                  ��  � t          j        dd�  �        �                    d�  �        } t          j        dd�  �        �                    d�  �        }t          �                    d�  �         t          �                    d| � ��  �         t          �                    d|� ��  �         t          �                    �   �          d	}	 	 t          j        | � d��  �        }|j        dk    rt          j	        d�  �         �9|�
                    �   �         }|�                    dg �  �        }|st          j	        d�  �         �zt          j        |� d�|��  �        }|j        dv r<t          |�  �        }||dz   k    r#t          �                    d|� d��  �         |dz
  }n#t          �                    d|j        � d��  �         n# t          $ r
}Y d }~nd }~ww xY wt          j	        d�  �         ��()N�DBL_GATEWAY_URLzhttp://127.0.0.1:8010�/�DBL_OBSERVER_URLzhttp://127.0.0.1:8020z![bold blue]Starting DBL Bridge[/]z
Gateway:  z
Observer: �����Tz/snapshot?limit=500��   �   �eventsz/ingest)�json)r	   ��   z[green]Synced z
 events[/]z[red]Observer connect failed: z[/]�   )�os�getenv�rstrip�console�print�httpx�get�status_code�time�sleepr   �post�len�text�	Exception)�gateway_url�observer_url�last_processed_index�resp�datar   �	new_count�es           �ND:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\bridge.py�
run_bridger%      s�  � ��)�-�/F�G�G�N�N�s�S�S�K��9�/�1H�I�I�P�P�QT�U�U�L��M�M�6�7�7�7��M�M�,�{�,�,�-�-�-��M�M�-�|�-�-�.�.�.��M�M�O�O�O���!�	� �9��@�@�@�A�A�D���3�&�&��
�1������9�9�;�;�D��X�X�h��+�+�F�� ��
�1����� �:��6�6�6�T�B�B�B�D���:�-�-���K�K�	��3�a�7�7�7��=�=�!G�)�!G�!G�!G�H�H�H�*3�a�-�'�����M�t�y�M�M�M�N�N�N���� 	� 	� 	��D�D�D�D�����	���� 	�
�1����C!s    �6F< �9A F< �:BF< �<
G�G�__main__)	�__doc__r   r   r   �rich.consoler   r   r%   �__name__� �    r$   �<module>r,      s}   ��� �
 ���� 	�	�	�	� ����  �  �  �  �  �  �
�'�)�)��,� ,� ,�\ �z����J�L�L�L�L�L� �r+   
```

### src/domainrunner/__pycache__/client.cpython-311.pyc
```
�
    X)ni�  �                  �T   � d Z ddlmZ ddlZddlZddlmZ ddlZ G d� d�  �        ZdS )z�Gateway HTTP client.

This module provides a minimal HTTP client for the DBL Gateway.
It ONLY sends INTENTs and reads snapshots. No decision logic.
�    )�annotationsN)�Anyc                  �D   � e Zd ZdZddd�Zddd	�dd�Zddd�dd�Zdd�ZdS )�GatewayClientz�HTTP client for DBL Gateway.
    
    Responsibilities:
    - POST /ingress/intent (send intent)
    - GET /snapshot (read ledger)
    
    Non-responsibilities:
    - No decision logic
    - No state storage
    - No interpretation
    N�base_url�
str | None�return�Nonec                �d   � |pt          j        dd�  �        �                    d�  �        | _        d S )N�DBL_GATEWAY_URLzhttp://127.0.0.1:8010�/)�os�getenv�rstripr   )�selfr   s     �ND:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\client.py�__init__zGatewayClient.__init__   s/   � �!�Z�R�Y�/@�BY�%Z�%Z�b�b�cf�g�g�����    �domainrunner)�turn_id�actor�	thread_id�str�messager   r   �dict[str, Any]c               �  � t          j        �   �         j        }d|dd|d||p"dt          j        �   �         j        dd�         � �d|id�d	�}t          j        d
��  �        5 }|�                    | j        � d�|��  �        }|�                    �   �          |�                    �   �         cddd�  �         S # 1 swxY w Y   dS )z�Send an intent to the gateway.
        
        Returns the gateway response (usually 202 Accepted with correlation info).
        �   �defaultzchat.messagezturn-N�   r   )�	stream_id�laner   �intent_typer   r   �payload)�interface_version�correlation_idr#   �      $@��timeoutz/ingress/intent)�json)	�uuid�uuid4�hex�httpx�Client�postr   �raise_for_statusr)   )	r   r   r   r   r   r%   �envelope�client�resps	            r   �send_intentzGatewayClient.send_intent   s  � � ����)�� "#�,�&�!��-�&�"�D�&D�d�j�l�l�.>�r��r�.B�&D�&D��w��
� 
�
� 
��  �\�$�'�'�'� 	�6��;�;�$�-�@�@�@�x�;�P�P�D��!�!�#�#�#��9�9�;�;�	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	���� 	� 	� 	� 	� 	� 	s   �!AB5�5B9�<B9�d   )r   �limitr6   �int�list[dict[str, Any]]c               �V  �� d|i}�rd|d<   t          j        d��  �        5 }|�                    | j        � d�|��  �        }|�                    �   �          |�                    �   �         }|�                    dg �  �        }�r�fd	�|D �   �         }|cd
d
d
�  �         S # 1 swxY w Y   d
S )zgFetch raw events from gateway ledger.
        
        Returns list of events in ledger order.
        r6   r   r    r&   r'   z	/snapshot)�params�eventsc                �F   �� g | ]}|�                     d �  �        �k    �|��S )r   )�get)�.0�er   s     �r   �
<listcomp>z.GatewayClient.get_snapshot.<locals>.<listcomp>Y   s/   �� �O�O�O��q�u�u�[�/A�/A�Y�/N�/N�!�/N�/N�/Nr   N�r-   r.   r=   r   r0   r)   )r   r   r6   r:   r2   r3   �datar;   s    `      r   �get_snapshotzGatewayClient.get_snapshotC   s  �� � #*�5�!1��� 	,�"+�F�;���\�$�'�'�'� 
	�6��:�:���9�9�9�&�:�I�I�D��!�!�#�#�#��9�9�;�;�D��X�X�h��+�+�F� � P�O�O�O�O�V�O�O�O���
	� 
	� 
	� 
	� 
	� 
	� 
	� 
	� 
	� 
	� 
	� 
	���� 
	� 
	� 
	� 
	� 
	� 
	s   �A/B�B"�%B"c                ��   � t          j        d��  �        5 }|�                    | j        � d��  �        }|�                    �   �          |�                    �   �         cddd�  �         S # 1 swxY w Y   dS )zFetch gateway status.g      @r'   z/statusNrA   )r   r2   r3   s      r   �
get_statuszGatewayClient.get_status]   s�   � ��\�#�&�&�&� 	�&��:�:���7�7�7�8�8�D��!�!�#�#�#��9�9�;�;�	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	���� 	� 	� 	� 	� 	� 	s   �AA(�(A,�/A,)N)r   r   r	   r
   )
r   r   r   r   r   r   r   r   r	   r   )r   r   r6   r7   r	   r8   )r	   r   )�__name__�
__module__�__qualname__�__doc__r   r4   rC   rE   � r   r   r   r      s�   � � � � � �
� 
�h� h� h� h� h� #�#�"� "� "� "� "� "�N !%��	� � � � � �4� � � � � r   r   )	rI   �
__future__r   r   r*   �typingr   r-   r   rJ   r   r   �<module>rM      s�   ��� �
 #� "� "� "� "� "� 	�	�	�	� ���� � � � � � � ����S� S� S� S� S� S� S� S� S� Sr   
```

### src/domainrunner/__pycache__/main.cpython-311.pyc
```
�
    �0ni�  �                   �   � d Z ddlZddlZddlZddlmZ ddlmZ ddlm	Z	m
Z
 ddlmZmZmZmZ ddlmZ d� Zed	k    r e�   �          dS dS )
zDomainrunner Entrypoint.�    N)�GatewayClient)�ObserverClient)�
happy_path�invalid_request)�render_scenario_result�print_header�print_gateway_unreachable�print_observer_unavailable)�
save_proofc                  �<  � t          �   �          t          �   �         } t          �   �         }	 | �                    �   �          n8# t          $ r+ t          | j        �  �         t          j        d�  �         Y nw xY w|�	                    �   �         st          �   �          t          t          g}t          |�  �        D ]�\  }}|dk    rt          j        d�  �         	 |�                    �   �         }t#          |�  �         t%          |�  �        }|rGddlm}  |�   �         �                    dt,          j        �                    |�  �        � d|� d��  �         ��# t          $ r,}ddlm}  |�   �         �                    �   �          Y d }~��d }~ww xY wt+          d�  �         d S )N�   r   )�ConsoleuD   📄 [dim]Governance Proof generated:[/dim] [bold blue link=file:///�]z[/]z
[dim]Done.[/])r   r   r   �
get_status�	Exceptionr	   �base_url�sys�exit�is_availabler
   r   r   �	enumerate�time�sleep�runr   r   �rich.consoler   �print�os�path�abspath�print_exception)	�gw�obs�	scenarios�i�scenario�result�
proof_filer   �es	            �LD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\main.py�mainr)      s�  � ��N�N�N� 
���B�
�
�
�C��
��������� � � �!�"�+�.�.�.������������� ����� %�"�$�$�$� 	���I�
 !��+�+� (� (���8��q�5�5��J�q�M�M�M�	(��\�\�^�^�F�"�6�*�*�*� $�F�+�+�J�� V�0�0�0�0�0�0���	�	���  !U�gi�gn�gv�gv�  xB�  hC�  hC�  !U�  !U�  FP�  !U�  !U�  !U�  V�  V�  V���� 	(� 	(� 	(�,�,�,�,�,�,��G�I�I�%�%�'�'�'�'�'�'�'�'�����	(���� 
�
�����s*   �A �2A6�5A6�A;E�
F
�"F�F
�__main__)�__doc__r   r   r   �domainrunner.clientr   �domainrunner.observer_clientr   �domainrunner.scenariosr   r   �domainrunner.visualizerr   r   r	   r
   �domainrunner.proof_rendererr   r)   �__name__� �    r(   �<module>r4      s�   �� � � 
�
�
�
� ���� 	�	�	�	� .� -� -� -� -� -� 7� 7� 7� 7� 7� 7� >� >� >� >� >� >� >� >�� � � � � � � � � � � � 3� 2� 2� 2� 2� 2�)� )� )�X �z����D�F�F�F�F�F� �r3   
```

### src/domainrunner/__pycache__/observer_client.cpython-311.pyc
```
�
    �&ni�	  �                  �L   � d Z ddlmZ ddlZddlmZ ddlZ G d� d�  �        ZdS )z�Observer HTTP client.

This module provides a READ-ONLY client for the DBL Observer.
It reads projections and signals. NEVER writes.

INVARIANT: Domainrunner does NOT call /ingest.
�    )�annotationsN)�Anyc                  �D   � e Zd ZdZddd�Zdd	�Zdd�Zdd�Zdd�Zdd�Z	dS )�ObserverClientaI  HTTP client for DBL Observer (READ-ONLY).
    
    Responsibilities:
    - GET /threads (read thread projections)
    - GET /threads/{id} (read single thread)
    - GET /signals (read attention markers)
    - GET /status (read system metrics)
    
    FORBIDDEN:
    - POST /ingest (would make us a participant, not witness)
    N�base_url�
str | None�return�Nonec                �d   � |pt          j        dd�  �        �                    d�  �        | _        d S )N�DBL_OBSERVER_URLzhttp://127.0.0.1:8020�/)�os�getenv�rstripr   )�selfr   s     �WD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\observer_client.py�__init__zObserverClient.__init__   s/   � �!�[�R�Y�/A�CZ�%[�%[�c�c�dg�h�h�����    �list[dict[str, Any]]c                �  � t          j        d��  �        5 }|�                    | j        � d��  �        }|j        dk    r4|�                    �   �         �                    dg �  �        cddd�  �         S g cddd�  �         S # 1 swxY w Y   dS )zFetch all thread summaries.�      @��timeoutz/threads��   �threadsN��httpx�Client�getr   �status_code�json�r   �client�resps      r   �get_threadszObserverClient.get_threads    ��   � ��\�#�&�&�&� 	�&��:�:���8�8�8�9�9�D���3�&�&��y�y�{�{���y�"�5�5�	� 	� 	� 	� 	� 	� 	� 	� �		� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	���� 	� 	� 	� 	� 	� 	�   �AB�3B�B�B�	thread_id�str�dict[str, Any] | Nonec                ��   � t          j        d��  �        5 }|�                    | j        � d|� ��  �        }|j        dk    r |�                    �   �         cddd�  �         S 	 ddd�  �         dS # 1 swxY w Y   dS )z'Fetch single thread summary with turns.r   r   z	/threads/r   Nr   )r   r(   r#   r$   s       r   �
get_threadzObserverClient.get_thread(   s�   � ��\�#�&�&�&� 	�&��:�:���D�D��D�D�E�E�D���3�&�&��y�y�{�{�	� 	� 	� 	� 	� 	� 	� 	� �		� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	���� 	� 	� 	� 	� 	� 	s   �>A/�!A/�/A3�6A3c                �  � t          j        d��  �        5 }|�                    | j        � d��  �        }|j        dk    r4|�                    �   �         �                    dg �  �        cddd�  �         S g cddd�  �         S # 1 swxY w Y   dS )z8Fetch current signals (NON_NORMATIVE attention markers).r   r   z/signalsr   �signalsNr   r"   s      r   �get_signalszObserverClient.get_signals0   r&   r'   c                ��   � t          j        d��  �        5 }|�                    | j        � d��  �        }|j        dk    r |�                    �   �         cddd�  �         S 	 ddd�  �         dS # 1 swxY w Y   dS )zFetch observer status.r   r   z/statusr   Nr   r"   s      r   �
get_statuszObserverClient.get_status8   s�   � ��\�#�&�&�&� 	�&��:�:���7�7�7�8�8�D���3�&�&��y�y�{�{�	� 	� 	� 	� 	� 	� 	� 	� �		� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	���� 	� 	� 	� 	� 	� 	s   �<A-�A-�-A1�4A1�boolc                ��   � 	 t          j        d��  �        5 }|�                    | j        � d��  �        }|j        dk    cddd�  �         S # 1 swxY w Y   dS # t           j        $ r Y dS w xY w)zCheck if observer is reachable.g       @r   z/healthzr   NF)r   r   r   r   r    �RequestErrorr"   s      r   �is_availablezObserverClient.is_available@   s�   � �	���c�*�*�*� /�f��z�z�T�]�"<�"<�"<�=�=���'�3�.�/� /� /� /� /� /� /� /� /� /� /� /���� /� /� /� /� /� /�� �!� 	� 	� 	��5�5�	���s3   �A �(A�A �A�A �A�A �A,�+A,)N)r   r   r	   r
   )r	   r   )r(   r)   r	   r*   )r	   r*   )r	   r2   )
�__name__�
__module__�__qualname__�__doc__r   r%   r,   r/   r1   r5   � r   r   r   r      s�   � � � � � �
� 
�i� i� i� i� i�� � � �� � � �� � � �� � � �� � � � � r   r   )r9   �
__future__r   r   �typingr   r   r   r:   r   r   �<module>r=      sy   ��� � #� "� "� "� "� "� 	�	�	�	� � � � � � � ����7� 7� 7� 7� 7� 7� 7� 7� 7� 7r   
```

### src/domainrunner/__pycache__/proof_renderer.cpython-311.pyc
```
�
    �0nie  �                  �F   � d Z ddlmZ ddlZddlmZ ddlmZ dd
�Zdd�ZdS )z�Governance Proof Renderer.

Generates immutable proof artifacts from ledger traces.
"This document is a formattted projection of existing facts."
�    )�annotationsN)�Any)�datetime�result�dict[str, Any]�return�strc                �H  � | �                     dd�  �        }| �                     dg �  �        }| �                     d| �                     dd�  �        �  �        }d}d}d}d}|D ]�}|�                     d�  �        }	|�                     d	i �  �        }
|	d
k    r-|
�                     dd�  �        }|
�                     dd�  �        }�`|	dk    rMd|
v rEd}|
�                     di �  �        }|�                     d�  �        p|�                     d�  �        pd}��d}d}��|dk    rdnd}|dk    rdnd}|dk    rd}t          j        �   �         �                    �   �         dz   }d|� d|� d|� d|� d|� d|� d|� d|� d �}|r|d!|� d"�z  }|d#z  }n|dk    r|d#z  }|d$z  }t	          |�  �        D ]x\  }}|�                     dd%�  �        }	|�                     d&d%�  �        }|�                     d'|�                     d(d)�  �        �  �        }||� d*|	� d+�z  }|d,|� d"�z  }|d-|� d.�z  }�y|d/z  }|S )0z-Generate Markdown proof from scenario result.�	thread_id�unknown�events�scenario_title�scenario�UNKNOWNN�kind�payload�DECISION�decision�	policy_id�	EXECUTION�error�FAILED�code�message�SUCCESS�ALLOWu   ✅u   🛑u   ❌u   ❓�Zz # GOVERNANCE PROOF

Thread ID: `z`
Generated: `z`
Scenario:  `z�`

Source of Authority: **DBL-GATEWAY** (immutable event ledger)

---

## Verdict

### Decision
- **Authority:** DBL-GATEWAY
- **Result:** � z
- **Policy ID:** `z`

### Execution
- **Status:** �
z- **Error Code:** `z`
z(- **Responsibility:** External Provider
zH
---

## Ledger Evidence

The following events were recorded in order:

�?�turn_id�id�event_idz
sha256:???z. **z**
z   - turn_id: `z   - digest: `z`

aI  ---

## Interpretation Boundary

This document does not interpret outcomes.

It proves:
- that a decision was made
- by whom it was made
- and what happened afterwards

Failures in execution do not invalidate governance correctness.

---

**Generated by:**
`dbl-domainrunner-governance-failure`
**Role:** Witness (non-normative)
)�getr   �utcnow�	isoformat�	enumerate)r   r   r   r   r   r   �exec_status�
exec_error�er   r   �err�decision_icon�	exec_icon�	timestamp�md�ir!   �digests                      �VD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\proof_renderer.py�generate_proofr3      s  � ��
�
�;�	�2�2�I��Z�Z��"�%�%�F��z�z�*�F�J�J�z�9�,M�,M�N�N�H� �H��I��K��J�� "� "���u�u�V�}�}���%�%�	�2�&�&���:����{�{�:�y�9�9�H����K��;�;�I�I��[� � ��'�!�!�&���k�k�'�2�.�.�� �W�W�V�_�_�O����	�0B�0B�O�i�
�
�'��!�
�� &��0�0�E�E�f�M�$�	�1�1���u�I��i����	� ��!�!�+�+�-�-��3�I�
��
� 
� �
� 
� �	
� 
� �
� 
�  (�
� 
� �
� 
�$ �%
� 
�$ '�%
� 
� 
�B�* � :�
�3�J�3�3�3�3��
�9�9���	�	�	!�	!�
�9�9��� � �B� �&�!�!� 	-� 	-���1��u�u�V�S�!�!���%�%�	�3�'�'�� ���t�Q�U�U�:�|�<�<�=�=��
��"�"��"�"�"�"��
�,��,�,�,�,��
�,�v�,�,�,�,���� � �B�& �I�    �
str | Nonec                �*  � 	 t          | �  �        }| �                    dd�  �        }t          j        dd��  �         d|� d�}t	          |dd	�
�  �        5 }|�                    |�  �         ddd�  �         n# 1 swxY w Y   |S # t          $ r Y dS w xY w)z Generate and save proof to file.r   r   �proofsT)�exist_okzproofs/proof_z.md�wzutf-8)�encodingN)r3   r$   �os�makedirs�open�write�	Exception)r   �contentr   �filename�fs        r2   �
save_proofrC   x   s�   � �� ��(�(���J�J�{�I�6�6�	�
��H�t�,�,�,�,�1�9�1�1�1���(�C�'�2�2�2� 	�a��G�G�G����	� 	� 	� 	� 	� 	� 	� 	� 	� 	� 	���� 	� 	� 	� 	� ���� � � ��t�t����s6   �AB �A7�+B �7A;�;B �>A;�?B �
B�B)r   r   r   r	   )r   r   r   r5   )	�__doc__�
__future__r   r;   �typingr   r   r3   rC   � r4   r2   �<module>rH      s�   ��� �
 #� "� "� "� "� "� 	�	�	�	� � � � � � � � � � � � �h� h� h� h�V� � � � � r4   
```

### src/domainrunner/__pycache__/visualizer.cpython-311.pyc
```
�
    .ni%  �                  �   � d Z ddlmZ ddlmZ ddlmZ ddlmZ ddl	m
Z
 ddlmZ  e�   �         Zdd�Zdd�Zdd�Zdd�Zd d�Zd!d�Zd"d�Zd!d�ZdS )#z�Visualizer: Render audit trail and projections.

This module renders data to the terminal using Rich.
It displays, never interprets.
�    )�annotations)�Any)�Console)�Panel)�Table)�Text�result�dict[str, Any]�return�Nonec                �r  � | �                     d| �                     dd�  �        �  �        }| �                     dd�  �        }| �                     dd�  �        }| �                     dg �  �        }| �                     d�  �        }| �                     d	g �  �        }| �                     d
�  �        }t          �                    �   �          t          �                    d|� d��  �         |r t          �                    d|� d�d��  �         t          �                    d|� d��  �         t          �                    �   �          |r0t          �                    t	          d|� d�dd��  �        �  �         dS t          |�  �         |rt          |�  �         t          |�  �         t          �                    �   �          dS )z2Render a complete scenario result with all panels.�scenario_title�scenario�unknown�scenario_subtitle� �	thread_id�events�
projection�signals�errorz[bold blue]Scenario: �[/]z[dim italic]�center)�justifyz[dim]Thread: �[red]�Error�red��title�border_styleN)�get�console�print�ruler   �_render_raw_ledger�_render_projection�_render_signals)r	   r   �subtitler   r   r   r   r   s           �RD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\visualizer.py�render_scenario_resultr*      s�  � � �z�z�*�F�J�J�z�9�,M�,M�N�N�H��z�z�-�r�2�2�H��
�
�;�	�2�2�I��Z�Z��"�%�%�F����L�)�)�J��j�j��B�'�'�G��J�J�w���E� �M�M�O�O�O��L�L�6��6�6�6�7�7�7�� F����2�X�2�2�2�H��E�E�E��M�M�0�)�0�0�0�1�1�1��M�M�O�O�O�� ����e�.�E�.�.�.�g�E�R�R�R�S�S�S��� �v���� � '��:�&�&�&� �G�����M�M�O�O�O�O�O�    r   �list[dict[str, Any]]c           	     ��  � t          ddd��  �        }|�                    ddd��  �         |�                    d	d
d��  �         |�                    dd��  �         |�                    dd��  �         t          | �  �        D �];\  }}|�                    dd�  �        }|�                    dd�  �        dd�         }|dk    rd|� d�}t	          |�  �        }n�|dk    rC|�                    di �  �        �                    dd�  �        }|dk    rd|� d�}nd|� d�}d|� �}nw|dk    rm|�                    di �  �        }	d|	v rJd|� d�}|	�                    di �  �        }
d |
�                    d!|
�                    d"d�  �        �  �        � �}nd|� d�}d#}n|}d$}|�                    t          |�  �        |||�  �         ��=t          �                    t          |d%�&�  �        �  �         dS )'z(Render raw events from gateway snapshot.zRAW LEDGER (Gateway /snapshot)N)r   �   )r   �box�padding�#�dim�   )�style�width�Kind�bold�   zTurn ID�   �r5   �Details)r4   �kind�?�turn_id�INTENTz[cyan]r   �DECISION�payload�decision�ALLOWz[green]r   zresult=�	EXECUTIONr   zERROR: �code�messagez	status=OKr   �blue�r    )
r   �
add_column�	enumerater!   �_extract_intent_details�add_row�strr"   r#   r   )r   �table�i�eventr<   r>   �kind_styled�detailsr	   rA   �errs              r)   r%   r%   7   s=  � ��8�d�F�S�S�S�E�	���S��Q��/�/�/�	���V�6���4�4�4�	���Y�b��)�)�)�	���Y�e��,�,�,��f�%�%� =� =���5��y�y���%�%���)�)�I�s�+�+�C�R�C�0�� �8���,�4�,�,�,�K�-�e�4�4�G�G��Z����Y�Y�y�"�-�-�1�1�*�c�B�B�F��� � �1��1�1�1���/�d�/�/�/��(��(�(�G�G��[� � ��i�i�	�2�.�.�G��'�!�!�/�d�/�/�/���k�k�'�2�.�.��N�C�G�G�F�C�G�G�I�s�4K�4K�$L�$L�N�N���1��1�1�1��%����K��G����c�!�f�f�k�7�G�<�<�<�<��M�M�%��F�3�3�3�4�4�4�4�4r+   rP   rM   c                ��   � | �                     di �  �        }|�                     d|�                     dd�  �        �  �        }t          |�  �        dk    r|dd�         dz   }d	|� d
�S )z+Extract readable details from INTENT event.rA   rF   �
user_inputr   �(   N�%   z...z	message="�")r!   �len)rP   rA   rF   s      r)   rK   rK   `   sj   � ��i�i�	�2�&�&�G��k�k�)�W�[�[��r�%B�%B�C�C�G�
�7�|�|�b����#�2�#�,��&��!�w�!�!�!�!r+   r   c           	     �  � | �                     di �  �        }| �                     dg �  �        }t          �   �         }|�                    d|�                     dd�  �        � d��  �         |�                    d|�                     dd�  �        � d��  �         |�                    d	|�                     d
d�  �        � d��  �         |�                    d|�                     dd�  �        � d��  �         |r%|�                    dt          |�  �        � ��  �         t          �                    t          |dddd��  �        �  �         dS )zRender observer projection.�thread�turnszturns_total: �turns_totalr   �
zallow_total: �allow_totalzdeny_total: �
deny_totalzexecution_error_total: �execution_error_totalz
Turns: z#PROJECTION (Observer /threads/{id})z:[italic dim]Note: Projections are eventually consistent[/]�right�green)r   r(   �subtitle_alignr    N)r!   r   �appendrY   r"   r#   r   )r   r[   r\   �texts       r)   r&   r&   i   sJ  � ��^�^�H�b�)�)�F��N�N�7�B�'�'�E��6�6�D��K�K�@��
�
�=�!� <� <�@�@�@�A�A�A��K�K�@��
�
�=�!� <� <�@�@�@�A�A�A��K�K�>�v�z�z�,��:�:�>�>�>�?�?�?��K�K�T�&�*�*�5L�a�*P�*P�T�T�T�U�U�U�� .����,��E�
�
�,�,�-�-�-��M�M�%��C�!]�'.�%,�	.� .� .� /� /� /� /� /r+   r   c           	     �R  � | s,t           �                    t          ddd��  �        �  �         dS t          ddd��  �        }|�                    dd	�
�  �         |�                    dd�
�  �         |�                    d�  �         | D ]w}|�                    dd�  �        }|dk    rd|� d�}n|dk    rd|� d�}nd|� d�}|�                    ||�                    dd�  �        |�                    dd�  �        �  �         �xt           �                    t          |d��  �        �  �         dS )zRender signals (if any).z|[dim](no signals - insufficient data for thresholds)[/]
[italic dim]Aggregated across system, not limited to this thread.[/]zSIGNALS (NON_NORMATIVE)�yellowr   NzD[italic dim]Aggregated across system, not limited to this thread.[/])r   r/   �caption�Severity�
   r:   �ID�   �Title�severityr=   �criticalz
[red bold]r   �warnz[yellow]z[dim]�idr   rH   )r"   r#   r   r   rI   r!   rL   )r   rN   �signalro   �
sev_styleds        r)   r'   r'   ~   sx  � �� ����e�  \�!:��S� S� S� 	T� 	T� 	T����1�t�  FL�  M�  M�  M�E�	���Z�r��*�*�*�	���T���$�$�$�	���W����� 	S� 	S���:�:�j�#�.�.���z�!�!�3�h�3�3�3�J�J�����1�H�1�1�1�J�J�.��.�.�.�J����j�&�*�*�T�3�"7�"7����G�S�9Q�9Q�R�R�R�R��M�M�%��H�5�5�5�6�6�6�6�6r+   c                 ��   � t           �                    �   �          t           �                    t          j        dd��  �        �  �         t           �                    �   �          dS )zPrint demo header.zm[bold]DBL Domainrunner: Governance Failure Demo[/]
[dim]This domainrunner is a witness, not a participant.[/]rG   rH   N)r"   r#   r   �fit� r+   r)   �print_headerrx   �   sT   � ��M�M�O�O�O��M�M�%�)�	E��� � � � � �
 �M�M�O�O�O�O�Or+   �urlc                �b   � t           �                    t          d| � d�dd��  �        �  �         dS )z Print gateway unreachable error.z[red]Gateway not reachable at z1[/]

Start the gateway first:
[dim]dbl-gateway[/]r   r   r   N)r"   r#   r   )ry   s    r)   �print_gateway_unreachabler{   �   sQ   � ��M�M�%�	�� 	� 	� 	� ��� � � � � � � r+   c                 �:   � t           �                    d�  �         dS )z"Print observer unavailable notice.z5[dim]Observer not available - skipping projections[/]N)r"   r#   rw   r+   r)   �print_observer_unavailabler}   �   s   � ��M�M�I�J�J�J�J�Jr+   N)r	   r
   r   r   )r   r,   r   r   )rP   r
   r   rM   )r   r
   r   r   )r   r,   r   r   )r   r   )ry   rM   r   r   )�__doc__�
__future__r   �typingr   �rich.consoler   �
rich.panelr   �
rich.tabler   �	rich.textr   r"   r*   r%   rK   r&   r'   rx   r{   r}   rw   r+   r)   �<module>r�      s<  ��� �
 #� "� "� "� "� "� � � � � � �  �  �  �  �  �  � � � � � � � � � � � � � � � � � � � �'�)�)��!� !� !� !�H&5� &5� &5� &5�R"� "� "� "�/� /� /� /�*7� 7� 7� 7�4� � � �� � � �K� K� K� K� K� Kr+   
```

### src/domainrunner/bridge.py
```python
"""Bridge Service.

Synchronizes Gateway events to Observer.
This simulates the 'infrastructure' that ensures the Observer is up to date.
"""
import time
import os
import httpx
from rich.console import Console

console = Console()

def run_bridge():
    gateway_url = os.getenv("DBL_GATEWAY_URL", "http://127.0.0.1:8010").rstrip("/")
    observer_url = os.getenv("DBL_OBSERVER_URL", "http://127.0.0.1:8020").rstrip("/")
    
    console.print(f"[bold blue]Starting DBL Bridge[/]")
    console.print(f"Gateway:  {gateway_url}")
    console.print(f"Observer: {observer_url}")
    console.print()
    
    last_processed_index = -1
    
    while True:
        try:
            # 1. Fetch from Gateway
            # We fetch all (limit=500 is a demo simplification)
            # In production, we would use tails/cursors.
            resp = httpx.get(f"{gateway_url}/snapshot?limit=500")
            if resp.status_code != 200:
                time.sleep(1)
                continue
                
            data = resp.json()
            events = data.get("events", [])
            
            if not events:
                time.sleep(1)
                continue
                
            # 2. Push to Observer
            # The observer handles idempotency, so we can just push the snapshot
            resp = httpx.post(f"{observer_url}/ingest", json=data)
            
            if resp.status_code in (200, 202):
                new_count = len(events)
                if new_count > last_processed_index + 1:
                   console.print(f"[green]Synced {new_count} events[/]")
                   last_processed_index = new_count - 1
            else:
                console.print(f"[red]Observer connect failed: {resp.text}[/]")

        except Exception as e:
            # console.print(f"[dim]Sync error: {e}[/]")
            pass
            
        time.sleep(2)

if __name__ == "__main__":
    run_bridge()

```

### src/domainrunner/client.py
```python
"""Gateway HTTP client.

This module provides a minimal HTTP client for the DBL Gateway.
It ONLY sends INTENTs and reads snapshots. No decision logic.
"""
from __future__ import annotations

import os
import uuid
from typing import Any

import httpx


class GatewayClient:
    """HTTP client for DBL Gateway.
    
    Responsibilities:
    - POST /ingress/intent (send intent)
    - GET /snapshot (read ledger)
    
    Non-responsibilities:
    - No decision logic
    - No state storage
    - No interpretation
    """

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("DBL_GATEWAY_URL", "http://127.0.0.1:8010")).rstrip("/")

    def send_intent(
        self,
        *,
        thread_id: str,
        message: str,
        turn_id: str | None = None,
        actor: str = "domainrunner",
    ) -> dict[str, Any]:
        """Send an intent to the gateway.
        
        Returns the gateway response (usually 202 Accepted with correlation info).
        """
        correlation_id = uuid.uuid4().hex
        
        # Proper IntentEnvelope structure required by dbl-gateway
        envelope = {
            "interface_version": 2,
            "correlation_id": correlation_id,
            "payload": {
                "stream_id": "default",
                "lane": "default",
                "actor": actor,
                "intent_type": "chat.message",
                "thread_id": thread_id,
                "turn_id": turn_id or f"turn-{uuid.uuid4().hex[:8]}",
                "payload": {
                    "message": message,
                },
            },
        }
        
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(f"{self.base_url}/ingress/intent", json=envelope)
            resp.raise_for_status()
            return resp.json()

    def get_snapshot(
        self,
        *,
        thread_id: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Fetch raw events from gateway ledger.
        
        Returns list of events in ledger order.
        """
        params: dict[str, Any] = {"limit": limit}
        if thread_id:
            params["stream_id"] = "default"  # Gateway uses stream_id
        
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{self.base_url}/snapshot", params=params)
            resp.raise_for_status()
            data = resp.json()
            events = data.get("events", [])
            
            # Filter by thread_id if specified
            if thread_id:
                events = [e for e in events if e.get("thread_id") == thread_id]
            
            return events

    def get_status(self) -> dict[str, Any]:
        """Fetch gateway status."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/status")
            resp.raise_for_status()
            return resp.json()

```

### src/domainrunner/main.py
```python
"""Domainrunner Entrypoint."""
import sys
import time
import os


from domainrunner.client import GatewayClient
from domainrunner.observer_client import ObserverClient
from domainrunner.scenarios import happy_path, invalid_request
from domainrunner.visualizer import (
    render_scenario_result,
    print_header,
    print_gateway_unreachable,
    print_observer_unavailable,
)
from domainrunner.proof_renderer import save_proof


def main():
    print_header()
    
    # 1. Health Check
    gw = GatewayClient()
    obs = ObserverClient()
    
    try:
        gw.get_status()
    except Exception:
        print_gateway_unreachable(gw.base_url)
        sys.exit(1)
        
    if not obs.is_available():
        print_observer_unavailable()

    # 2. Run Scenarios
    scenarios = [
        happy_path,
        invalid_request,
    ]
    
    for i, scenario in enumerate(scenarios):
        if i > 0:
            time.sleep(1) # Visual separator pause
        
        try:
            result = scenario.run()
            render_scenario_result(result)
            
            # Generate Proof
            proof_file = save_proof(result)
            if proof_file:
                from rich.console import Console
                Console().print(f"📄 [dim]Governance Proof generated:[/dim] [bold blue link=file:///{os.path.abspath(proof_file)}]{proof_file}[/]")
        except Exception as e:
            # Fallback if scenario code crashes
            from rich.console import Console
            Console().print_exception()

    # 3. Done
    print("\n[dim]Done.[/]")


if __name__ == "__main__":
    main()

```

### src/domainrunner/observer_client.py
```python
"""Observer HTTP client.

This module provides a READ-ONLY client for the DBL Observer.
It reads projections and signals. NEVER writes.

INVARIANT: Domainrunner does NOT call /ingest.
"""
from __future__ import annotations

import os
from typing import Any

import httpx


class ObserverClient:
    """HTTP client for DBL Observer (READ-ONLY).
    
    Responsibilities:
    - GET /threads (read thread projections)
    - GET /threads/{id} (read single thread)
    - GET /signals (read attention markers)
    - GET /status (read system metrics)
    
    FORBIDDEN:
    - POST /ingest (would make us a participant, not witness)
    """

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("DBL_OBSERVER_URL", "http://127.0.0.1:8020")).rstrip("/")

    def get_threads(self) -> list[dict[str, Any]]:
        """Fetch all thread summaries."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/threads")
            if resp.status_code == 200:
                return resp.json().get("threads", [])
            return []

    def get_thread(self, thread_id: str) -> dict[str, Any] | None:
        """Fetch single thread summary with turns."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/threads/{thread_id}")
            if resp.status_code == 200:
                return resp.json()
            return None

    def get_signals(self) -> list[dict[str, Any]]:
        """Fetch current signals (NON_NORMATIVE attention markers)."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/signals")
            if resp.status_code == 200:
                return resp.json().get("signals", [])
            return []

    def get_status(self) -> dict[str, Any] | None:
        """Fetch observer status."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/status")
            if resp.status_code == 200:
                return resp.json()
            return None

    def is_available(self) -> bool:
        """Check if observer is reachable."""
        try:
            with httpx.Client(timeout=2.0) as client:
                resp = client.get(f"{self.base_url}/healthz")
                return resp.status_code == 200
        except httpx.RequestError:
            return False

```

### src/domainrunner/proof_renderer.py
```python
"""Governance Proof Renderer.

Generates immutable proof artifacts from ledger traces.
"This document is a formattted projection of existing facts."
"""
from __future__ import annotations

import os
from typing import Any
from datetime import datetime


def generate_proof(result: dict[str, Any]) -> str:
    """Generate Markdown proof from scenario result."""
    thread_id = result.get("thread_id", "unknown")
    events = result.get("events", [])
    scenario = result.get("scenario_title", result.get("scenario", "unknown"))
    
    # 1. Extract Verdict Data from Events (Witness Logic)
    decision = "UNKNOWN"
    policy_id = "unknown"
    exec_status = "UNKNOWN"
    exec_error = None
    
    for e in events:
        kind = e.get("kind")
        payload = e.get("payload", {})
        
        if kind == "DECISION":
            decision = payload.get("decision", "UNKNOWN")
            policy_id = payload.get("policy_id", "unknown")
            
        elif kind == "EXECUTION":
            if "error" in payload:
                exec_status = "FAILED"
                err = payload.get("error", {})
                exec_error = err.get("code") or err.get("message") or "unknown"
            else:
                exec_status = "SUCCESS"
                exec_error = None

    # Icon Logic
    decision_icon = "✅" if decision == "ALLOW" else "🛑"
    exec_icon = "✅" if exec_status == "SUCCESS" else "❌"
    if exec_status == "UNKNOWN":
        exec_icon = "❓"

    # 2. Build Markdown
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    md = f"""# GOVERNANCE PROOF

Thread ID: `{thread_id}`
Generated: `{timestamp}`
Scenario:  `{scenario}`

Source of Authority: **DBL-GATEWAY** (immutable event ledger)

---

## Verdict

### Decision
- **Authority:** DBL-GATEWAY
- **Result:** {decision_icon} {decision}
- **Policy ID:** `{policy_id}`

### Execution
- **Status:** {exec_icon} {exec_status}
"""

    if exec_error:
        md += f"- **Error Code:** `{exec_error}`\n"
        md += "- **Responsibility:** External Provider\n"
    elif exec_status == "SUCCESS":
        md += "- **Responsibility:** External Provider\n"
    
    md += """
---

## Ledger Evidence

The following events were recorded in order:

"""

    for i, e in enumerate(events):
        kind = e.get("kind", "?")
        turn_id = e.get("turn_id", "?")
        # Digest simulation (real gateway has digest, here we simulate or extract if available)
        # Gateway snapshot V2 usually has event_id or digest.
        digest = e.get("id", e.get("event_id", "sha256:???"))
        
        md += f"{i}. **{kind}**\n"
        md += f"   - turn_id: `{turn_id}`\n"
        md += f"   - digest: `{digest}`\n\n"

    md += """---

## Interpretation Boundary

This document does not interpret outcomes.

It proves:
- that a decision was made
- by whom it was made
- and what happened afterwards

Failures in execution do not invalidate governance correctness.

---

**Generated by:**
`dbl-domainrunner-governance-failure`
**Role:** Witness (non-normative)
"""
    return md


def save_proof(result: dict[str, Any]) -> str | None:
    """Generate and save proof to file."""
    try:
        content = generate_proof(result)
        thread_id = result.get("thread_id", "unknown")
        
        os.makedirs("proofs", exist_ok=True)
        filename = f"proofs/proof_{thread_id}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
        return filename
    except Exception:
        return None

```

### src/domainrunner/scenarios/__init__.py
```python
"""Scenarios package."""

```

### src/domainrunner/scenarios/__pycache__/__init__.cpython-311.pyc
```
�
    U&ni   �                   �
   � d Z dS )zScenarios package.N)�__doc__� �    �ZD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\scenarios\__init__.py�<module>r      s   �� � � � r   
```

### src/domainrunner/scenarios/__pycache__/happy_path.cpython-311.pyc
```
�
    �-ni�  �                   �>   � d Z ddlZddlZddlmZ ddlmZ defd�ZdS )z�Happy Path Scenario.

Steps:
1. Send valid INTENT
2. Wait for processing
3. Fetch results

Expected:
INTENT -> DECISION(ALLOW) -> EXECUTION(OK)
�    N)�GatewayClient)�ObserverClient�returnc                  �j  � t          �   �         } t          �   �         }dt          j        �   �         j        d d�         � �}| �                    |dd��  �         t          j        d�  �         | �                    |d��  �        }|�	                    |�  �        }|�
                    �   �         }d	d
||||d�S )Nz	dr-happy-�   z"Hello from domainrunner happy pathzdomainrunner-happy)�	thread_id�message�actorg      �?i�  )r   �limit�
happy_pathz6Policy decision: ALLOW  |  Execution outcome: VARIABLE)�scenario_title�scenario_subtitler   �events�
projection�signals)r   r   �uuid�uuid4�hex�send_intent�time�sleep�get_snapshot�
get_thread�get_signals)�gw�obsr   �
raw_eventsr   r   s         �\D:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\scenarios\happy_path.py�runr      s�   � �	���B�
�
�
�C�2�D�J�L�L�,�R�a�R�0�2�2�I� �N�N��4�"� � � � � 	�J�s�O�O�O� ���9�C��@�@�J����	�*�*�J��o�o���G� '�U��� ��� � �    )	�__doc__r   r   �domainrunner.clientr   �domainrunner.observer_clientr   �dictr   � r    r   �<module>r&      sl   ��	� 	� ���� ���� -� -� -� -� -� -� 7� 7� 7� 7� 7� 7��T� � � � � � r    
```

### src/domainrunner/scenarios/__pycache__/invalid_request.cpython-311.pyc
```
�
    �-niB  �                   �>   � d Z ddlZddlZddlmZ ddlmZ defd�ZdS )z�Invalid Request Scenario.

Steps:
1. Send INTENT that provokes Provider Error (e.g. empty message)
2. Wait for processing
3. Fetch results

Expected:
INTENT -> DECISION(ALLOW) -> EXECUTION(ERROR)
�    N)�GatewayClient)�ObserverClient�returnc                  ��  � t          �   �         } t          �   �         }dt          j        �   �         j        d d�         � �}	 | �                    |dd��  �         n0# t          $ r#}d|dt          |�  �        � �g d g d�cY d }~S d }~ww xY wt          j	        d	�  �         | �
                    |d
��  �        }|�                    |�  �        }|�                    �   �         }dd||||d�S )Nzdr-invalid-�   � zdomainrunner-invalid)�	thread_id�message�actor�invalid_requestzIngress rejected request: )�scenarior	   �error�events�
projection�signalsg      �?i�  )r	   �limitz3Policy decision: ALLOW  |  Execution outcome: ERROR)�scenario_title�scenario_subtitler	   r   r   r   )r   r   �uuid�uuid4�hex�send_intent�	Exception�str�time�sleep�get_snapshot�
get_thread�get_signals)�gw�obsr	   �e�
raw_eventsr   r   s          �aD:\DEV\projects\dbl-domainrunner-governance-failure\src\domainrunner\scenarios\invalid_request.py�runr%      s7  � �	���B�
�
�
�C�4�d�j�l�l�.�r��r�2�4�4�I�

�
�����(� 	� 	
� 	
� 	
� 	
��
 � 
� 
� 
�
 *�"�:�#�a�&�&�:�:����
� 
� 	
� 	
� 	
� 	
� 	
� 	
�����	
���� 	�J�s�O�O�O� ���9�C��@�@�J����	�*�*�J��o�o���G� ,�R��� ��� � s   �A �
B�$B�<B�B)	�__doc__r   r   �domainrunner.clientr   �domainrunner.observer_clientr   �dictr%   � �    r$   �<module>r,      sl   ��	� 	� ���� ���� -� -� -� -� -� -� 7� 7� 7� 7� 7� 7�+�T� +� +� +� +� +� +r+   
```

### src/domainrunner/scenarios/happy_path.py
```python
"""Happy Path Scenario.

Steps:
1. Send valid INTENT
2. Wait for processing
3. Fetch results

Expected:
INTENT -> DECISION(ALLOW) -> EXECUTION(OK)
"""
import time
import uuid

from domainrunner.client import GatewayClient
from domainrunner.observer_client import ObserverClient


def run() -> dict:
    gw = GatewayClient()
    obs = ObserverClient()
    
    thread_id = f"dr-happy-{uuid.uuid4().hex[:6]}"
    
    # 1. Send intent
    gw.send_intent(
        thread_id=thread_id,
        message="Hello from domainrunner happy path",
        actor="domainrunner-happy",
    )
    
    # 2. Wait for processing (Gateway is async)
    time.sleep(1.0)
    
    # 3. Fetch results
    # Pass 'limit=500' to ensure we get our events if ledger is busy
    raw_events = gw.get_snapshot(thread_id=thread_id, limit=500)
    
    projection = obs.get_thread(thread_id)
    signals = obs.get_signals()
    
    return {
        "scenario_title": "happy_path",
        "scenario_subtitle": "Policy decision: ALLOW  |  Execution outcome: VARIABLE",
        "thread_id": thread_id,
        "events": raw_events,
        "projection": projection,
        "signals": signals,
    }

```

### src/domainrunner/scenarios/invalid_request.py
```python
"""Invalid Request Scenario.

Steps:
1. Send INTENT that provokes Provider Error (e.g. empty message)
2. Wait for processing
3. Fetch results

Expected:
INTENT -> DECISION(ALLOW) -> EXECUTION(ERROR)
"""
import time
import uuid

from domainrunner.client import GatewayClient
from domainrunner.observer_client import ObserverClient


def run() -> dict:
    gw = GatewayClient()
    obs = ObserverClient()
    
    thread_id = f"dr-invalid-{uuid.uuid4().hex[:6]}"
    
    # 1. Send intent with empty message to provoke Provider 400
    # Note: Gateway accepts it (Ingress), Policy allows it (if allow_all),
    # but Provider should reject empty prompts.
    try:
        gw.send_intent(
            thread_id=thread_id,
            message="",  # Empty message usually provokes 400
            actor="domainrunner-invalid",
        )
    except Exception as e:
        # If Ingress rejects it immediately, we might not get a ledger entry.
        # This demonstrates "Ingress Rejection" which is also valid governance,
        # but less interesting for the ledger demo.
        return {
            "scenario": "invalid_request",
            "thread_id": thread_id,
            "error": f"Ingress rejected request: {str(e)}",
            "events": [],
            "projection": None,
            "signals": [],
        }
    
    # 2. Wait
    time.sleep(1.0)
    
    # 3. Fetch
    raw_events = gw.get_snapshot(thread_id=thread_id, limit=500)
    projection = obs.get_thread(thread_id)
    signals = obs.get_signals()
    
    return {
        "scenario_title": "invalid_request",
        "scenario_subtitle": "Policy decision: ALLOW  |  Execution outcome: ERROR",
        "thread_id": thread_id,
        "events": raw_events,
        "projection": projection,
        "signals": signals,
    }

```

### src/domainrunner/visualizer.py
```python
"""Visualizer: Render audit trail and projections.

This module renders data to the terminal using Rich.
It displays, never interprets.
"""
from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


def render_scenario_result(result: dict[str, Any]) -> None:
    """Render a complete scenario result with all panels."""
    # Support both old and new field names
    scenario = result.get("scenario_title", result.get("scenario", "unknown"))
    subtitle = result.get("scenario_subtitle", "")
    thread_id = result.get("thread_id", "unknown")
    events = result.get("events", [])
    projection = result.get("projection")
    signals = result.get("signals", [])
    error = result.get("error")

    # Header
    console.print()
    console.rule(f"[bold blue]Scenario: {scenario}[/]")
    if subtitle:
        console.print(f"[dim italic]{subtitle}[/]", justify="center")
    console.print(f"[dim]Thread: {thread_id}[/]")
    console.print()

    if error:
        console.print(Panel(f"[red]{error}[/]", title="Error", border_style="red"))
        return

    # Panel A: Raw Ledger
    _render_raw_ledger(events)

    # Panel B: Projection (if available)
    if projection:
        _render_projection(projection)

    # Panel C: Signals (if any)
    _render_signals(signals)

    console.print()


def _render_raw_ledger(events: list[dict[str, Any]]) -> None:
    """Render raw events from gateway snapshot."""
    table = Table(title="RAW LEDGER (Gateway /snapshot)", box=None, padding=(0, 1))
    table.add_column("#", style="dim", width=4)
    table.add_column("Kind", style="bold", width=12)
    table.add_column("Turn ID", width=20)
    table.add_column("Details", style="dim")

    for i, event in enumerate(events):
        kind = event.get("kind", "?")
        turn_id = event.get("turn_id", "?")[:20]
        
        # Kind-specific styling
        if kind == "INTENT":
            kind_styled = f"[cyan]{kind}[/]"
            details = _extract_intent_details(event)
        elif kind == "DECISION":
            result = event.get("payload", {}).get("decision", "?")
            if result == "ALLOW":
                kind_styled = f"[green]{kind}[/]"
            else:
                kind_styled = f"[red]{kind}[/]"
            details = f"result={result}"
        elif kind == "EXECUTION":
            payload = event.get("payload", {})
            if "error" in payload:
                kind_styled = f"[red]{kind}[/]"
                err = payload.get("error", {})
                details = f"ERROR: {err.get('code', err.get('message', '?'))}"
            else:
                kind_styled = f"[green]{kind}[/]"
                details = "status=OK"
        else:
            kind_styled = kind
            details = ""
        
        table.add_row(str(i), kind_styled, turn_id, details)

    console.print(Panel(table, border_style="blue"))


def _extract_intent_details(event: dict[str, Any]) -> str:
    """Extract readable details from INTENT event."""
    payload = event.get("payload", {})
    message = payload.get("message", payload.get("user_input", ""))
    if len(message) > 40:
        message = message[:37] + "..."
    return f'message="{message}"'


def _render_projection(projection: dict[str, Any]) -> None:
    """Render observer projection."""
    thread = projection.get("thread", {})
    turns = projection.get("turns", [])

    text = Text()
    text.append(f"turns_total: {thread.get('turns_total', 0)}\n")
    text.append(f"allow_total: {thread.get('allow_total', 0)}\n")
    text.append(f"deny_total: {thread.get('deny_total', 0)}\n")
    text.append(f"execution_error_total: {thread.get('execution_error_total', 0)}\n")
    
    if turns:
        text.append(f"\nTurns: {len(turns)}")

    console.print(Panel(text, 
                        title="PROJECTION (Observer /threads/{id})", 
                        subtitle="[italic dim]Note: Projections are eventually consistent[/]",
                        subtitle_align="right",
                        border_style="green"))


def _render_signals(signals: list[dict[str, Any]]) -> None:
    """Render signals (if any)."""
    if not signals:
        console.print(Panel("[dim](no signals - insufficient data for thresholds)[/]\n[italic dim]Aggregated across system, not limited to this thread.[/]", 
                           title="SIGNALS (NON_NORMATIVE)", border_style="yellow"))
        return

    table = Table(title="SIGNALS (NON_NORMATIVE)", box=None, caption="[italic dim]Aggregated across system, not limited to this thread.[/]")
    table.add_column("Severity", width=10)
    table.add_column("ID", width=30)
    table.add_column("Title")

    for signal in signals:
        severity = signal.get("severity", "?")
        if severity == "critical":
            sev_styled = f"[red bold]{severity}[/]"
        elif severity == "warn":
            sev_styled = f"[yellow]{severity}[/]"
        else:
            sev_styled = f"[dim]{severity}[/]"
        
        table.add_row(sev_styled, signal.get("id", "?"), signal.get("title", "?"))

    console.print(Panel(table, border_style="yellow"))


def print_header() -> None:
    """Print demo header."""
    console.print()
    console.print(Panel.fit(
        "[bold]DBL Domainrunner: Governance Failure Demo[/]\n"
        "[dim]This domainrunner is a witness, not a participant.[/]",
        border_style="blue",
    ))
    console.print()


def print_gateway_unreachable(url: str) -> None:
    """Print gateway unreachable error."""
    console.print(Panel(
        f"[red]Gateway not reachable at {url}[/]\n\n"
        "Start the gateway first:\n"
        "[dim]dbl-gateway[/]",
        title="Error",
        border_style="red",
    ))


def print_observer_unavailable() -> None:
    """Print observer unavailable notice."""
    console.print("[dim]Observer not available - skipping projections[/]")

```

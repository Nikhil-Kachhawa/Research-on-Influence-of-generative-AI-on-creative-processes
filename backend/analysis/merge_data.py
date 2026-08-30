import requests
import pandas as pd

from pathlib import Path
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

SOSCI_URL = (
    "https://sosci.rlp.net/nikhil/"
    "?act=Z2pMP9Jc8mLsvLw3TlyjhpVl"
)

DJANGO_BASE_URL = "http://127.0.0.1:8000/api"

# =====================================================
# LABEL MAPPINGS
# =====================================================

PR01_MAP = {
    1: "Computer Science",
    2: "Web and Data Science",
    3: "E-government",
    4: "Other",
}

PR02_MAP = {
    1: "Never",
    2: "Rarely",
    3: "Sometimes",
    4: "Often",
    5: "Very Often",
}

PR03_MAP = {
    1: "Not familiar at all",
    2: "Slightly familiar",
    3: "Moderately familiar",
    4: "Familiar",
    5: "Very familiar",
}

PO01_MAP = {
    1: "Very Negative",
    2: "Negative",
    3: "Neutral",
    4: "Positive",
    5: "Very Positive",
}

# =====================================================
# FETCH DATA
# =====================================================

print("Fetching SoSci data...")
sosci_data = requests.get(SOSCI_URL).json()

print("Fetching chat export...")
chat_data = requests.get(
    f"{DJANGO_BASE_URL}/chat-export/"
).json()

print("Fetching experiment export...")
experiment_data = requests.get(
    f"{DJANGO_BASE_URL}/experiment-export/"
).json()

# =====================================================
# BUILD SOSCI DATASET
# =====================================================

participants = {}

for record in sosci_data["data"].values():

    participant_id = record.get("REF")

    if not participant_id:
        continue

    if participant_id not in participants:
        participants[participant_id] = {
            "participant_id": participant_id
        }

    questionnaire = record.get("QUESTNNR")

    if questionnaire == "base":

        participants[participant_id]["PR01"] = record.get("PR01")
        participants[participant_id]["PR02"] = record.get("PR02")
        participants[participant_id]["PR03"] = record.get("PR03")

        participants[participant_id]["pre_time_seconds"] = (
            record.get("TIME_SUM")
        )

    elif questionnaire == "qnr2":

        participants[participant_id]["PO01"] = record.get("PO01")

        participants[participant_id]["post_time_seconds"] = (
            record.get("TIME_SUM")
        )

sosci_df = pd.DataFrame(
    participants.values()
)

# =====================================================
# HUMAN READABLE LABELS
# =====================================================

if not sosci_df.empty:

    sosci_df["field_of_study"] = (
        sosci_df["PR01"].map(PR01_MAP)
    )

    sosci_df["ai_usage"] = (
        sosci_df["PR02"].map(PR02_MAP)
    )

    sosci_df["research_familiarity"] = (
        sosci_df["PR03"].map(PR03_MAP)
    )

    sosci_df["experience_rating"] = (
        sosci_df["PO01"].map(PO01_MAP)
    )

# =====================================================
# DJANGO DATAFRAMES
# =====================================================

chat_df = pd.DataFrame(chat_data)

experiment_df = pd.DataFrame(
    experiment_data
)

# =====================================================
# PARTICIPANT DATASET
# =====================================================

participant_df = experiment_df.merge(
    sosci_df,
    on="participant_id",
    how="left"
)

# =====================================================
# MESSAGE DATASET
# =====================================================

message_df = chat_df.merge(
    participant_df,
    on="participant_id",
    how="left"
)

# =====================================================
# OUTPUT DIRECTORY
# =====================================================

OUTPUT_DIR = Path("analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

participant_file = (
    OUTPUT_DIR /
    f"participant_dataset_{timestamp}.csv"
)

message_file = (
    OUTPUT_DIR /
    f"message_dataset_{timestamp}.csv"
)

participant_latest = (
    OUTPUT_DIR /
    "participant_dataset_latest.csv"
)

message_latest = (
    OUTPUT_DIR /
    "message_dataset_latest.csv"
)

# =====================================================
# EXPORT
# =====================================================

participant_df.to_csv(
    participant_file,
    index=False
)

message_df.to_csv(
    message_file,
    index=False
)

participant_df.to_csv(
    participant_latest,
    index=False
)

message_df.to_csv(
    message_latest,
    index=False
)

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("EXPORT COMPLETED")
print("=" * 60)

print(
    f"Participants: {len(participant_df)}"
)

print(
    f"Messages: {len(message_df)}"
)

print()

print(
    f"Saved: {participant_file}"
)

print(
    f"Saved: {message_file}"
)

print()

print(
    f"Updated: {participant_latest}"
)

print(
    f"Updated: {message_latest}"
)
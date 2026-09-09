"""
Runs the full pipeline: 
load warnings -> keep latest per event -> rank by danger
"""

from src.cdm_loader import load_cdms

from src.event_summarizer import summarize_events

from src.triage_queue import AlertQueue
from src.config import DATA_PATH, OUTPUT_DIR, TOP_N
from src.priority_analysis import add_priority_score
from src.report_writer import write_reports

def main():

  df = load_cdms(DATA_PATH)

  final_rows = summarize_events(df)
  scored_events = add_priority_score(final_rows)
  write_reports(df, scored_events, OUTPUT_DIR)

  queue = AlertQueue()

  for _, row in scored_events[scored_events["priority"].isin(["HIGH", "MEDIUM"])].iterrows():

    queue.add(row["event_id"], row["priority_score"])

  high_count = (scored_events["priority"] == "HIGH").sum()
  medium_count = (scored_events["priority"] == "MEDIUM").sum()

  print(f"Warning rows: {len(df)}, Events: {len(scored_events)}")
  print(f"High priority: {high_count}, Medium priority: {medium_count}")
  print(f"Reports written to: {OUTPUT_DIR}")

  print(f"Top {TOP_N} events for human review:")

  for event_id, risk in queue.most_urgent(TOP_N):

    print(f"  event {event_id}: risk={risk:.2f}")

if __name__ == "__main__":
  main()
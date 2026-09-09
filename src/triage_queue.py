"""Keep scored events ordered for a small human-review list."""

import bisect

class AlertQueue:
  """A simple descending queue using binary search for insertion."""

  def __init__(self):
    self._scores = []
    self._event_ids = []

  def add(self, event_id, score: float):
    """Insert one event so the largest priority score comes first."""
    index = bisect.bisect_left(self._scores, -score)
    self._scores.insert(index, -score)
    self._event_ids.insert(index, event_id)

  def most_urgent(self, n: int = 5):
    """Return up to n event IDs and their scores."""
    return list(zip(self._event_ids[:n], [-score for score in self._scores[:n]]))
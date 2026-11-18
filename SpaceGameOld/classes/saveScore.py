import os


class ScoreManager:
    """Load, save and sort player scores in the scores.txt file."""

    def __init__(self, file_path=None):
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = file_path or os.path.join(project_folder, "scores.txt")
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Read saved scores and ignore lines with an invalid format."""
        self.scores = []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().rsplit(",", 1)
                    if len(parts) != 2:
                        continue
                    try:
                        name = parts[0].strip() or "Player"
                        score = int(parts[1])
                    except ValueError:
                        continue
                    self.scores.append((name, score))
        except FileNotFoundError:
            pass

        self.scores.sort(key=lambda item: item[1], reverse=True)

    def save_score(self, name, score):
        """Add a score and write the complete sorted list to the file."""
        safe_name = name.replace(",", " ").replace("\n", " ").strip()[:15]
        if not safe_name:
            safe_name = "Player"

        self.scores.append((safe_name, int(score)))
        self.scores.sort(key=lambda item: item[1], reverse=True)

        folder = os.path.dirname(self.file_path)
        os.makedirs(folder, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            for player_name, points in self.scores:
                file.write(f"{player_name},{points}\n")

    def get_top_scores(self):
        """Return the five highest scores."""
        return self.scores[:5]


# Keep the old class name available for existing imports.
SaveScore = ScoreManager

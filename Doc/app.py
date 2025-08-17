from platform import system
import re
from collections import defaultdict
import os

def sort_changelog(input_file="CHANGELOG.md", output_file="CHANGELOG_sorted.md"):
    categories = {
        "feat": "✨ Features",
        "fix": "🐛 Fixes",
        "chore": "🧹 Chores",
        "refactor": "♻️ Refactoring",
        "docs": "📖 Documentation",
        "test": "✅ Tests",
        "other": "🔧 Other"
    }

    grouped = defaultdict(list)

    # Lire les commits
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            match = re.match(r"-\s*(\w+)", line)
            if match:
                commit_type = match.group(1).lower()
                if commit_type in categories:
                    grouped[commit_type].append(line)
                else:
                    grouped["other"].append(line)

    # Écrire le changelog trié
    with open(output_file, "w", encoding="utf-8") as f:
        for key, title in categories.items():
            if grouped[key]:
                f.write(f"## {title}\n\n")
                f.write("\n".join(grouped[key]) + "\n\n")

    print(f"✅ Changelog trié dans {output_file}")


if __name__ == "__main__":
    sort_changelog()
    os.system("cp CHANGELOG_sorted.md CHANGELOG.md")
    os.system("rm CHANGELOG_sorted.md")
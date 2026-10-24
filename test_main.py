import main


def use_temp_file(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "DATA_FILE", str(tmp_path / "data.json"))


def test_set_goals_and_reload(monkeypatch, tmp_path):
    use_temp_file(monkeypatch, tmp_path)
    assert main.main(["goals", "--set", "Finish labs", "Push 2 projects", "Strong grades"]) == 0
    assert main.load()["goals"] == ["Finish labs", "Push 2 projects", "Strong grades"]


def test_add_review_saved(monkeypatch, tmp_path):
    use_temp_file(monkeypatch, tmp_path)
    assert main.main(["add", "--finished", "CLI lab", "--proud", "Fixed bug", "--next-week", "Quiz"]) == 0
    assert main.load()["reviews"][0]["proud"] == "Fixed bug"


def test_empty_field_rejected(monkeypatch, tmp_path):
    use_temp_file(monkeypatch, tmp_path)
    assert main.main(["add", "--finished", " ", "--proud", "x", "--next-week", "y"]) == 1
    assert main.load()["reviews"] == []


def test_bad_file_starts_empty(monkeypatch, tmp_path):
    use_temp_file(monkeypatch, tmp_path)
    with open(main.DATA_FILE, "w") as file:
        file.write("{ not json")
    assert main.load() == {"goals": [], "reviews": []}

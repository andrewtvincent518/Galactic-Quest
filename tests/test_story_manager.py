from galactic_quest.game.story import HistoryEntry, StoryManager


def test_story_manager_loads_default_story():
    manager = StoryManager()
    start_scene = manager.get_current_scene()

    assert start_scene.choices
    assert manager.current_scene == "start"
    assert not list(manager.iter_history())


def test_make_choice_updates_history_and_scene():
    manager = StoryManager()
    start_scene = manager.get_current_scene()

    assert manager.make_choice(0)
    assert manager.current_scene == start_scene.choices[0].next_scene

    history = list(manager.iter_history())
    assert len(history) == 1
    entry = history[0]
    assert isinstance(entry, HistoryEntry)
    assert entry.scene_id == "start"
    assert entry.choice_index == 0


def test_go_back_restores_previous_scene():
    manager = StoryManager()

    manager.make_choice(0)
    assert manager.go_back()
    assert manager.current_scene == "start"
    assert not manager.can_go_back()
    assert list(manager.iter_history()) == []


def test_jump_to_scene_truncates_history():
    manager = StoryManager()
    manager.make_choice(0)
    # Jumping to same scene should keep history intact
    next_scene = manager.current_scene
    manager.jump_to_scene(next_scene)
    assert manager.current_scene == next_scene
    assert manager.can_go_back()

    # Jumping to start clears history
    manager.jump_to_scene("start")
    assert manager.current_scene == "start"
    assert not manager.can_go_back()


# VAM Lab — Electron–Swirl GUI

A plug-in GUI (Tkinter + Matplotlib) with a splash screen and auto-discovery of tests.

## How to run
```bash
python vam_lab_gui.py
```
> Drop new test files in this same folder named `vamtest_*.py` (or `*_vamtest.py`).
> Each file should define `TEST_CLASS` deriving from `BaseTest` (see `test_base.py`).

## Included tests
- **Electron–Swirl: Single-Mode (JC)** — Jaynes–Cummings + Lindblad.
- **Two-Mode Swirl with Chirality** — Adds a second near-degenerate mode with complex mixing. Set `sweep_delta=true` to plot a coherence bump vs detuning.

## Writing a new test
Create `vamtest_myidea.py`:

```python
from test_base import BaseTest

class MyTest(BaseTest):
    name = "My Experiment"
    description = "One line about it."
    def default_params(self):
        return {"foo": 1.0, "bar": 2}
    def run(self, params, figure):
        ax = figure.gca()
        ax.plot([0,1,2],[0,1,0])
        ax.set_title("Hello")
        return {"ok": True}

TEST_CLASS = MyTest
```

Restart the app; it will appear in the list.

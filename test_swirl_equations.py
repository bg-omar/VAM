import importlib
import inspect

import generate_equation_class as gen
import swirl_equations


def test_equations_match():
    expected = gen.extract_equations()
    swirl = swirl_equations.SwirlEquations()
    for i, eq in enumerate(expected, 1):
        func = getattr(swirl, f"equation_{i}")
        assert func() == eq
        assert func(as_latex=False) == gen.latex_to_python(eq)


def test_equation_count():
    expected = gen.extract_equations()
    methods = [name for name, _ in inspect.getmembers(swirl_equations.SwirlEquations, predicate=inspect.isfunction) if name.startswith("equation_")]
    assert len(methods) == len(expected)

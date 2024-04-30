from pylint.lint import Run

results = Run(["assignment6.py"])
print(results.linter.stats["global_note"])
from pylint.lint import Run

results = Run(["assignment6.py", do_exit=False])
print(results.linter.stats["global_note"])
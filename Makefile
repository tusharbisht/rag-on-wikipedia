.PHONY: help run eval embed-baseline validate render fmt test

help:
	@echo "make embed-baseline   — one-time: download + embed Simple English Wikipedia (~\$$5)"
	@echo "make run              — start the agent on http://localhost:8000"
	@echo "make eval             — run gold-set eval; print accuracy + ECE + latency"
	@echo "make validate         — cli validate against course.yaml"
	@echo "make render           — re-derive grading/*/judge.json + SUBMISSION.md"
	@echo "make fmt              — ruff format"
	@echo "make test             — pytest"

run:
	uv run uvicorn agent:app --host 0.0.0.0 --port 8000 --reload

eval:
	uv run python -m eval.run_gold_set

embed-baseline:
	uv run python -m kb_loader.embed_baseline

validate:
	cli validate ./course.yaml || python -m cli validate ./course.yaml

render:
	cli render-judge ./course.yaml && cli render-docs ./course.yaml

fmt:
	uv run ruff format .

test:
	uv run pytest -v

"""Grading engine for benchmark tasks.

Supports two grading modes:
1. Auto-grading: Compare LLM output to reference answer
2. Rubric-based grading: Score each criterion with LLM-as-judge
"""

from __future__ import annotations

import json
import re
from typing import Optional

from .models import (
    CriterionScore,
    GradingDetails,
    ReferenceAnswer,
    Rubric,
    TaskDefinition,
)


def grade_task(
    task: TaskDefinition,
    raw_output: str,
    grading_model: Optional[str] = None,
    dry_run: bool = False,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> GradingDetails:
    """Grade a task's raw LLM output.

    Args:
        task: The task definition with grading criteria
        raw_output: The raw LLM output to grade
        grading_model: Model to use for LLM-as-judge (if needed)
        dry_run: If True, use mock grading
        api_base: Custom API base URL for grading model
        api_key: Custom API key for grading model

    Returns:
        GradingDetails with score and breakdown.
    """
    if not raw_output.strip():
        return GradingDetails(
            grading_method="auto",
            total_score=0.0,
            rationale="Empty output from LLM.",
        )

    if task.grading_type == "reference_answer" and task.reference_answer:
        return _grade_reference(task.reference_answer, raw_output)
    elif task.grading_type == "rubric" and task.rubric:
        if dry_run:
            return _grade_rubric_mock(task.rubric, raw_output)
        return _grade_rubric_llm(task.rubric, raw_output, task.prompt, grading_model, api_base, api_key)
    else:
        return GradingDetails(
            grading_method="auto",
            total_score=0.0,
            rationale="No grading criteria found for task.",
        )


def _grade_reference(ref: ReferenceAnswer, raw_output: str) -> GradingDetails:
    """Auto-grade by comparing output to reference answer.

    Scoring:
    - Exact match: 100
    - Structural similarity (all key elements present): 80-99
    - Partial match (some key elements): 40-79
    - No match: 0-39
    """
    output_lower = raw_output.lower().strip()
    answer_lower = ref.answer.lower().strip()

    # Check for exact match
    if output_lower == answer_lower:
        return GradingDetails(
            grading_method="auto",
            total_score=100.0,
            reference_match_type="exact",
            rationale="Output matches reference answer exactly.",
        )

    # Check key elements
    if ref.key_elements:
        elements_found = 0
        for element in ref.key_elements:
            if element.lower() in output_lower:
                elements_found += 1

        match_ratio = elements_found / len(ref.key_elements)

        if match_ratio >= 0.9:
            score = 85.0 + (match_ratio - 0.9) * 150  # 85-100
            match_type = "structural"
        elif match_ratio >= 0.5:
            score = 40.0 + (match_ratio - 0.5) * 90  # 40-85
            match_type = "partial"
        else:
            score = match_ratio * 40  # 0-40
            match_type = "none"
    else:
        # No key elements defined, do text similarity
        score = _text_similarity(output_lower, answer_lower)
        if score >= 80:
            match_type = "structural"
        elif score >= 40:
            match_type = "partial"
        else:
            match_type = "none"

    # If the method is structural_similarity, adjust scoring
    if ref.method == "structural_similarity" and match_type == "structural":
        score = max(score, 80.0)

    return GradingDetails(
        grading_method="auto",
        total_score=round(min(score, 100.0), 1),
        reference_match_type=match_type,
        rationale=f"Match type: {match_type}. Found {match_ratio:.0%} of key elements."
        if ref.key_elements
        else f"Match type: {match_type}. Text similarity score: {score:.1f}",
    )


def _text_similarity(text1: str, text2: str) -> float:
    """Compute a simple text similarity score based on word overlap.

    This is a simplified metric, not a full NLP similarity measure.
    """
    words1 = set(re.findall(r"\b\w+\b", text1))
    words2 = set(re.findall(r"\b\w+\b", text2))

    if not words1 or not words2:
        return 0.0

    intersection = words1 & words2
    union = words1 | words2

    # Jaccard similarity scaled to 0-100
    jaccard = len(intersection) / len(union) if union else 0.0
    return round(jaccard * 100, 1)


def _grade_rubric_mock(rubric: Rubric, raw_output: str) -> GradingDetails:
    """Mock rubric grading for dry-run mode.

    Assigns scores based on simple heuristics of the output.
    """
    criterion_scores: list[CriterionScore] = []
    output_len = len(raw_output)

    for criterion in rubric.criteria:
        # Simple heuristic: longer, more detailed responses get higher mock scores
        # Base score depends on output length and content
        base = min(output_len / 200, 1.0) * 6  # 0-6 based on length

        # Bonus for having relevant keywords from the criterion description
        desc_words = set(re.findall(r"\b\w+\b", criterion.description.lower()))
        output_words = set(re.findall(r"\b\w+\b", raw_output.lower()))
        overlap = len(desc_words & output_words)
        bonus = min(overlap / max(len(desc_words), 1), 1.0) * 4  # 0-4 bonus

        score = min(round(base + bonus, 1), criterion.max_score)

        criterion_scores.append(
            CriterionScore(
                name=criterion.name,
                score=score,
                max_score=criterion.max_score,
                weight=criterion.weight,
                rationale=(
                    f"[Dry-run mock] Score based on output length"
                    f" ({output_len} chars) and keyword overlap."
                ),
            )
        )

    # Calculate weighted total
    total = sum(cs.score / cs.max_score * cs.weight for cs in criterion_scores) * 100
    total = round(min(total, 100.0), 1)

    return GradingDetails(
        grading_method="rubric",
        total_score=total,
        criterion_scores=criterion_scores,
        rationale="[Dry-run mock] Grading based on heuristics, not LLM evaluation.",
    )


def _grade_rubric_llm(
    rubric: Rubric,
    raw_output: str,
    original_prompt: str,
    grading_model: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> GradingDetails:
    """Grade using LLM-as-judge against rubric criteria.

    Sends the task prompt, rubric, and LLM output to a grading model
    which scores each criterion 0-10 with rationale.

    Falls back to mock grading if the grading model call fails.
    """
    from .llm_client import call_llm

    model = grading_model or _default_grading_model()

    grading_prompt = _build_grading_prompt(rubric, raw_output, original_prompt)

    try:
        response = call_llm(
            model=model,
            prompt=grading_prompt,
            temperature=0.0,
            max_tokens=2048,
            api_base=api_base,
            api_key=api_key,
        )
        return _parse_grading_response(rubric, response)
    except Exception as e:
        # Fallback to mock grading if LLM judge fails
        return GradingDetails(
            grading_method="rubric",
            total_score=0.0,
            rationale=f"LLM-as-judge failed: {e}. Falling back to mock scoring.",
        )


def _default_grading_model() -> str:
    """Get the default grading model from env or fallback."""
    import os
    return os.environ.get("GRADING_MODEL", os.environ.get("DEFAULT_MODEL", "gpt-4o"))


def _build_grading_prompt(rubric: Rubric, raw_output: str, original_prompt: str) -> str:
    """Build the prompt for LLM-as-judge grading."""
    criteria_text = "\n".join(
        f"  - {c.name} (weight: {c.weight}, max: {c.max_score}): {c.description}"
        for c in rubric.criteria
    )

    return f"""You are an expert evaluator grading an LLM's response to a benchmark task.

## Original Task Prompt
{original_prompt}

## LLM Response to Grade
{raw_output}

## Grading Rubric
{criteria_text}

## Instructions
Score each criterion from 0 to its max_score based on how well the
LLM response meets the criterion description.
Be strict but fair. A perfect score should be rare.

Respond ONLY with valid JSON in this exact format:
{{
  "criterion_scores": [
    {{"name": "<criterion_name>", "score": <0-max_score>, "rationale": "<brief explanation>"}},
    ...
  ],
  "overall_rationale": "<1-2 sentence summary>"
}}

Do not include any text before or after the JSON."""


def _parse_grading_response(rubric: Rubric, response: str) -> GradingDetails:
    """Parse the LLM-as-judge response into GradingDetails.

    Uses multiple repair strategies to handle malformed JSON from LLMs:
    1. Direct JSON parse
    2. Strip markdown fences, then parse
    3. Repair common issues (unescaped quotes in rationale, trailing commas)
    4. Regex-based fallback to extract individual criterion scores
    """
    # Try to extract JSON from the response
    json_str = _extract_json_string(response)
    if not json_str:
        return GradingDetails(
            grading_method="rubric",
            total_score=0.0,
            rationale="No JSON object found in grading response.",
        )

    # Try parsing with progressive repair strategies
    data = None
    parse_errors: list[str] = []

    # Strategy 1: Direct parse
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        parse_errors.append(f"direct: {e}")

    # Strategy 2: Strip markdown code fences and parse
    if data is None:
        stripped = re.sub(r"```(?:json)?\s*", "", json_str).strip()
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError as e:
            parse_errors.append(f"strip-fences: {e}")

    # Strategy 3: Fix trailing commas before } or ]
    if data is None:
        fixed = re.sub(r",\s*([}\]])", r"\1", json_str)
        try:
            data = json.loads(fixed)
        except json.JSONDecodeError as e:
            parse_errors.append(f"fix-trailing-commas: {e}")

    # Strategy 4: Regex fallback - extract scores directly
    if data is None:
        criterion_scores = _regex_extract_scores(rubric, response)
        if criterion_scores:
            total = sum(cs.score / cs.max_score * cs.weight for cs in criterion_scores) * 100
            total = round(min(total, 100.0), 1)
            return GradingDetails(
                grading_method="rubric",
                total_score=total,
                criterion_scores=criterion_scores,
                rationale="[Regex fallback] Parsed from malformed JSON response.",
            )
        return GradingDetails(
            grading_method="rubric",
            total_score=0.0,
            rationale=f"Failed to parse grading response: {'; '.join(parse_errors)}",
        )

    return _build_grading_details_from_data(rubric, data)


def _extract_json_string(response: str) -> Optional[str]:
    """Extract the JSON block from the grading response."""
    # Try to find JSON wrapped in markdown code fences first
    fence_match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", response)
    if fence_match:
        return fence_match.group(1)

    # Fall back to finding any JSON object
    json_match = re.search(r"\{[\s\S]*\}", response)
    if json_match:
        return json_match.group()

    return None


def _regex_extract_scores(rubric: Rubric, response: str) -> list[CriterionScore]:
    """Fallback: extract criterion scores using regex when JSON parsing fails.

    Looks for patterns like "name": "...", "score": N in the response.
    """
    criterion_scores: list[CriterionScore] = []
    criterion_map = {c.name.lower(): c for c in rubric.criteria}

    # Find all score-like patterns: "score": <number>
    score_pattern = re.compile(r'"(?:name|criterion)"\s*:\s*"([^"]+)"[^}]*?"score"\s*:\s*(\d+(?:\.\d+)?)', re.IGNORECASE)
    # Also try the reverse order
    score_pattern2 = re.compile(r'"score"\s*:\s*(\d+(?:\.\d+)?)[^}]*?"(?:name|criterion)"\s*:\s*"([^"]+)"', re.IGNORECASE)

    found: dict[str, float] = {}

    for match in score_pattern.finditer(response):
        name = match.group(1).lower()
        score = float(match.group(2))
        found[name] = score

    for match in score_pattern2.finditer(response):
        score = float(match.group(1))
        name = match.group(2).lower()
        found[name] = score

    for name_lower, score in found.items():
        # Match to rubric criterion (fuzzy)
        criterion = None
        for cname_lower, cobj in criterion_map.items():
            if cname_lower in name_lower or name_lower in cname_lower:
                criterion = cobj
                break

        if criterion:
            score = min(score, criterion.max_score)
            criterion_scores.append(
                CriterionScore(
                    name=criterion.name,
                    score=score,
                    max_score=criterion.max_score,
                    weight=criterion.weight,
                    rationale="[Regex fallback] Score extracted from malformed JSON.",
                )
            )

    # Fill in missing criteria with 0
    scored_names = {cs.name for cs in criterion_scores}
    for criterion in rubric.criteria:
        if criterion.name not in scored_names:
            criterion_scores.append(
                CriterionScore(
                    name=criterion.name,
                    score=0.0,
                    max_score=criterion.max_score,
                    weight=criterion.weight,
                    rationale="Not scored by LLM judge (regex fallback).",
                )
            )

    return criterion_scores


def _build_grading_details_from_data(rubric: Rubric, data: dict) -> GradingDetails:
    """Build GradingDetails from parsed JSON data."""
    criterion_scores: list[CriterionScore] = []
    criterion_map = {c.name: c for c in rubric.criteria}

    for cs_data in data.get("criterion_scores", []):
        name = cs_data.get("name", "")
        criterion = criterion_map.get(name)
        if not criterion:
            # Try fuzzy match
            for cname, cobj in criterion_map.items():
                if cname.lower() in name.lower() or name.lower() in cname.lower():
                    criterion = cobj
                    break

        if criterion:
            score = float(cs_data.get("score", 0))
            score = min(score, criterion.max_score)
            criterion_scores.append(
                CriterionScore(
                    name=criterion.name,
                    score=score,
                    max_score=criterion.max_score,
                    weight=criterion.weight,
                    rationale=cs_data.get("rationale", ""),
                )
            )

    # If we didn't get all criteria scored, fill in missing ones with 0
    scored_names = {cs.name for cs in criterion_scores}
    for criterion in rubric.criteria:
        if criterion.name not in scored_names:
            criterion_scores.append(
                CriterionScore(
                    name=criterion.name,
                    score=0.0,
                    max_score=criterion.max_score,
                    weight=criterion.weight,
                    rationale="Not scored by LLM judge.",
                )
            )

    # Calculate weighted total
    total = sum(cs.score / cs.max_score * cs.weight for cs in criterion_scores) * 100
    total = round(min(total, 100.0), 1)

    return GradingDetails(
        grading_method="rubric",
        total_score=total,
        criterion_scores=criterion_scores,
        rationale=data.get("overall_rationale", ""),
    )

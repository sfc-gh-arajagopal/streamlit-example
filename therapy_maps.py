"""Original therapy study maps.

These summarize widely published clinical ideas for learning and session
planning. They are not copies of any commercial mind-map pack.
"""

from __future__ import annotations

import html

MAPS: list[dict] = [
    {
        "id": "process",
        "title": "Therapeutic process",
        "summary": "A session-to-session arc from a clear frame through shared work to a planned ending.",
        "center": "Therapy",
        "branches": [
            {
                "title": "Frame",
                "color": "#0f766e",
                "items": ["Consent and roles", "Confidentiality limits", "Practical agreements"],
            },
            {
                "title": "Alliance",
                "color": "#b45309",
                "items": ["Warmth and respect", "Shared goals", "Repair ruptures early"],
            },
            {
                "title": "Assess",
                "color": "#1d4ed8",
                "items": ["Story and context", "Symptoms and risk", "Strengths and supports"],
            },
            {
                "title": "Formulate",
                "color": "#7c3aed",
                "items": ["What keeps it going", "A shared hypothesis", "What to test first"],
            },
            {
                "title": "Plan",
                "color": "#be123c",
                "items": ["Specific goals", "Methods and pace", "Between-session tasks"],
            },
            {
                "title": "Work",
                "color": "#0369a1",
                "items": ["Skills and experiments", "Review what happened", "Update the plan"],
            },
            {
                "title": "Close",
                "color": "#3f6212",
                "items": ["Relapse plan", "Ending the work", "Follow-up if needed"],
            },
        ],
    },
    {
        "id": "cbt",
        "title": "Cognitive behavioral therapy",
        "summary": "Situation, meaning, feeling, body, and action influence each other. Change can start at any point.",
        "center": "CBT",
        "branches": [
            {
                "title": "Situation",
                "color": "#0f766e",
                "items": ["What happened", "Where and with whom", "What I noticed first"],
            },
            {
                "title": "Thoughts",
                "color": "#1d4ed8",
                "items": ["Automatic thoughts", "Rules and assumptions", "Core beliefs"],
            },
            {
                "title": "Emotion",
                "color": "#be123c",
                "items": ["Name the feeling", "Rate the intensity", "Allow mixed feelings"],
            },
            {
                "title": "Body",
                "color": "#b45309",
                "items": ["Arousal and tension", "Sleep and energy", "Appetite and pain"],
            },
            {
                "title": "Action",
                "color": "#7c3aed",
                "items": ["What I did", "What I avoided", "Safety behaviors"],
            },
            {
                "title": "Test it",
                "color": "#0369a1",
                "items": ["Evidence for and against", "Another plausible view", "A behavioral experiment"],
            },
            {
                "title": "Practice",
                "color": "#3f6212",
                "items": ["One between-session step", "Review the result", "Keep or adjust"],
            },
        ],
    },
    {
        "id": "distortions",
        "title": "Common thought traps",
        "summary": "Habits of interpretation that feel true in the moment. The check question is a way back to a wider view.",
        "center": "Traps",
        "branches": [
            {
                "title": "All or nothing",
                "color": "#be123c",
                "items": ["Only extremes count", "Look for the middle"],
            },
            {
                "title": "Overgeneralizing",
                "color": "#b45309",
                "items": ["Always or never", "Stay with this instance"],
            },
            {
                "title": "Mental filter",
                "color": "#1d4ed8",
                "items": ["One detail fills the frame", "What else is here"],
            },
            {
                "title": "Discounting good",
                "color": "#7c3aed",
                "items": ["Positives do not count", "Let them count"],
            },
            {
                "title": "Mind reading",
                "color": "#0f766e",
                "items": ["Guessing their mind", "Check or hold it lightly"],
            },
            {
                "title": "Fortune telling",
                "color": "#0369a1",
                "items": ["The bad outcome is certain", "Rate odds and coping"],
            },
            {
                "title": "Magnifying",
                "color": "#9f1239",
                "items": ["Problems loom, skills shrink", "Right-size both"],
            },
            {
                "title": "Emotional reasoning",
                "color": "#a16207",
                "items": ["I feel it, so it is true", "Feeling is data, not proof"],
            },
            {
                "title": "Shoulds",
                "color": "#3f6212",
                "items": ["Rigid rules for self or others", "Prefer, or choose"],
            },
            {
                "title": "Labels and blame",
                "color": "#4338ca",
                "items": ["A person reduced to one act", "Name the act, not the person"],
            },
        ],
    },
    {
        "id": "act",
        "title": "Psychological flexibility",
        "summary": "Six moves from acceptance and commitment therapy. The aim is workable action toward what matters, including when pain is present.",
        "center": "ACT",
        "branches": [
            {
                "title": "Acceptance",
                "color": "#0f766e",
                "items": ["Make room for feeling", "Drop the struggle to erase it"],
            },
            {
                "title": "Defusion",
                "color": "#1d4ed8",
                "items": ["Notice a thought as a thought", "Name the story, unhook"],
            },
            {
                "title": "Present",
                "color": "#b45309",
                "items": ["Come back to the senses", "One moment, one task"],
            },
            {
                "title": "Observer",
                "color": "#7c3aed",
                "items": ["You are more than the story", "Notice who is noticing"],
            },
            {
                "title": "Values",
                "color": "#be123c",
                "items": ["Chosen directions", "Qualities of action"],
            },
            {
                "title": "Committed action",
                "color": "#3f6212",
                "items": ["Small steps that fit", "Continue with discomfort"],
            },
        ],
    },
    {
        "id": "formulation",
        "title": "Case formulation",
        "summary": "The five Ps turn a problem list into a working map of why this is happening now and what can help.",
        "center": "5 Ps",
        "branches": [
            {
                "title": "Presenting",
                "color": "#be123c",
                "items": ["Problem in their words", "Impact on life", "Risk right now"],
            },
            {
                "title": "Predisposing",
                "color": "#7c3aed",
                "items": ["History and learning", "Temperament and health", "Culture and context"],
            },
            {
                "title": "Precipitating",
                "color": "#b45309",
                "items": ["Recent triggers", "Losses and changes", "Why now"],
            },
            {
                "title": "Perpetuating",
                "color": "#1d4ed8",
                "items": ["Cycles that maintain it", "Avoidance and beliefs", "Environment responses"],
            },
            {
                "title": "Protective",
                "color": "#0f766e",
                "items": ["Strengths and skills", "People and values", "What already helps"],
            },
            {
                "title": "Plan",
                "color": "#3f6212",
                "items": ["First targets", "How we will know", "Who does what"],
            },
        ],
    },
    {
        "id": "anxiety",
        "title": "Anxiety cycle",
        "summary": "Alarm, threat meaning, and safety behaviors can keep anxiety going even when the feared outcome does not happen.",
        "center": "Anxiety",
        "branches": [
            {
                "title": "Trigger",
                "color": "#b45309",
                "items": ["Cue or uncertainty", "Body sensation", "Memory or image"],
            },
            {
                "title": "Appraisal",
                "color": "#be123c",
                "items": ["This is dangerous", "I cannot cope", "I must stop it now"],
            },
            {
                "title": "Alarm",
                "color": "#9f1239",
                "items": ["Heart and breath", "Tension and heat", "Dizziness or nausea"],
            },
            {
                "title": "Safety move",
                "color": "#1d4ed8",
                "items": ["Avoid or escape", "Check and reassure", "Control or prepare"],
            },
            {
                "title": "Payoff",
                "color": "#7c3aed",
                "items": ["Relief in the short term", "Fear stays in place", "Life gets smaller"],
            },
            {
                "title": "Turn",
                "color": "#0f766e",
                "items": ["Stay and breathe", "Test the prediction", "Approach in steps"],
            },
        ],
    },
    {
        "id": "depression",
        "title": "Low mood cycle",
        "summary": "Withdrawal reduces contact with reward and other people, which gives the low mood more evidence.",
        "center": "Low mood",
        "branches": [
            {
                "title": "Load",
                "color": "#b45309",
                "items": ["Loss or stress", "Exhaustion", "Conflict or isolation"],
            },
            {
                "title": "Mood",
                "color": "#1d4ed8",
                "items": ["Sad, flat, or numb", "Irritable or hopeless", "Low interest"],
            },
            {
                "title": "Pull back",
                "color": "#7c3aed",
                "items": ["Less activity", "More rumination", "Putting life on hold"],
            },
            {
                "title": "Result",
                "color": "#be123c",
                "items": ["Fewer rewarding moments", "More fatigue", "Nothing helps feels true"],
            },
            {
                "title": "Restart",
                "color": "#0f766e",
                "items": ["Tiny valued actions", "Routine, light, people", "Sleep and movement"],
            },
            {
                "title": "Thoughts",
                "color": "#3f6212",
                "items": ["Catch always and never", "Test one prediction", "Speak to yourself fairly"],
            },
        ],
    },
    {
        "id": "emotion",
        "title": "Working with emotion",
        "summary": "A practical sequence: notice the emotion, understand its job, then choose a response that fits the situation and your values.",
        "center": "Emotion",
        "branches": [
            {
                "title": "Name it",
                "color": "#be123c",
                "items": ["Feeling word", "Intensity 0 to 10", "Body and urge"],
            },
            {
                "title": "Allow",
                "color": "#b45309",
                "items": ["Let the wave move", "No need to fix it at once"],
            },
            {
                "title": "Understand",
                "color": "#1d4ed8",
                "items": ["What need is here", "What triggered it", "What story is attached"],
            },
            {
                "title": "Choose",
                "color": "#7c3aed",
                "items": ["Change the situation", "Shift attention", "Reappraise or act"],
            },
            {
                "title": "Soothe",
                "color": "#0f766e",
                "items": ["Breath and grounding", "Rest and support", "Something kind and concrete"],
            },
            {
                "title": "Toward values",
                "color": "#3f6212",
                "items": ["If the urge shrinks life", "Take one opposite step", "Keep it small enough to do"],
            },
        ],
    },
    {
        "id": "alliance",
        "title": "Therapeutic alliance",
        "summary": "Bond, goals, and tasks are the working relationship. Fit and repair matter as much as technique.",
        "center": "Alliance",
        "branches": [
            {
                "title": "Bond",
                "color": "#be123c",
                "items": ["Empathy", "Respect", "Genuineness"],
            },
            {
                "title": "Goals",
                "color": "#1d4ed8",
                "items": ["Shared", "Specific", "Open to revision"],
            },
            {
                "title": "Tasks",
                "color": "#0f766e",
                "items": ["Methods that make sense", "Agreed, not imposed", "Reviewed together"],
            },
            {
                "title": "Fit",
                "color": "#b45309",
                "items": ["Culture and identity", "Language and pace", "Power and access"],
            },
            {
                "title": "Rupture",
                "color": "#7c3aed",
                "items": ["Name the strain", "Own your part", "Repair and continue"],
            },
            {
                "title": "Frame",
                "color": "#3f6212",
                "items": ["Boundaries", "Consent", "Confidentiality"],
            },
        ],
    },
    {
        "id": "session",
        "title": "Session map",
        "summary": "A blank map for one moment in therapy. Fill the branches in the client's words.",
        "center": "Today",
        "branches": [
            {
                "title": "Situation",
                "color": "#0f766e",
                "items": ["What happened", "When it mattered most"],
            },
            {
                "title": "Thought",
                "color": "#1d4ed8",
                "items": ["What I told myself", "The hottest line"],
            },
            {
                "title": "Feeling",
                "color": "#be123c",
                "items": ["Emotion", "Where it sits in the body"],
            },
            {
                "title": "Action",
                "color": "#b45309",
                "items": ["What I did", "What I avoided"],
            },
            {
                "title": "Need",
                "color": "#7c3aed",
                "items": ["What mattered underneath", "What I wanted"],
            },
            {
                "title": "Next",
                "color": "#3f6212",
                "items": ["One small step", "What would make it 10% easier"],
            },
        ],
    },
]


def text_width(value: str, size: float) -> float:
    """Approximate SVG text width without a font engine."""
    width = 0.0
    for char in value:
        if char == " ":
            width += size * 0.33
        elif char in "il.,'|":
            width += size * 0.28
        elif char in "mwMW":
            width += size * 0.85
        else:
            width += size * 0.56
    return width


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def to_markdown(mind_map: dict) -> str:
    lines = [f"# {mind_map['title']}", "", mind_map["summary"], ""]
    for branch in mind_map["branches"]:
        lines.append(f"- {branch['title']}")
        for item in branch["items"]:
            lines.append(f"  - {item}")
    lines.append("")
    return "\n".join(lines)


def to_mermaid(mind_map: dict) -> str:
    lines = ["mindmap", f"  root(({_mermaid_label(mind_map['center'])}))"]
    for branch in mind_map["branches"]:
        lines.append(f"    {_mermaid_label(branch['title'])}")
        for item in branch["items"]:
            lines.append(f"      {_mermaid_label(item)}")
    lines.append("")
    return "\n".join(lines)


def _mermaid_label(value: str) -> str:
    cleaned = value.replace("(", "").replace(")", "").replace('"', "'")
    if any(char in cleaned for char in ":;[]{}#"):
        return f'"{cleaned}"'
    return cleaned


def to_svg(mind_map: dict) -> tuple[str, int, int]:
    """Return an SVG mind map plus its pixel width and height."""
    leaf_h = 28
    leaf_gap = 6
    branch_h = 34
    branch_gap = 18
    pad_x = 14
    column_gap = 54
    margin = 32
    label_size = 14
    leaf_size = 13
    center_size = 18

    def leaf_block_width(items: list[str]) -> float:
        if not items:
            return 0
        return max(text_width(item, leaf_size) + pad_x * 2 for item in items)

    def label_width(title: str) -> float:
        return text_width(title, label_size) + pad_x * 2

    def block_height(branch: dict) -> float:
        count = max(1, len(branch["items"]))
        leaves = count * leaf_h + max(0, count - 1) * leaf_gap
        return max(branch_h, leaves)

    left = mind_map["branches"][0::2]
    right = mind_map["branches"][1::2]

    def column_width(branches: list[dict]) -> float:
        if not branches:
            return 0
        return max(label_width(branch["title"]) + 12 + leaf_block_width(branch["items"]) for branch in branches)

    def stack_height(branches: list[dict]) -> float:
        if not branches:
            return 0
        return sum(block_height(branch) for branch in branches) + branch_gap * (len(branches) - 1)

    left_w = column_width(left)
    right_w = column_width(right)
    hub_w = text_width(mind_map["center"], center_size) + 56
    hub_h = 72
    height = int(max(stack_height(left), stack_height(right), hub_h) + margin * 2)
    width = int(margin + left_w + column_gap + hub_w + column_gap + right_w + margin)
    hub_x = margin + left_w + column_gap
    hub_y = (height - hub_h) / 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        "<title>" + _escape(mind_map["title"]) + "</title>",
        "<defs>",
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
        '<feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-color="#1c1917" flood-opacity="0.12"/>',
        "</filter>",
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="28" fill="#fbf7f2"/>',
    ]

    def draw_side(branches: list[dict], side: str) -> None:
        if not branches:
            return
        y = (height - stack_height(branches)) / 2
        for branch in branches:
            color = branch["color"]
            block_h = block_height(branch)
            label_w = label_width(branch["title"])
            leaves_w = leaf_block_width(branch["items"])
            if side == "left":
                label_x = margin + left_w - label_w
                leaves_x = label_x - 12 - leaves_w
                x1, x2 = hub_x, label_x + label_w
            else:
                label_x = hub_x + hub_w + column_gap
                leaves_x = label_x + label_w + 12
                x1, x2 = hub_x + hub_w, label_x
            label_y = y + (block_h - branch_h) / 2
            y1 = hub_y + hub_h / 2
            y2 = label_y + branch_h / 2
            mid_x = (x1 + x2) / 2
            parts.append(
                f'<path d="M {x1:.1f} {y1:.1f} C {mid_x:.1f} {y1:.1f}, {mid_x:.1f} {y2:.1f}, {x2:.1f} {y2:.1f}" '
                f'fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>'
            )
            parts.append(
                f'<rect x="{label_x:.1f}" y="{label_y:.1f}" width="{label_w:.1f}" height="{branch_h}" rx="17" '
                f'fill="{color}" filter="url(#shadow)"/>'
            )
            parts.append(
                f'<text x="{label_x + label_w / 2:.1f}" y="{label_y + branch_h / 2:.1f}" text-anchor="middle" '
                f'dominant-baseline="middle" fill="#fffaf5" font-family="Georgia, serif" font-size="{label_size}" '
                f'font-weight="700">{_escape(branch["title"])}</text>'
            )
            leaf_y = y + (block_h - (len(branch["items"]) * leaf_h + max(0, len(branch["items"]) - 1) * leaf_gap)) / 2
            for item in branch["items"]:
                parts.append(
                    f'<rect x="{leaves_x:.1f}" y="{leaf_y:.1f}" width="{leaves_w:.1f}" height="{leaf_h}" rx="8" '
                    f'fill="#fffdf9" stroke="{color}" stroke-opacity="0.45"/>'
                )
                parts.append(
                    f'<text x="{leaves_x + 12:.1f}" y="{leaf_y + leaf_h / 2:.1f}" text-anchor="start" '
                    f'dominant-baseline="middle" fill="#292524" font-family="Georgia, serif" font-size="{leaf_size}">'
                    f'{_escape(item)}</text>'
                )
                leaf_y += leaf_h + leaf_gap
            y += block_h + branch_gap

    draw_side(left, "left")
    draw_side(right, "right")
    parts.append(
        f'<rect x="{hub_x:.1f}" y="{hub_y:.1f}" width="{hub_w:.1f}" height="{hub_h}" rx="36" fill="#292524" filter="url(#shadow)"/>'
    )
    parts.append(
        f'<text x="{hub_x + hub_w / 2:.1f}" y="{hub_y + hub_h / 2:.1f}" text-anchor="middle" dominant-baseline="middle" '
        f'fill="#fffaf5" font-family="Georgia, serif" font-size="{center_size}" font-weight="700">'
        f'{_escape(mind_map["center"])}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts), width, height

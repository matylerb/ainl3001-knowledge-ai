"""AINL3001 — Topic 7: Knowledge Representation and Logical Reasoning.

Student starter: complete the TODOs in Tasks 3 and 4.
This lab uses propositional facts and simple IF/THEN rules.

BSP
2026
"""

# TASK 1 — Represent facts (provided; inspect and experiment).
facts = {"rainy", "weekday", "cold"}

# TASK 2 — Represent rules (provided; inspect and experiment).
# Each rule is (list_of_required_facts, conclusion).
# All conditions must be known before the conclusion can be inferred.
rules = [
    (["rainy"], "take_umbrella"),
    (["rainy", "cold"], "wear_coat"),
    (["take_umbrella"], "stay_dry"),
]


# Forward chaining: start from known facts, apply every matching rule, repeat until no new facts can be added.
def forward_chaining(known_facts, rules):
    """Return all original and inferred facts without changing known_facts.

    TASK 3 — TODO:
    1. Copy known_facts into a new set.
    2. Examine every rule and add its conclusion when ALL conditions hold.
    3. Repeat until an entire pass adds no new facts.
    4. Return the completed set.
    """
    # TODO

    inferred_facts = set(known_facts)  # start with what we already know

    changed = True
    while changed:  # keep looping until a full pass adds nothing new
        changed = False

        for conditions, conclusion in rules:
            if all(c in inferred_facts for c in conditions):  # if every condition is already known...
                if conclusion not in inferred_facts: # ...and we haven't added this conclusion yet...
                    inferred_facts.add(conclusion) # ...add it as a new fact
                    changed = True # flag that something changed, so loop again

    return inferred_facts


def query(inferred_facts, statement):
    """TASK 4 — Return True if statement is established in inferred_facts.

    A False result means 'not established', not necessarily 'false'.
    """
    # TODO

    return statement in inferred_facts
    pass

# Backward chaining: start from a goal, find a rule that proves it, then recursively prove each of that rule's conditions.
def backward_chaining(goal, known_facts, rules):
    """TASK 5  - Return True if goal can be proven from known_facts using rules.

    Starts from the goal and works backwards: find a rule that concludes
    the goal, then recursively check if all that rule's conditions are provable.
    """
    if goal in known_facts: # base case: if the goal is already a known fact, no need to search
        return True
    for conditions, conclusion in rules:
        if conclusion == goal:  # find a rule whose conclusion matches the goal we're trying to prove
            if all(backward_chaining(c, known_facts, rules) for c in conditions):  # recursively prove each condition
                return True # all conditions provable, so the goal is provable
    return False # no rule could prove the goal


if __name__ == "__main__":
    print("=" * 55)
    print("TASK 0 — MANUAL REASONING")
    print("=" * 55)
    print("Initial facts:", sorted(facts))
    print("Rules:")
    for conditions, conclusion in rules:
        print(f"  IF {' AND '.join(conditions)} THEN {conclusion}")
    print("\nBefore coding, predict whether these can be inferred:")
    print("  take_umbrella?  stay_dry?  wear_coat?  Why?")

    print("\n" + "=" * 55)
    print("TASKS 3–4 — FORWARD CHAINING AND QUERIES")
    print("=" * 55)
    inferred = forward_chaining(facts, rules)
    if inferred is None:
        print("Complete forward_chaining() to see inferred knowledge.")
    else:
        print("Initial facts:", sorted(facts))
        print("All known facts:", sorted(inferred))
        for statement in ("take_umbrella", "stay_dry", "wear_coat"):
            print(f"Can infer {statement}? {query(inferred, statement)}")

    print("\n" + "=" * 55)
    print("TASK 5 — BACKWARD CHAINING")
    print("=" * 55)
    for goal in ("stay_dry", "wear_coat", "take_umbrella"):
        result = backward_chaining(goal, facts, rules)
        print(f"Can backward chaining prove '{goal}'? {result}")

    print("\nTASK 6 — LOGIC DISCUSSION")
    print("Is 'IF rainy THEN take_umbrella' always true in the real world?")
    print("What assumptions does the rule make?")
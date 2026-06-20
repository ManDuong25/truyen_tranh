from __future__ import annotations

from .models import Character, RelationshipState, Secret, WorldSeed


def build_bridge_scenario(run_id: str = "run_bridge_poc") -> WorldSeed:
    characters = {
        "linh": Character(
            id="linh",
            name="Linh",
            role="protagonist",
            public_description="A guarded young cultivator searching for the truth.",
            personality_traits=("stubborn", "distrustful", "emotionally guarded"),
            short_term_goal="force Khai to explain what happened to her father",
            long_term_goal="uncover the organization behind her father's disappearance",
            starting_location="rainy_old_bridge",
        ),
        "khai": Character(
            id="khai",
            name="Khai",
            role="oath-bound protector",
            public_description="A calm swordsman who knows more than he admits.",
            personality_traits=("protective", "guilty", "self-controlled"),
            short_term_goal="keep Linh alive without breaking his oath",
            long_term_goal="repay an old debt by protecting Linh",
            starting_location="rainy_old_bridge",
            private_secret_ids=("s_khai_black_lotus",),
        ),
        "minh": Character(
            id="minh",
            name="Minh",
            role="opportunist",
            public_description="A smiling informant who listens before he strikes.",
            personality_traits=("manipulative", "patient", "ambitious"),
            short_term_goal="learn leverage over Linh and Khai",
            long_term_goal="sell secrets to the strongest faction",
            starting_location="rainy_old_bridge",
        ),
    }
    secrets = {
        "s_khai_black_lotus": Secret(
            id="s_khai_black_lotus",
            truth="Khai once served the Black Lotus sect that took Linh's father.",
            known_by=("khai",),
            reveal_conditions=("Khai voluntarily confesses", "GM commits a reveal event"),
        )
    }
    relationships = {
        ("linh", "khai"): RelationshipState(
            from_id="linh",
            to_id="khai",
            trust=35,
            tension=45,
            reason="Linh suspects Khai is hiding something about her father.",
        ),
        ("khai", "linh"): RelationshipState(
            from_id="khai",
            to_id="linh",
            trust=65,
            tension=55,
            reason="Khai wants to protect Linh but fears the oath.",
        ),
        ("minh", "linh"): RelationshipState(
            from_id="minh",
            to_id="linh",
            trust=10,
            tension=30,
            reason="Minh sees Linh as useful leverage.",
        ),
        ("minh", "khai"): RelationshipState(
            from_id="minh",
            to_id="khai",
            trust=5,
            tension=35,
            reason="Minh suspects Khai has marketable secrets.",
        ),
    }
    return WorldSeed(
        run_id=run_id,
        world_name="Rain Veil City",
        location="rainy_old_bridge",
        premise=(
            "A guarded young cultivator confronts an oath-bound protector while "
            "an opportunist listens from the rain."
        ),
        characters=characters,
        secrets=secrets,
        relationships=relationships,
    )

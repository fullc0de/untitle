from typing import List

def build_prompt(
    template: str,
    user_name: str,
    user_description: str,
    user_age: int,
    user_gender: str,
    persona_list: List[str],
    persona_relationship: List[str]
) -> str:
    persona_list_str = "\n".join(
        [f"{i+1}. {persona}" for i, persona in enumerate(persona_list)]
    ) if persona_list else ''
    
    persona_relationship_str = "\n".join(
        [f"{i+1}. {relationship}" for i, relationship in enumerate(persona_relationship)]
    ) if persona_relationship else ''
    
    return template.format(
        user_name=user_name,
        user_description=user_description, 
        user_age=user_age,
        user_gender=user_gender,
        persona_list=persona_list_str,
        persona_relationship=persona_relationship_str
    )



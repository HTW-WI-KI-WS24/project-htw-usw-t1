from langchain.llms import OpenAI
from langchain.schema import SystemMessage

# Initialize the LLMs for each agent
creative_llm = OpenAI()
critical_llm = OpenAI()
user_focussed_llm = OpenAI()


# Helper function to improve prompt using a given LLM and a specific instruction
def improve_prompt_with_llm(llm, human_message, instruction):
    messages = [SystemMessage(
        content=f"{instruction} '{human_message}'."
    )]
    improved_prompt = llm.invoke(messages)
    print("Improved prompt:", improved_prompt)
    return improved_prompt


# Define the roles of the agents with LLM-based improvement logic
class CreativeAgent:
    def suggest_improvement(self, prompt):
        creative_instruction = ("Please refine the user's prompt by adding creative elements and imaginative "
                                "scenarios. Only give me the refined user prompt.")
        print("Creative instruction:", creative_instruction)
        return improve_prompt_with_llm(creative_llm, prompt, creative_instruction)


class CriticalAgent:
    def suggest_improvement(self, prompt):
        critical_instruction = "Please refine the user's prompt by enhancing its clarity and precision."
        print("Critical instruction:", critical_instruction)
        return improve_prompt_with_llm(critical_llm, prompt, critical_instruction)


class UserFocusedAgent:
    def suggest_improvement(self, prompt):
        user_focused_instruction = ("Please refine the user's prompt by aligning it closely with user needs and "
                                    "practical outcomes.")
        print("User-focused instruction:", user_focused_instruction)
        return improve_prompt_with_llm(user_focussed_llm, prompt, user_focused_instruction)


# Function to simulate a debate between agents
def debate(agents, original_prompt):
    suggestions = [agent.suggest_improvement(original_prompt) for agent in agents]
    # Simulated discussion
    for i, agent in enumerate(agents):
        for j, other_agent in enumerate(agents):
            if i != j:
                #print(f"Agent {i+1} about Agent {j+1}'s prompt: {agent.comment_on_prompt(suggestions[j])}")
                print(f"Agent {i+1} about Agent {j+1}'s prompt: ")

    # Decision mechanism (placeholder logic)
    # For simplicity, let's say they agree on the longest prompt after discussion
    ideal_prompt = max(suggestions, key=len)
    return ideal_prompt


# Main execution function
def main():
    user_prompt = input("Enter your prompt: ")

    # Initialize agents
    creative_agent = CreativeAgent()
    critical_agent = CriticalAgent()
    user_focused_agent = UserFocusedAgent()
    agents = [creative_agent, critical_agent, user_focused_agent]

    # Agents debate and agree on an ideal prompt
    ideal_prompt = debate(agents, user_prompt)
    print("Ideal prompt after debate:", ideal_prompt)

    # LLM responds to the ideal prompt
    llm_response = OpenAI().invoke(ideal_prompt)
    print("LLM's response to the ideal prompt:", llm_response)


if __name__ == "__main__":
    main()

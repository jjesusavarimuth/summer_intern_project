import asyncio

from agents import Runner, SQLiteSession

from .agents.coordinator_agent import coordinator_agent

class Manager:

    async def run(self) -> None:
        # Intialize session to store conversation history
        session = SQLiteSession("session1")

        print("Hi I'm a data analysis and visualization assistant for a digital fashion e-commerce store. I can help you with data insights, visualizations, and QuickSight management. How can I help you today?")
        # Add initial message to the session
        await session.add_items([{"role": "assistant", "content": "Hi I'm a data analysis and visualization assistant for a digital fashion e-commerce store. I can help you with data insights, visualizations, and QuickSight management. How can I help you today?"}])

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ("exit"):
                    print("\nGoodbye!")
                    break
                
                if not user_input:
                    continue
                
                # By passing the session each run, the agent has knowledge of the conversation history
                
                chatbot_response = await Runner.run(coordinator_agent, user_input, session=session)
                
                print("\n" + chatbot_response.final_output + "\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...")
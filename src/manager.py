import asyncio

from agents import Runner, SQLiteSession

from .agents.data_insights_agent import data_insights_agent

class Manager:

    async def run(self) -> None:
        # Intialize session to store conversation history
        session = SQLiteSession("session1")

        print("Hi I'm a data insights assistant for a digital fashion e-commerce store. How can I help you today?")
        # Add initial message to the session
        await session.add_items([{"role": "assistant", "content": "Hi I'm a data insights assistant for a digital fashion e-commerce store. How can I help you today?"}])

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ("exit"):
                    print("\nGoodbye!")
                    break
                
                if not user_input:
                    continue
                
                # By passing the session each run, the agent has knowledge of the conversation history
                
                chatbot_response = await Runner.run(data_insights_agent, user_input, session=session)
                
                print("\n" + chatbot_response.final_output + "\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...")
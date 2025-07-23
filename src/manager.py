import asyncio

from agents import Runner, SQLiteSession

from .agents.web_search_agent import web_search_agent

class Manager:

    async def run(self) -> None:
        # Intialize session to store conversation history
        session = SQLiteSession("session1")

        print("Welcome to my web search assistant! What's on your mind?")
        # Add initial message to the session
        await session.add_items([{"role": "assistant", "content": "Welcome to my web search assistant! What's on your mind?"}])

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ("exit"):
                    print("\nGoodbye!")
                    break
                
                if not user_input:
                    continue
                
                # By passing the session each run, the agent has knowledge of the conversation history
                chatbot_response = await Runner.run(web_search_agent, user_input, session=session)
                
                print(chatbot_response.final_output)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...")
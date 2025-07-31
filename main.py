from agent import agent_executor


def main():
    print("\n\n🤖 Task Assistant Local (Powered by Llama3)")
    print("=" * 50)
    print("📝 Example commands:")
    print("   • 'Add a task: review code with high priority'")
    print("   • 'What tasks do I have?'")
    print("   • 'Show only high priority tasks'")
    print("   • 'Mark task 1 as completed'")
    print("   • 'Delete task 3'")
    print("   • 'Show me statistics'")
    print("   • 'bye', 'exit', 'quit', or 'done' to quit")
    print("=" * 50)

    while True:
        try:
            user_input = input("\n💬 What do you need? > ")

            if user_input.lower() in ['bye', 'exit', 'quit', 'done', 'q']:
                print("\n👋 Goodbye! Your tasks are saved.")
                break
            
            if not user_input.strip():
                continue
            
            print("\n🧠 Thinking...")
            response = agent_executor.invoke({"input": user_input})
            output = response.get('output', '')

            if "Agent stopped due to iteration limit" in output:
                print("\n📋 Here's what I found:")

                steps = response.get('intermediate_steps', [])
                if steps and len(steps) > 0:
                    # Get the last tool output
                    last_output = None
                    for action, observation in steps:
                        if observation and "📋" in str(observation):
                            last_output = observation
                    
                    if last_output:
                        print(last_output)
                    else:
                        print("The agent couldn't complete the request. Try rephrasing.")
                else:
                    print("The agent couldn't complete the request. Try rephrasing your question.")
            else:
                print(f"\n{output}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("💡 Tip: Try being more specific or check that Ollama is running")


if __name__ == "__main__":
    # Verify Ollama is running
    try:
        from agent import llm
        llm.invoke("test")
    except Exception as e:
        print("❌ Error: Make sure Ollama is running")
        print("💡 Run 'ollama serve' in another terminal")
        exit(1)
    
    main()

from langchain_core.messages import HumanMessage
def repl(app):
    print("LangGraph AI Assistant 📈 (type 'exit' to quit)")
    print("-" * 50)
    print("""
    Try asking quantitative questions like:
        - Are there more images than videos or audio in the collections?
        - What is the most common creator variant?
        - How many works are there by work type?
        - What embedding models were used to generate the embeddings for the collections? How many works were generated with each model?
    
    Or qualitative questions like:
        - Can you show me works about Willie Mays?
        - Which musicians played the Berkeley Folk Music Festival?
        - What kinds of food could you order on a transantlantic flight during the golden age of air travel?
    """)
    
    while True:
        # Get user input
        user_input = input("\nUser: ").strip()
        
        # Check for exit condition
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        # Skip empty inputs
        if not user_input:
            continue
            
        # Process the user's question
        response = app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": 42}},
        )
        
        # Print the AI's response
        print("\nAssistant:", response["messages"][-1].content)
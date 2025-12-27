from crewai import Task, Crew
from agents.sales_agent import sales_agent
import os
from dotenv import load_dotenv

load_dotenv()

print("=== Loan Application System ===")
print("Type 'exit' or 'quit' to end the conversation\n")

# Store conversation history
conversation_history = []

while True:
    # Get customer input
    customer_query = input("Customer: ")
    
    # Exit condition
    if customer_query.lower() in ['exit', 'quit', 'bye']:
        print("Agent: Thank you for your time! Have a great day!")
        break
    
    # Add to history
    conversation_history.append(f"Customer: {customer_query}")
    
    # Build context from history
    context = "\n".join(conversation_history[-5:])  # Keep last 5 exchanges
    
    # Define task with conversation context
    sales_task = Task(
        description=f"""Previous conversation:
{context}

Customer's latest message: "{customer_query}"
    
Your job:
1. Respond naturally to their message
2. Gather loan information if not already collected (amount, purpose, income, employment)
3. Keep the conversation flowing
4. If you have all the information, provide a summary

Be conversational and helpful.""",
        agent=sales_agent,
        expected_output="A natural conversational response"
    )
    
    # Create and run crew
    crew = Crew(
        agents=[sales_agent],
        tasks=[sales_task],
        verbose=False
    )
    
    result = crew.kickoff()
    
    # Add agent response to history
    conversation_history.append(f"Agent: {result}")
    
    print(f"\nAgent: {result}\n")
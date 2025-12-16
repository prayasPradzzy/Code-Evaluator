import streamlit as st
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import google.generativeai as genai
import os
from dotenv import load_dotenv
import operator

# Load environment variables from .env file
load_dotenv()

# Graph State Definition
class GraphState(TypedDict):
    code: str
    time_result: dict
    space_result: dict
    readability_result: dict
    final_summary: str
    average_score: float

# Initialize Gemini Model
def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Please set GOOGLE_API_KEY environment variable")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

# Evaluator Nodes
def evaluate_time_complexity(state: GraphState) -> GraphState:
    llm = get_llm()
    prompt = f"""Analyze the time complexity of this C++ code. Provide:
1. Brief feedback (2-3 sentences)
2. Score from 0-10 (10 = optimal)

Code:
{state['code']}

Format: Feedback: <text>
Score: <number>"""
    
    response = llm.generate_content(prompt).text
    feedback = response.split("Score:")[0].replace("Feedback:", "").strip()
    score = float(response.split("Score:")[1].strip().split()[0])
    
    state['time_result'] = {"feedback": feedback, "score": score}
    return state

def evaluate_space_complexity(state: GraphState) -> GraphState:
    llm = get_llm()
    prompt = f"""Analyze the space complexity of this C++ code. Provide:
1. Brief feedback (2-3 sentences)
2. Score from 0-10 (10 = optimal)

Code:
{state['code']}

Format: Feedback: <text>
Score: <number>"""
    
    response = llm.generate_content(prompt).text
    feedback = response.split("Score:")[0].replace("Feedback:", "").strip()
    score = float(response.split("Score:")[1].strip().split()[0])
    
    state['space_result'] = {"feedback": feedback, "score": score}
    return state

def evaluate_readability(state: GraphState) -> GraphState:
    llm = get_llm()
    prompt = f"""Analyze the readability of this C++ code (naming, structure, clarity). Provide:
1. Brief feedback (2-3 sentences)
2. Score from 0-10 (10 = excellent)

Code:
{state['code']}

Format: Feedback: <text>
Score: <number>"""
    
    response = llm.generate_content(prompt).text
    feedback = response.split("Score:")[0].replace("Feedback:", "").strip()
    score = float(response.split("Score:")[1].strip().split()[0])
    
    state['readability_result'] = {"feedback": feedback, "score": score}
    return state

def aggregate_results(state: GraphState) -> GraphState:
    time_score = state['time_result']['score']
    space_score = state['space_result']['score']
    readability_score = state['readability_result']['score']
    
    avg_score = (time_score + space_score + readability_score) / 3
    
    summary = f"""**Overall Analysis:**
- Time Complexity: {time_score}/10
- Space Complexity: {space_score}/10
- Readability: {readability_score}/10

The code demonstrates {'excellent' if avg_score >= 8 else 'good' if avg_score >= 6 else 'moderate'} quality overall."""
    
    state['final_summary'] = summary
    state['average_score'] = avg_score
    return state

# Build LangGraph Workflow
def create_workflow():
    from langgraph.graph import START
    
    workflow = StateGraph(GraphState)
    
    # Add all nodes
    workflow.add_node("time_eval", evaluate_time_complexity)
    workflow.add_node("space_eval", evaluate_space_complexity)
    workflow.add_node("readability_eval", evaluate_readability)
    workflow.add_node("aggregator", aggregate_results)
    
    # Sequential execution to avoid state conflicts
    workflow.add_edge(START, "time_eval")
    workflow.add_edge("time_eval", "space_eval")
    workflow.add_edge("space_eval", "readability_eval")
    workflow.add_edge("readability_eval", "aggregator")
    workflow.add_edge("aggregator", END)
    
    return workflow.compile()

# Streamlit UI
def main():
    st.set_page_config(page_title="C++ Code Evaluator", page_icon="🔍", layout="wide")
    
    st.title("🔍 Parallel C++ Code Evaluator")
    st.markdown("Evaluate your C++ code using parallel AI analysis powered by Google Gemini")
    
    # Code input
    code_input = st.text_area(
        "Enter your C++ code:",
        height=300,
        placeholder="Paste your C++ code here...",
        value="""int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}"""
    )
    
    # Evaluate button
    if st.button("🚀 Evaluate Code", type="primary"):
        if not code_input.strip():
            st.warning("Please enter some C++ code to evaluate")
            return
        
        with st.spinner("Analyzing code in parallel..."):
            try:
                # Create workflow and run
                app = create_workflow()
                initial_state = {
                    "code": code_input,
                    "time_result": {},
                    "space_result": {},
                    "readability_result": {},
                    "final_summary": "",
                    "average_score": 0.0
                }
                
                result = app.invoke(initial_state)
                
                # Display results
                st.success("✅ Evaluation Complete!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("⏱️ Time Complexity")
                    st.write(result['time_result']['feedback'])
                    st.metric("Score", f"{result['time_result']['score']}/10")
                
                with col2:
                    st.subheader("💾 Space Complexity")
                    st.write(result['space_result']['feedback'])
                    st.metric("Score", f"{result['space_result']['score']}/10")
                
                with col3:
                    st.subheader("📖 Readability")
                    st.write(result['readability_result']['feedback'])
                    st.metric("Score", f"{result['readability_result']['score']}/10")
                
                st.divider()
                
                # Final summary
                st.subheader("📊 Final Summary")
                st.markdown(result['final_summary'])
                
                # Average score with color coding
                avg = result['average_score']
                color = "green" if avg >= 7 else "orange" if avg >= 5 else "red"
                st.markdown(f"### Average Score: <span style='color:{color}; font-size:2em;'>{avg:.2f}/10</span>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error during evaluation: {str(e)}")
                st.info("Make sure your GOOGLE_API_KEY environment variable is set correctly")

if __name__ == "__main__":
    main()

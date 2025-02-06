import openai
import dotenv
import os
import streamlit as st

# Load environment variables and set up OpenAI
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_description(user_input):
    prompt = f"""
    You are an AI assisting with a VEX Robotics engineering notebook. 
    The user will provide a description of their work for the day.
    Break the description into the following sections. 
    You may not need to use some of these sections, but you should use as many as possible.
    Try to highlight how the design process is used.
    This is one entry.
    Please create one entry per objective discussed in the description. 
    The following sections ARE required as they are a part of the engineering design process:
    - Define the Problem
    - Research
    - Specify Requirements
    - Brainstorm Solutions
    - Build Prototype
    - Evaluate Prototype
    - Implement Prototype or Iterate
    *note: the following sections should be inplemented into previous sections as visual proof of the design process. They are optional*
    - Images
    - Code Snippets

    If any section is missing, prompt the user for more details.

    user input: {user_input}

    Return the structured response.
    """

    client = openai.Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Create the Streamlit interface
def main():
    st.title("VEX Robotics Notebook Generator")
    st.write("Enter your work description below and get a structured notebook entry.")

    # Create the main text input
    user_input = st.text_area("Describe today's work:", height=200)

    # Create a button to generate the response
    if st.button("Generate Notebook Entry"):
        if user_input:
            with st.spinner("Generating structured entry..."):
                structured_response = analyze_description(user_input)
                st.markdown("### Structured Notebook Entry:")
                st.markdown(structured_response)
        else:
            st.warning("Please enter a description of your work.")

    # Add a section for additional details
    st.markdown("### Additional Details")
    additional_details = st.text_area("Add any additional details here:", height=100)
    if st.button("Add Additional Details"):
        if additional_details:
            with st.spinner("Updating entry..."):
                combined_input = f"{user_input}\n\nAdditional details:\n{additional_details}"
                updated_response = analyze_description(combined_input)
                st.markdown("### Updated Notebook Entry:")
                st.markdown(updated_response)

if __name__ == "__notebook-vrc-generator-inpythonfile__":
    main()

#test_response = analyze_description("today, we rebuilt the triangle bracing of the conveyor tower. this fixed bending of the conveyor tower. additionally, we changed the piston position of the doinker, which helped add consistency since the old position was poorly mounted. additionally, this new position allowed the rubber band to fully keep it retracted. we also added a chain tensioner for the main conveyor which also served as more much needed bracing. now we need to adjust the clamp to allign with the conveyor because of the new tensioner")
#print(test_response)
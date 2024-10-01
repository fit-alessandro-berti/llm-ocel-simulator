import streamlit as st
import io
import sys
import os
from simulator import simulate_process

# Function to capture print statements
class StreamCapture(io.StringIO):
    def __init__(self):
        super().__init__()
        self.output = ""

    def write(self, s):
        super().write(s)
        self.output += s

    def get_output(self):
        return self.output

# Streamlit app layout
st.title("Process Simulation Interface")

with st.form("simulation_form"):
    target_process = st.text_input("Target Process (optional):")
    api_key = st.text_input("API Key:", type="password")
    desc_model = st.text_input("Description Generation Model:", value="gpt-4o-2024-08-06")
    sim_model = st.text_input("Simulation Generation Model:", value="o1-preview-2024-09-12")
    output_file = st.text_input("Output File Name:", value="output.xml")
    submitted = st.form_submit_button("Run Simulation")

# Placeholder for output
output_area = st.empty()

if submitted:
    if not api_key:
        st.error("API Key is required to run the simulation.")
    else:
        # Capture print statements
        capture = StreamCapture()
        sys.stdout = capture
        sys.stderr = capture

        with st.spinner("Running simulation..."):
            try:
                simulate_process(
                    target_process=target_process,
                    api_key=api_key,
                    description_generation_model=desc_model,
                    simulation_generation_model=sim_model,
                    output_file=output_file
                )
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                # Restore stdout and stderr
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

        # Display the captured output
        output_area.text(capture.get_output())

        st.success("Simulation completed.")

        # Check if the output file exists and provide a download link
        if os.path.exists(output_file):
            with open(output_file, "rb") as file:
                btn = st.download_button(
                    label="Download Output File",
                    data=file,
                    file_name=output_file,
                    mime="application/octet-stream"
                )
        else:
            st.error(f"Output file '{output_file}' not found.")
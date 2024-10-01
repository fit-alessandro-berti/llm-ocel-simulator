import requests
import traceback
import os


def make_api_call(prompt, api_key, api_model) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": api_model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    content = r.json()["choices"][0]["message"]["content"]

    return content


def simulate_process(target_process, api_key, description_generation_model, simulation_generation_model, output_file="output.xml", simulation_script="simulation.py"):
    F = open("target_process.txt", "w")
    F.write(target_process)
    F.close()

    process_description_request = "Generate a description of real-life process with many different object types and high degree of variability, batching, synchronization, and workarounds. describe everything in detail."

    process_simulation_generation_request = """
    The OCEL object in pm4py is stored in the class OCEL contained in pm4py.objects.ocel.obj

    In the pm4py process mining library, the OCEL class is a collection of different dataframes, containing at least the following columns:
    The constructor of OCEL objects is __init__(self, events=None, objects=None, relations=None, globals=None, parameters=None, o2o=None, e2e=None,
                 object_changes=None)


    ocel.events
     #   Column          Non-Null Count  Dtype
    ---  ------          --------------  -----
     0   ocel:eid        23 non-null     string
     1   ocel:timestamp  23 non-null     datetime64[ns, UTC]
     2   ocel:activity   23 non-null     string

    ocel.objects
    #   Column     Non-Null Count  Dtype
    ---  ------     --------------  -----
     0   ocel:oid   15 non-null     string
     1   ocel:type  15 non-null     string

    ocel.relations 
     #   Column          Non-Null Count  Dtype
    ---  ------          --------------  -----
     0   ocel:eid        39 non-null     string
     1   ocel:activity   39 non-null     string
     2   ocel:timestamp  39 non-null     datetime64[ns, UTC]
     3   ocel:oid        39 non-null     string
     4   ocel:type       39 non-null     string
     5   ocel:qualifier  0 non-null      object


    The 'ocel.relations' dataframe contains the many-to-many relationships between events and objects (E2O). An event can be related to different objects of different object types. The relationship can be qualified (i.e., described by a qualifier).

    Moreover, there is an ocel.o2o dataframe containing the object to object (O2O) relationships. Also these relationships can be qualified.


     #   Column          Non-Null Count  Dtype
    ---  ------          --------------  -----
     0   ocel:oid        0 non-null      string
     1   ocel:oid_2      0 non-null      string
     2   ocel:qualifier  0 non-null      string


    Could you create a Python script to simulate an object-centric event log?
    Please include at least 30 different activities in the object-centric event log and at least 6 different object types.
    Please include at least 5000 events and 5000 objects.

    The result should be stored in the "ocel" variable.

    Include attributes at the events and objects level.
    Include different types of behavior, including batching, synchronization, and workarounds.
    Include a high degree of variability in the object-centric event log.

    <ProcessDescription>
    !!REPLACE HERE!!
    </ProcessDescription>

    The object-centric event log should resemble a real-life process. The activities and object types should have realistic names.
    Please also include the following lines at the end of the script, to clean it up and export it as an OCEL 2.0 file


    import pm4py
    from pm4py.objects.ocel.util import ocel_consistency
    from pm4py.objects.ocel.util import filtering_utils

    ocel = ocel_consistency.apply(ocel)
    ocel = filtering_utils.propagate_relations_filtering(ocel)

    pm4py.write_ocel2(ocel, "output.xml")
    
    
    
    After the script, include a <description> XML tag containing the textual description of the simulated process model
    (for non-technical process analysts).
    """

    if target_process:
        process_description_request += "\n\nPlease focus on the following process: " + target_process

    print("\n\n")
    print(process_description_request)

    print("\n\n== Generating Process Description ==\n\n")

    process_description = make_api_call(process_description_request, api_key=api_key,
                                        api_model=description_generation_model)

    process_description = process_simulation_generation_request.replace("!!REPLACE HERE!!", process_description)
    process_description = process_description.replace("output.xml", output_file)

    F = open("process_description.txt", "w")
    F.write(process_description)
    F.close()

    print(process_description)

    print("\n\n== Generating Process Simulation ==\n\n")

    try:
        process_simulation = make_api_call(process_description, api_key=api_key, api_model=simulation_generation_model)
        print(process_simulation)
        process_simulation = process_simulation.split("```python")[1].split("```")[0]
        F = open(simulation_script, "w")
        F.write(process_simulation)
        F.close()
        os.system("python "+simulation_script)
    except:
        traceback.print_exc()


if __name__ == "__main__":
    API_KEY = open("api_key.txt", "r").read().strip()
    DESCRIPTION_GENERATION_MODEL = "gpt-4o-2024-08-06"
    SIMULATION_GENERATION_MODEL = "o1-preview-2024-09-12"

    target_process = input("Target process (possibly empty if you don't know)  ->  ")

    simulate_process(target_process, api_key=API_KEY, description_generation_model=DESCRIPTION_GENERATION_MODEL, simulation_generation_model=SIMULATION_GENERATION_MODEL, output_file="output.xml")

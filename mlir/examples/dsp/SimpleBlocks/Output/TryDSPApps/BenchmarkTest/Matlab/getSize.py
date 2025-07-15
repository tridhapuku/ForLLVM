import os
import subprocess
import pandas as pd
# The script does the following
# Input : filename
# Output : TimeOfExecution for different IP sizes :
# Steps to run:
# Open a terminal at the path of the script --
# Run: python ScriptForCases #3.11 validated

# Pseudo-code:
# Iterate for all the input-size & update the input value in file
# Update logic -- change the 2nd parameter of line: var c = getRangeOfVector(init , Count, StepSize)
# Run the respective commands on the file

# Path to the input file
# Apps = "noiseCancelling.m" , "echoCancelling.m", "periodogram.m", "lowPassFull.m", "hearingAid.m", "lowPassFIRFilterDesign", "energyOfSignal", "audioEqualizer", "audioCompression","vibrationAnalysis", "underWaterCommunication", "voiceActivityDetection", "signalSmoothing", "targetDetection", "biomedicalSignalProcessing"
input_files = ["audioCompression", "biomedicalSignalProcessing", "dtmfDetection", "lowPassFIRFilterDesign", "noisecancelling", \
"radarSignalProcessing", "signalSmoothing", "speakerIdentification", "targetDetection", "vibrationAnalysis", "audioEqualizer", \
"digitalModulation", "echocancelling", "hearingAid", "lowPassFull", "periodogram2Conv1", "spaceCommunication", "spectralAnalysis", \
"underWaterCommunication", "voiceActivityDetection"]
data = []

for input_file in input_files:
    input_file_path = input_file + ".m"
    BasePathForLLVM = "/home/local/ASURITE/megan/ForLLVM/"
    OutputScriptPath = "mlir/examples/dsp/SimpleBlocks/Output/TryDSPApps/BenchmarkTest/Matlab/"
    mcc_path ="/home/local/ASURITE/apkhedka/Matlab_Installation/bin/mcc"
    mrt_path ="/home/local/ASURITE/apkhedka/Matlab_Runtime/R2024b/"
    # OutputPath = BasePathForLLVM + "mlir/examples/dsp/SimpleBlocks/Output/TryDSPApps/Results/TryResultScript/Output/"
    print(f"Running Application {input_file_path}")
    # Construct full output path
    OutputPath = os.path.join(BasePathForLLVM, OutputScriptPath, "Output")

    # Check if the Output folder exists, create it if it doesn't
    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)


    def delete_folder_contents(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    try:
        with open(input_file_path, "r") as file:
            lines = file.readlines()
    except:
        continue

    print("", end="\t")

    size_test = {"100M": 100000000}
    for key, value in size_test.items():
        # Update the specific line in the file
        # print("Updating for {}".format(value))
        print("\n{}".format(key), end="\t")
        with open(input_file_path, "w") as file:
            for line in lines:
                if line.strip().startswith("INPUT_LENGTH = "):
                    updated_line = f"INPUT_LENGTH = {value};\n"
                    file.write(updated_line)
                else:
                    file.write(line)

        command = f"{mcc_path} -m {input_file_path} -d 'Output/' -o {input_file}{key}"
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        command2 = f"size ./Output/{input_file}{key}"

        # Execute the command
        try:
            result = subprocess.run(
                    command2,
                    shell=True,
                    capture_output=True, text=True
                    )
            
            output_parts = result.stdout.splitlines()
            if len(output_parts) > 1:
                size_data = output_parts[1].split()

                data.append({
                    "filename": input_file_path,
                    # "input size" : key,
                    # "text": size_data[0],
                    # "data": size_data[1],
                    # "bss": size_data[2],
                    # "dec": size_data[3],
                    # "hex": size_data[4],
                    "total": sum(map(int, size_data[:4]))
                })
        except subprocess.CalledProcessError as exc:
            print(
                    f"Process failed because did not return a successful return code. "
                    f"Returned {exc.returncode}\n{exc}"
                    )

    df = pd.DataFrame(data)
    
    df.to_csv("codesize.csv", index=False)

    delete_folder_contents("./Output")



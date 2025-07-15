import os
import subprocess
import pandas as pd

# The script does the following
# Input : filename.c
# Output : TimeOfExecution for different IP sizes :
# Steps to run:
# Open a terminal at the path of the script --
# Run: python ScriptForCases.c #3.11 validated

# Pseudo-code:
# Iterate for all the input-size & update the input value in file
# Update logic -- change the 2nd parameter of line: var c = getRangeOfVector(init , Count, StepSize)
# Run the respective commands on the file

# Path to the input file
# Apps = "lowPassFIRFilterDesign.c", "noisecancelling.c" , "echocancelling.c",  "hearingAid.c", "audioEqualizer.c", "vibrationAnalysis.c", "underWaterCommunication.c", "voiceActivityDetection.c", "signalSmoothing",  "targetDetection", "biomedicalSignalProcessing", "periodogram2Conv", "spaceCommunication", "dtmfDetection"
input_files = ["audioCompression.c", "biomedicalSignalProcessing.c", "dtmfDetection.c", "lowPassFIRFilterDesign.c", "noisecancelling.c", \
"radarSignalProcessing.c", "signalSmoothing.c", "speakerIdentification.c", "targetDetection.c", "vibrationAnalysis.c", "audioEqualizer.c", \
"digitalModulation.c", "echocancelling.c", "hearingAid.c", "lowPassFull.c", "periodogram2Conv1.c", "spaceCommunication.c", "spectralAnalysis.c", \
"underWaterCommunication.c", "voiceActivityDetection.c"]
data = []

for input_file_path in input_files:
    BasePathForLLVM = "/home/local/ASURITE/megan/ForLLVM/"
    OutputScriptPath = "mlir/examples/dsp/SimpleBlocks/Output/TryDSPApps/BenchmarkTest/CCode/"
    # OutputPath = BasePathForLLVM + "mlir/examples/dsp/SimpleBlocks/Output/TryDSPApps/Results/TryResultScript/Output/"
    print(f"Running Application {input_file_path}")
    # Construct full output path
    OutputPath = os.path.join(BasePathForLLVM, OutputScriptPath, "Output")

    # Check if the Output folder exists, create it if it doesn't
    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)

    # Now OutputPath is ready for use
    print("InputPath:{}".format(BasePathForLLVM))
    print(f"OutputPath: {OutputPath}")
    # exit()

    # ************ Don't change unless u required
    # Define the values dictionary
    inputValues = {
        "10": 10,
        "100": 100,
        "1K": 1000,
        "10K": 10000,
        "20K": 20000,
        "30K": 30000,
        "40K": 40000,
        "50K": 50000,
        "100K": 100000,
        "1M": 1000000,
        "10M": 10000000,
        "20M": 20000000,
        "30M": 30000000,
        "40M": 40000000,
        "50M": 50000000,
        "100M": 100000000,
        # "1B": 1000000000
    }
    NoOfIterations = 3


    # Define the cases
    cases = [
        {
            "gcc": True,
            "clang": False,
            "exe": "fileGCCOptExe",
        },
        {
            "clang": True,
            "gcc": False,
            "exe": "fileClangOptExe",
        },
    ]

    try:
        with open(input_file_path, "r") as file:
            lines = file.readlines()
    except:
        continue

    print("", end="\t")

    for case in cases:
        print(f"{case['exe']}", end="\t")

    size_test = {"100M": 100000000}
    for key, value in size_test.items():
        # Update the specific line in the file
        # print("Updating for {}".format(value))
        print("\n{}".format(key), end="\t")
        with open(input_file_path, "w") as file:
            for line in lines:
                if line.strip().startswith("#define INPUT_LENGTH"):
                    updated_line = f"#define INPUT_LENGTH {value}\n"
                    file.write(updated_line)
                else:
                    file.write(line)

        for case in cases:
            
            test_size = 0
            gcc_flag = ["O3", "Os"]
            clang_flag = ["O3", "Oz"]
            if case["gcc"]:
                command = f"gcc -{gcc_flag[test_size]} -o {OutputPath}/{case['exe']} {input_file_path} -lm", # -Os
            if case["clang"]:
                command = f"clang-17 -{clang_flag[test_size]} {input_file_path} -o {OutputPath}/{case['exe']} -lm", # -Oz
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            command2 = f"size ./Output/{case['exe']}"

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
                        "opt": case['exe'],
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
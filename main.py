def extract_transfers_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    model_data = []
    current_model = {}
    capture_phase = False

    #Include your elements here, str.
    elements = [ ]
    
    model_number = 0
    for line in lines:
        if "Phase mole transfers:" in line:
            if current_model:
                model_data.append(current_model)
            model_number += 1
            current_model = {"Model Number": model_number}
            capture_phase = True
        elif "Redox mole transfers:" in line:
            capture_phase = True
        elif capture_phase:
            match = re.match(r'^\s*(\S+)\s+([-]?\d*\.\d+[eE][-+]?\d+|\d*\.\d+)', line)
            if match:
                name, value = match.groups()
                if name in elements:
                    current_model[name] = value
            else:
                if line.strip() == '':
                    capture_phase = False

    if current_model:
        model_data.append(current_model)
    
    df = pd.DataFrame(model_data, columns=["Model Number"] + elements)
    return df

def main():
    # Input file path
    txt_file_path = input("Enter the path to the input text file: ")
    if not txt_file_path:
        print("No file path provided. Exiting.")
        return
    
    # Output file path
    output_file_path = input("Enter the path to save the output Excel file: ")
    if not output_file_path:
        print("No file path provided. Exiting.")
        return

    df = extract_transfers_from_file(txt_file_path)
    
    df.to_excel(output_file_path, index=False)
    print(f"Data successfully saved to {output_file_path}")

if __name__ == "__main__":
    main()

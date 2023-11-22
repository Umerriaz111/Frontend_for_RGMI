import os
import re
import pandas as pd
import random




study_id = []
subject_id = []
ref_id = []
question_type = []
question = []
answer = []
split = []

def extract_findings(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        # Use regular expression to find the "FINDINGS" portion
        match = re.search(r'FINDINGS:(.*?)IMPRESSION:', content, re.DOTALL)
        if match:
            findings = match.group(1).strip()
            return findings
        else:
            return "There is no abnormality or fracture found in the given X-ray image so the patient is absolutely fit."

def process_folders(root_folder,df2):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                study_id.append(file_path.split("\\")[-1].split(".")[0][1:])
                subject_id.append(file_path.split("\\")[2][1:])
                ref_id.append(0)
                question_type.append('report')
                indx = random.randint(1, len(df2) - 2)

                question.append(df2['Questions'][indx])
                split.append("train")
                findings = extract_findings(file_path)

                if findings:
                    answer.append(findings)




def main():
    df = pd.read_csv('mimic_pair_questions2.csv')
    df2 = pd.read_csv('findings_Questions.csv')

    # Replace 'files' with the actual path to your 'files' folder
    root_directory = r'files/files'
    process_folders(root_directory, df2)
    data={
        "study_id": study_id,
        "subject_id": subject_id,
        "ref_id": ref_id,
        "question_type": question_type,
        "question": question,
        "answer": answer,
        "split": split
    }
    df_created = pd.DataFrame(data)
    df = pd.concat([df, df_created])
    df['study_id'] = pd.to_numeric(df['study_id'], errors='coerce')
    df = df.sort_values('study_id')
    df.to_csv('mimic_pair_questions2.csv', index=False)
if __name__ == '__main__':
    main()
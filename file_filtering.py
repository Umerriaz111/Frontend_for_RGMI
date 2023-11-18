import pandas as pd
import os



def extract_QA_row_for_each_folder(folder_names, data):
    # Filter rows based on folder names
    filtered_data = data[data['subject_id'].astype(str).isin(folder_names)]

    # Display the filtered data
    print(filtered_data.head(2))
    filtered_data.to_csv('mimic_pair_questions2.csv', index=False)



def extract_path_from_csv(partial_path, df):
    # Filter the DataFrame based on the partial path match
    first = True
    for path in partial_path:
        # path- path to each report
        filtered_df = df[df['study_id'].str.contains(path)]
        # Save the filtered DataFrame back to a CSV file
        if first:
            # if running for the first time to avoid the header again and again
            filtered_df.to_csv('record_list2.csv', index=False)
            first = False
            continue
        filtered_df.to_csv('mimic_pair_questions2.csv', mode='a', index=False, header=not os.path.exists('study_list2.csv'))


def main():
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('csr_record_list.csv') #(downloaded from https://physionet.org/content/mimic-cxr/2.0.0/#files-panel)
    print(df.head(2))

    # Define the partial string you want to match in the 'path' column
    partial_path = [r'files/p10/p10000032',r'files/p10/p10000764',r'files/p10/p10000898',r'files/p10/p10000935',r'files/p10/p10000980',r'files/p10/p10001038',r'files/p10/p10001122',r'files/p10/p10001176',r'files/p10/p10001217',r'files/p10/p10001401']
    extract_path_from_csv(partial_path, df)


    # Load the CSV file into a pandas DataFrame
    data = pd.read_csv('mimic_pair_questions.csv') #(downloaded from https://physionet.org/content/medical-diff-vqa/1.0.0/)
    print(data.head(2))
    # List of folder names
    folder_names = ['10000032', '10000764', '10000898','10000935','10000980','10001038','10001122','10001176','10001217','10001401']  # folder names/patient ids
    extract_QA_row_for_each_folder(folder_names, data)
if __name__ == '__main__':
    main()
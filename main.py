import json

import pandas as pd

from dataset import createDataset

def main():
    # df = pd.read_json("./data/project_details.json")
    # df['description'].fillna("", inplace=True)
    # checkTagNDescription(df)

    # merge_json_files("data/project_details.json", "data/project_details_v1.json", "data/project_details_merged_v1.json")

    all_issues_data = []
    df = pd.read_json("../../../PycharmProjects/cps-bug-analysis/data/project_details_merged_v1.json")
    for link in df["source_link"].head(3):
        print(link)
        all_issues_data.append(createDataset(link))

    with open("../../../PycharmProjects/cps-bug-analysis/data/github_open_issues.json", "w") as json_file:
        json.dump(all_issues_data, json_file, indent=4)
    print("Open and closed issues data along with comments has been scraped and stored in 'github_issues.json'.")


def checkTagNDescription(df):
    for index, row in df.iterrows():
        tags = row['tags']
        desc = row['description']
        if "cyber-physical-systems" not in tags:
            print(f'Index: {index}, Value: {row['project_name']}')

        if type(desc) is not type(""):
            print(f'Index: {index}, Value: {desc}')


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from itertools import combinations

st.set_page_config(page_title="De-duplication App", layout="wide")
st.title("🔍 Data De-duplication Tool")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    if all(col in df.columns for col in ['name', 'email']):
        threshold = st.slider("Set Name Similarity Threshold", 70, 100, 85)

        # Identify potential duplicates
        dupes = []
        for (i, row1), (j, row2) in combinations(df.iterrows(), 2):
            name_score = fuzz.token_sort_ratio(str(row1['name']), str(row2['name']))
            email_match = row1['email'] == row2['email']

            if name_score >= threshold and email_match:
                dupes.append((row1['id'], row2['id'], name_score))

        if dupes:
            st.subheader("🔁 Potential Duplicates")
            dupe_df = pd.DataFrame(dupes, columns=["Record 1", "Record 2", "Name Similarity"])
            st.dataframe(dupe_df)

            def merge_duplicates(df, pairs):
                merged_ids = set()
                master_records = []

                for id1, id2, _ in pairs:
                    if id1 in merged_ids or id2 in merged_ids:
                        continue
                    merged_ids.update([id1, id2])

                    master = df[df['id'] == min(id1, id2)].iloc[0].to_dict()
                    master_records.append(master)

                others = df[~df['id'].isin(merged_ids)]
                master_df = pd.DataFrame(master_records)
                return pd.concat([master_df, others], ignore_index=True)

            clean_df = merge_duplicates(df, dupes)
            st.subheader("✅ De-duplicated Data")
            st.dataframe(clean_df)

            csv = clean_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Cleaned CSV", csv, "deduplicated_data.csv", "text/csv")
        else:
            st.info("No duplicates found with the current threshold.")
    else:
        st.error("The uploaded file must include at least 'id', 'name', and 'email' columns.")

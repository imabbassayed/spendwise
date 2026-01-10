import streamlit as st
import pandas as pd
import sys
import os

# Add root directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config


def category_manager():
    # Initialize only once, building DataFrame from list of dicts
    if "categories_df" not in st.session_state:
        st.session_state.categories_df = pd.DataFrame(config.DEFAULT_CATEGORIES)

    df = st.session_state.categories_df.copy()

    # Editable table for user to modify categories + priorities
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Category": st.column_config.TextColumn("Category"),
            "Priority": st.column_config.SelectboxColumn(
                "Priority",
                options=config.PRIORITY_OPTIONS
            ),
        },
    )

    # Ensure both columns exist even if user edits structure
    if "Category" not in edited_df.columns:
        edited_df["Category"] = ""

    if "Priority" not in edited_df.columns:
        edited_df["Priority"] = "Should Keep"

    # Strip whitespace & clean invalid entries
    edited_df["Category"] = (
        edited_df["Category"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Remove empty rows
    cleaned_df = edited_df[edited_df["Category"] != ""]

    # Reset index for consistency
    cleaned_df = cleaned_df.reset_index(drop=True)

    # Update session state immediately after any changes
    if not cleaned_df.equals(st.session_state.categories_df):
        st.session_state.categories_df = cleaned_df
        st.rerun()

    return cleaned_df
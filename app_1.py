import streamlit as st
import pandas as pd

from explainability import analyze
from model_loader import model, tokenizer, device


# Store analyzed items
if "reviewed_items" not in st.session_state:
    st.session_state.reviewed_items = []


st.title("Misinformation Detection - Review Dashboard")

st.subheader("Submit an article or headline")


text_input = st.text_area(
    "Text to analyze",
    height=100
)


if st.button("Analyze"):

    if text_input.strip() == "":
        st.warning("Please enter some text first.")

    else:

        result = analyze(
            text_input,
            model,
            tokenizer,
            device,
            no_of_words=6
        )

        # Add dashboard information
        result["text"] = text_input
        result["status"] = "pending"

        # Save result
        st.session_state.reviewed_items.append(result)

        st.success(
            f"Analyzed. Prediction: "
            f"{result['prediction']} "
            f"({result['confidence']:.1%} confidence)"
        )


st.subheader("Flagged items (ranked by confidence)")


if len(st.session_state.reviewed_items) == 0:

    st.info(
        "No items analyzed yet. Submit something above."
    )

else:

    table_rows = []

    for i, item in enumerate(
        st.session_state.reviewed_items
    ):

        table_rows.append({
            "index": i,
            "text": item["text"][:60] + (
                "..." if len(item["text"]) > 60 else ""
            ),
            "prediction": item["prediction"],
            "confidence": item["confidence"],
            "status": item["status"]
        })


    table_df = pd.DataFrame(table_rows)


    # Fake / misinformation
    fake_items = (
        table_df[
            table_df["prediction"] == "fake"
        ]
        .sort_values(
            "confidence",
            ascending=False
        )
    )


    # Real
    real_items = (
        table_df[
            table_df["prediction"] == "real"
        ]
        .sort_values(
            "confidence",
            ascending=False
        )
    )


    st.subheader(
        "Flagged as likely misinformation"
    )

    if len(fake_items) == 0:

        st.write("None yet.")

    else:

        st.dataframe(
            fake_items,
            use_container_width=True
        )


    st.subheader(
        "Flagged as likely real"
    )

    if len(real_items) == 0:

        st.write("None yet.")

    else:

        st.dataframe(
            real_items,
            use_container_width=True
        )
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import io


def set_background(local_img_path):
    with open(local_img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    /* Main app background */
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Hide header and footer only, keep the three dots visible */
    header {{
        background: none;
    }}
    footer {{
        visibility: hidden;
    }}

 

    /* Optional: Add spacing for input fields */
    .stNumberInput {{
        margin-bottom: 10px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("Background.jpg")




# App title


st.markdown(
    '<h1 style="text-align: center;"><span style="background-color: rgba(255,255,255,0.7); padding: 4px; border-radius: 4px;">مخطط توزيع الأنماط البيئية للأسماك</span></h1>',
    unsafe_allow_html=True
)


st.markdown(
    '<h1 style="text-align: center;"><span style="background-color: rgba(255,255,255,0.7); padding: 4px; border-radius: 4px;">Ecotype Distribution</span></h1>',
    unsafe_allow_html=True
)






# Arabic Text (Right-Aligned)
# Add space before instructions
st.markdown("<br>", unsafe_allow_html=True)

# Arabic instruction
st.markdown(
    """
    <p style="text-align: right;">
        <span style="background-color: rgba(255,255,255,0.7); padding: 3px; border-radius: 3px;">
        :أدخل النسب المئوية لكل فئة من الأسماك ضمن المجموعات الثلاث
        </span>
    </p>
    """,
    unsafe_allow_html=True
)




# English instruction
st.markdown(
    '<p><span style="background-color: rgba(255,255,255,0.7); padding: 3px; border-radius: 3px;">Enter the percentages for each fish category within the three groups:</span></p>',
    unsafe_allow_html=True
)



# Define groups and fish categories
groups = ["Juvenile", "Migratory", "Resident"]
categories = [
    "أنثى مهاجرة",
    "أنثى خليط الجينات",
    "أنثى مقيمة",
    "ذكر مهاجر",
    "ذكر خليط الجينات",
    "ذكر مقيم"
]

# Create input fields with highlight box
data = {}
for group in groups:
    # Highlighted group heading
    st.markdown(
        f'<h3 style="text-align: left;"><span style="background-color: rgba(255,255,255,0.7); padding: 4px; border-radius: 4px;">{group} Group</span></h3>',
        unsafe_allow_html=True
    )

    group_data = {}
    total = 0
    for cat in categories:
        # Highlight box for label + input
        st.markdown(
            f"""
            <div style="background-color: rgba(255,255,255,0.7); padding: 8px; border-radius: 6px; margin-bottom: 8px;">
                <span style="font-weight: bold;">{cat}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Place the number input right after the box
        val = st.number_input("", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key=f"{group}_{cat}")
        group_data[cat] = val
        total += val

    if total != 100:
        st.warning(f"The total percentage for the ({group}) group is ({total}). It must be equal to 100%.")
        
    data[group] = group_data


# Convert to DataFrame
df = pd.DataFrame(data)

# Plot
st.subheader("📊 المخطط البياني")

fig, ax = plt.subplots(figsize=(6, 5))

colors = [
    "lightgrey",      # Female Migratory
    "grey",           # Female Heterozygote
    "dimgray",        # Female Resident
    "lightgrey",      # Male Migratory (dashed)
    "grey",           # Male Heterozygote (dashed)
    "dimgray"         # Male Resident (dashed)
]
hatches = [None, None, None, "//", "//", "//"]

bottom = [0, 0, 0]
for i, cat in enumerate(categories):
    values = df.loc[cat]
    ax.bar(groups, values, bottom=bottom, color=colors[i], hatch=hatches[i], edgecolor="black", label=cat)
    bottom = [sum(x) for x in zip(bottom, values)]

ax.set_ylim(0, 100)
ax.set_ylabel("Percent", fontsize=14, fontweight='bold')
ax.set_xlabel("Ecotype", fontsize=14, fontweight='bold', labelpad=15)

import arabic_reshaper
from bidi.algorithm import get_display

# Prepare Arabic labels for the legend in RTL
labels_rtl = [get_display(arabic_reshaper.reshape(cat)) for cat in categories]
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', labels=labels_rtl)

st.pyplot(fig)

# Save the figure to a BytesIO buffer
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
buf.seek(0)  # Move to the beginning of the buffer

# Download button
st.download_button(
    label="Download Graph as PNG",
    data=buf,
    file_name="ecotype_distribution.png",
    mime="image/png"
)
































































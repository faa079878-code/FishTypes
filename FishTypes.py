import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

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

    /* Hide top menu, header, and footer */
    #MainMenu {{visibility: hidden;}}
    header {{background: none;}}
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply background
set_background("Background.jpg")



# App title
st.title("مخطط توزيع الأنماط البيئية للأسماك (Ecotype Distribution)")

# Arabic Text (Right-Aligned)
st.markdown("""
<p style="text-align: right;">
    :أدخل النسب المئوية لكل فئة من الأسماك ضمن المجموعات الثلاث  
</p>
""", unsafe_allow_html=True)

# English Translation (Default Left-Aligned)
st.markdown("Enter the percentages for each fish category within the three groups:")

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

# Create input fields for each group
data = {}
for group in groups:
    st.subheader(f"{group} Group")
    group_data = {}
    total = 0
    for cat in categories:
        val = st.number_input(f"{cat} - {group}", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        group_data[cat] = val
        total += val

    # Check if total is 100
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








































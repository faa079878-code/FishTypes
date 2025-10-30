import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# App title
st.title("مخطط توزيع الأنماط البيئية للأسماك (Ecotype Distribution)")

st.markdown("""
أدخل النسب المئوية لكل فئة من الأسماك ضمن المجموعات الثلاث:
**اليافعة (Juvenile)**، **المهاجرة (Migratory)**، و**القاطنة (Resident)**.
""")

# Define groups and fish categories
groups = ["Juvenile", "Migratory", "Resident"]
categories = [
    "أنثى مهاجرة",
    "أنثى خليط الجينات",
    "أنثى قاطنة",
    "ذكر مهاجر",
    "ذكر خليط الجينات",
    "ذكر قاطن"
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
        st.warning(f"⚠️ مجموع النسب لمجموعة {group} هو {total}%. يجب أن يساوي 100%.")
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
ax.set_xlabel("Ecotype", fontsize=14, fontweight='bold')
import arabic_reshaper
from bidi.algorithm import get_display

# Prepare Arabic labels for the legend in RTL
labels_rtl = [get_display(arabic_reshaper.reshape(cat)) for cat in categories]
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', labels=labels_rtl)

st.pyplot(fig)











import streamlit as st
import pandas as pd

# Try importing matplotlib safely
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    st.error("❌ مكتبة Matplotlib غير مثبتة. يرجى إضافتها في ملف requirements.txt.")
    st.stop()

# --- App Title and Description ---
st.title("مخطط توزيع الأنماط البيئية للأسماك (Ecotype Distribution) 🐟")

st.markdown("""
هذا التطبيق يسمح لك بإدخال **النسب المئوية** لأنواع الأسماك المختلفة 
في ثلاث مجموعات بيئية رئيسية:
- **اليافعة (Juvenile)**  
- **المهاجرة (Migratory)**  
- **المقيمة (Resident)**  

وسيتم رسم مخطط بياني مكدس يعرض توزيع الأنواع داخل كل مجموعة.
""")

# --- Define Ecotypes and Categories ---
groups = ["Juvenile", "Migratory", "Resident"]
categories = [
    "أنثى مهاجرة (Light Grey)",
    "أنثى خليط الجينات (Grey)",
    "أنثى مقيمة (Dark Grey)",
    "ذكر مهاجر (Light Dashed Grey)",
    "ذكر خليط الجينات (Dashed Grey)",
    "ذكر مقيم (Dark Dashed Grey)"
]

# --- Create Input Fields ---
data = {}
st.divider()
st.subheader("🧮 إدخال البيانات")

for group in groups:
    st.markdown(f"### {group} Group")
    group_data = {}
    total = 0
    cols = st.columns(3)
    for i, cat in enumerate(categories):
        with cols[i % 3]:
            val = st.number_input(f"{cat} - {group}", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            group_data[cat] = val
            total += val

if total != 100:
data[group] = group_data

# --- Convert to DataFrame ---
df = pd.DataFrame(data)

# --- Plot Section ---
st.divider()
st.subheader("📊 المخطط البياني")

if df.sum().sum() == 0:
    st.info("أدخل القيم أعلاه لعرض المخطط.")
else:
    # Define visual style
    colors = [
        "lightgrey",    # Female Migratory
        "grey",         # Female Heterozygote
        "dimgray",      # Female Resident
        "lightgrey",    # Male Migratory (dashed)
        "grey",         # Male Heterozygote (dashed)
        "dimgray"       # Male Resident (dashed)
    ]
    hatches = [None, None, None, "//", "//", "//"]

    # Create the stacked bar chart
    fig, ax = plt.subplots(figsize=(7, 6))
    bottom = [0, 0, 0]

    for i, cat in enumerate(categories):
        values = df.loc[cat]
        ax.bar(groups, values, bottom=bottom, color=colors[i],
               hatch=hatches[i], edgecolor="black", label=cat)
        bottom = [sum(x) for x in zip(bottom, values)]

    ax.set_ylabel("النسبة المئوية (%)", fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_title("توزيع الأنماط البيئية للأسماك", fontsize=14, pad=15)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    plt.tight_layout()

    st.pyplot(fig)

st.divider()
st.caption("تم تطوير التطبيق لعرض توزيع الأنماط البيئية للأسماك بطريقة تفاعلية 🐠")

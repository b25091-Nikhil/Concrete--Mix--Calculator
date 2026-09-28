import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IS 10262:2019 Concrete Mix Design Calculator",
    page_icon="🏗️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 16px;
    margin-bottom: 25px;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border: 2px solid #2e7d32;
    margin-top: 15px;
    margin-bottom: 15px;
}

.ratio-box {
    padding: 25px;
    border-radius: 15px;
    background: #e8f5e9;
    border: 3px solid #2e7d32;
    text-align: center;
    margin: 20px 0;
}

.ratio-title {
    font-size: 22px;
    font-weight: 700;
    color: #1b5e20;
}

.ratio-value {
    font-size: 32px;
    font-weight: 800;
    color: #2e7d32;
}

.step-box {
    padding: 15px;
    border-left: 5px solid #2e7d32;
    background: #f7f7f7;
    border-radius: 8px;
    margin-bottom: 10px;
}

.graph-note {
    padding: 15px;
    background: #e8f5e9;
    border-left: 5px solid #2e7d32;
    border-radius: 8px;
    margin-top: 10px;
}

.warning-box {
    padding: 15px;
    background: #fff8e1;
    border-left: 5px solid #ff9800;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">IIT MANDI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Civil Engineering Department</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title"><b>Course: Civil Engineering Materials CE203</b></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="group-title">Group 5 | Nikhil | Neetesh | Nitya | Meet | Mohit | Amar</div>',
    unsafe_allow_html=True
)

st.divider()

st.title("🏗️ IS 10262:2019 Concrete Mix Design Calculator")


# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.header("⚙️ Mix Design Inputs")

grade = st.sidebar.selectbox(
    "Concrete Grade",
    [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
    index=6
)

exposure = st.sidebar.selectbox(
    "Exposure Condition",
    ["Mild", "Moderate", "Severe", "Very Severe", "Extreme"],
    index=2
)

cement_type = st.sidebar.selectbox(
    "Cement Type",
    ["PPC", "OPC 33", "OPC 43", "OPC 53"]
)

aggregate_size = st.sidebar.selectbox(
    "Maximum Nominal Aggregate Size (mm)",
    [10, 20, 40],
    index=1
)

zone = st.sidebar.selectbox(
    "Fine Aggregate Zone",
    ["I", "II", "III", "IV"],
    index=1
)

slump = st.sidebar.slider(
    "Slump (mm)",
    25,
    200,
    100,
    25
)

concrete_type = st.sidebar.selectbox(
    "Concrete Type",
    ["RCC", "PCC"]
)

st.sidebar.subheader("Material Properties")

sg_cement = st.sidebar.number_input(
    "Specific Gravity of Cement",
    min_value=2.5,
    max_value=3.5,
    value=3.15,
    step=0.01
)

sg_fa = st.sidebar.number_input(
    "Specific Gravity of Fine Aggregate",
    min_value=2.0,
    max_value=3.5,
    value=2.65,
    step=0.01
)

sg_ca = st.sidebar.number_input(
    "Specific Gravity of Coarse Aggregate",
    min_value=2.0,
    max_value=3.5,
    value=2.70,
    step=0.01
)

sg_sp = st.sidebar.number_input(
    "Specific Gravity of Superplasticizer",
    min_value=0.8,
    max_value=2.0,
    value=1.20,
    step=0.01
)

st.sidebar.subheader("Admixture")

use_sp = st.sidebar.checkbox(
    "Use Superplasticizer",
    value=True
)

if use_sp:

    sp_dosage = st.sidebar.number_input(
        "SP Dosage (% of cement)",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
        step=0.1
    )

    water_reduction = st.sidebar.number_input(
        "Water Reduction (%)",
        min_value=0.0,
        max_value=50.0,
        value=23.0,
        step=1.0
    )

else:

    sp_dosage = 0.0
    water_reduction = 0.0


st.sidebar.subheader("Aggregate Moisture")

ca_absorption = st.sidebar.number_input(
    "CA Absorption (%)",
    min_value=0.0,
    max_value=10.0,
    value=0.5,
    step=0.1
)

fa_absorption = st.sidebar.number_input(
    "FA Absorption (%)",
    min_value=0.0,
    max_value=10.0,
    value=1.0,
    step=0.1
)

ca_moisture = st.sidebar.number_input(
    "CA Surface Moisture (%)",
    min_value=0.0,
    max_value=20.0,
    value=0.0,
    step=0.1
)

fa_moisture = st.sidebar.number_input(
    "FA Surface Moisture (%)",
    min_value=0.0,
    max_value=20.0,
    value=0.0,
    step=0.1
)

volume = st.sidebar.number_input(
    "Concrete Volume (m³)",
    min_value=0.1,
    max_value=1000.0,
    value=1.0,
    step=0.1
)


# ============================================================
# STANDARD DEVIATION
# ============================================================

st.sidebar.subheader("Quality Control")

sd = st.sidebar.number_input(
    "Standard Deviation s (MPa)",
    min_value=1.0,
    max_value=15.0,
    value=5.0,
    step=0.1
)


# ============================================================
# TARGET MEAN STRENGTH
# ============================================================

# CE203 lecture uses:
# f_target = max(fck + 1.65s, fck + X)
#
# X = 6.5 MPa is used in the M40 lecture example.

X = 6.5

target_1 = grade + 1.65 * sd
target_2 = grade + X

target_mean = max(target_1, target_2)


# ============================================================
# APPROXIMATE STRENGTH CURVES
# ============================================================

CURVE_X = np.array([
    0.25, 0.30, 0.35, 0.40,
    0.45, 0.50, 0.55, 0.60, 0.65
])

CURVE_1 = np.array([
    60.0, 51.0, 43.0, 36.5,
    30.0, 25.0, 21.0, 17.5, 15.0
])

CURVE_2 = np.array([
    66.0, 57.0, 49.0, 42.0,
    36.0, 30.0, 26.0, 22.0, 19.0
])

CURVE_3 = np.array([
    74.0, 65.0, 57.0, 50.0,
    43.0, 37.5, 32.0, 27.0, 23.0
])


# ============================================================
# SELECT CURVE
# ============================================================

if cement_type == "OPC 33":

    selected_curve = CURVE_1
    curve_name = "Curve 1 — 33 MPa and below"

elif cement_type == "OPC 43":

    selected_curve = CURVE_2
    curve_name = "Curve 2 — 43 MPa to below 53 MPa"

elif cement_type == "OPC 53":

    selected_curve = CURVE_3
    curve_name = "Curve 3 — 53 MPa and above"

else:

    # Lecture example assumes OPC 43 curve for PPC trial
    selected_curve = CURVE_2
    curve_name = "OPC 43 curve used for PPC trial"


# ============================================================
# W/C FROM GRAPH
# ============================================================

# np.interp gives an approximate graph reading.

graph_wc = None

if target_mean >= selected_curve.min() and target_mean <= selected_curve.max():

    # Curve strength decreases as W/C increases.
    graph_wc = np.interp(
        target_mean,
        selected_curve[::-1],
        CURVE_X[::-1]
    )


# ============================================================
# EXPOSURE LIMITS
# ============================================================

exposure_wc = {
    "Mild": 0.55,
    "Moderate": 0.50,
    "Severe": 0.45,
    "Very Severe": 0.45,
    "Extreme": 0.40
}

exposure_min_cement = {
    "Mild": 300,
    "Moderate": 300,
    "Severe": 320,
    "Very Severe": 340,
    "Extreme": 360
}

max_wc = exposure_wc[exposure]
minimum_cement = exposure_min_cement[exposure]


# ============================================================
# ADOPT W/C
# ============================================================

if graph_wc is None:

    # If target is outside the displayed graph,
    # use the durability limit as a fallback.

    adopted_wc = max_wc

else:

    # More stringent requirement governs:
    # lower of strength-based and durability-based W/C

    adopted_wc = min(graph_wc, max_wc)


# ============================================================
# BASE WATER CONTENT
# ============================================================

# CE203 Lecture 13:
#
# 10 mm = 208 kg/m3
# 20 mm = 186 kg/m3
# 40 mm = 165 kg/m3
#
# at 50 mm slump

base_water_table = {
    10: 208,
    20: 186,
    40: 165
}

base_water = base_water_table[aggregate_size]


# ============================================================
# SLUMP CORRECTION
# ============================================================

if slump > 50:

    number_of_25mm_increments = (slump - 50) / 25

    slump_factor = 1 + 0.03 * number_of_25mm_increments

else:

    slump_factor = 1.0


water_after_slump = base_water * slump_factor


# ============================================================
# SUPERPLASTICIZER WATER REDUCTION
# ============================================================

water = water_after_slump * (1 - water_reduction / 100)


# ============================================================
# CEMENT FROM W/C
# ============================================================

cement = water / adopted_wc


# ============================================================
# MINIMUM CEMENT REQUIREMENT
# ============================================================

cement_final = max(
    cement,
    minimum_cement
)


# If cement is increased to satisfy durability,
# water is adjusted to maintain adopted W/C.

if cement_final > cement:

    cement = cement_final
    water = cement * adopted_wc


# ============================================================
# SUPERPLASTICIZER MASS
# ============================================================

sp_mass = cement * sp_dosage / 100


# ============================================================
# COARSE AGGREGATE FRACTION
# ============================================================

# Explicit lecture example:
# 20 mm + Zone II + W/C 0.50 = 0.62
#
# Other combinations below are reference values for the
# calculator structure. The lecture itself explicitly
# demonstrates the 20 mm + Zone II value.

CA_REFERENCE_TABLE = {

    10: {
        "I": 0.44,
        "II": 0.46,
        "III": 0.48,
        "IV": 0.50
    },

    20: {
        "I": 0.60,
        "II": 0.62,
        "III": 0.64,
        "IV": 0.66
    },

    40: {
        "I": 0.69,
        "II": 0.71,
        "III": 0.73,
        "IV": 0.75
    }
}

ca_fraction_reference = CA_REFERENCE_TABLE[
    aggregate_size
][zone]


# ============================================================
# CA CORRECTION
# ============================================================

reference_wc = 0.50

if adopted_wc < reference_wc:

    decrease = reference_wc - adopted_wc

    correction = (decrease / 0.05) * 0.01

    ca_fraction = ca_fraction_reference + correction

else:

    increase = adopted_wc - reference_wc

    correction = (increase / 0.05) * 0.01

    ca_fraction = ca_fraction_reference - correction


# Keep physically meaningful

ca_fraction = max(
    0.0,
    min(ca_fraction, 0.90)
)

fa_fraction = 1 - ca_fraction


# ============================================================
# ABSOLUTE VOLUME METHOD
# ============================================================

air_volume = 0.01 if aggregate_size == 20 else 0.01

cement_volume = cement / (
    sg_cement * 1000
)

water_volume = water / 1000

sp_volume = sp_mass / (
    sg_sp * 1000
)

aggregate_volume = (
    1
    - cement_volume
    - water_volume
    - sp_volume
    - air_volume
)


# ============================================================
# AGGREGATE MASSES — SSD BASIS
# ============================================================

ca_volume = aggregate_volume * ca_fraction

fa_volume = aggregate_volume * fa_fraction

ca_ssd = ca_volume * sg_ca * 1000

fa_ssd = fa_volume * sg_fa * 1000


# ============================================================
# MOISTURE CORRECTION
# ============================================================

# SSD mass = Dry mass × (1 + absorption)

ca_dry = ca_ssd / (
    1 + ca_absorption / 100
)

fa_dry = fa_ssd / (
    1 + fa_absorption / 100
)


# Surface moisture adds water to the mix.
# Therefore actual batch water is reduced.

water_contribution_ca = ca_dry * ca_moisture / 100
water_contribution_fa = fa_dry * fa_moisture / 100

batch_water = (
    water
    - water_contribution_ca
    - water_contribution_fa
)


# ============================================================
# TOTAL QUANTITIES FOR SELECTED VOLUME
# ============================================================

cement_total = cement * volume

water_total = batch_water * volume

fa_total = fa_dry * volume

ca_total = ca_dry * volume

sp_total = sp_mass * volume


# ============================================================
# MAIN RESULT
# ============================================================

st.header("📊 Final Mix Design")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cement",
        f"{cement:.1f} kg/m³"
    )

with col2:
    st.metric(
        "Water",
        f"{batch_water:.1f} kg/m³"
    )

with col3:
    st.metric(
        "Fine Aggregate",
        f"{fa_dry:.1f} kg/m³"
    )

with col4:
    st.metric(
        "Coarse Aggregate",
        f"{ca_dry:.1f} kg/m³"
    )


# ============================================================
# CEMENT : FA : CA
# ============================================================

mix_ratio_fa = fa_ssd / cement

mix_ratio_ca = ca_ssd / cement

st.markdown(
    f"""
    <div class="ratio-box">

    <div class="ratio-title">
    Cement : Fine Aggregate : Coarse Aggregate
    </div>

    <div class="ratio-value">
    1 : {mix_ratio_fa:.2f} : {mix_ratio_ca:.2f}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Mix ratio is based on the calculated SSD aggregate quantities."
)


# ============================================================
# GRAPHS
# ============================================================

st.header("📈 Learn the Mix-Design Relationships")

tab1, tab2, tab3 = st.tabs([
    "1️⃣ Strength vs W/C",
    "2️⃣ Water vs Slump",
    "3️⃣ CA Correction"
])


# ============================================================
# GRAPH 1 — STRENGTH VS W/C
# ============================================================

with tab1:

    st.subheader(
        "IS 10262:2019 — 28-day Strength vs Free Water-Cement Ratio"
    )

    st.markdown(
        """
        <div class="graph-note">

        <b>How to read this graph:</b>

        <br><br>

        1. Calculate the <b>target mean strength</b>.

        <br>

        2. Select the appropriate cement strength curve.

        <br>

        3. From the target strength, move horizontally to the selected curve.

        <br>

        4. From that point, move vertically downward.

        <br>

        5. The x-axis gives the approximate <b>water-cement ratio</b>.

        <br><br>

        <b>Green line/point = selected curve and target value.</b>

        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()

    # Curve 1

    fig.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=CURVE_1,
            mode="lines",
            name="Curve 1 — ≤33 MPa",
            line=dict(width=3)
        )
    )

    # Curve 2

    fig.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=CURVE_2,
            mode="lines",
            name="Curve 2 — 43 to <53 MPa",
            line=dict(width=3)
        )
    )

    # Curve 3

    fig.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=CURVE_3,
            mode="lines",
            name="Curve 3 — ≥53 MPa",
            line=dict(width=3)
        )
    )

    # Highlight selected curve in GREEN

    fig.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=selected_curve,
            mode="lines",
            name="Selected curve",
            line=dict(
                color="green",
                width=6
            )
        )
    )

    # Target point

    if graph_wc is not None:

        fig.add_trace(
            go.Scatter(
                x=[graph_wc],
                y=[target_mean],
                mode="markers",
                name="Target point",
                marker=dict(
                    color="green",
                    size=14
                )
            )
        )

        # Green horizontal guide

        fig.add_hline(
            y=target_mean,
            line_color="green",
            line_dash="dash",
            line_width=2
        )

        # Green vertical guide

        fig.add_vline(
            x=graph_wc,
            line_color="green",
            line_dash="dash",
            line_width=2
        )

    fig.update_layout(
        title="Strength vs Free W/C Ratio",
        xaxis_title="Free water-cement ratio",
        yaxis_title="28-day compressive strength (MPa)",
        height=550,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        f"""
        Target mean strength = {target_mean:.2f} MPa

        Selected curve = {curve_name}

        Approximate graph W/C = {
            f"{graph_wc:.3f}"
            if graph_wc is not None
            else "Outside displayed graph range"
        }

        Adopted W/C = {adopted_wc:.3f}
        """
    )

    st.info(
        "For PPC, your Lecture 13 example assumes the OPC 43 strength curve "
        "for the trial calculation."
    )


# ============================================================
# GRAPH 2 — WATER VS SLUMP
# ============================================================

with tab2:

    st.subheader(
        "Water Content vs Slump"
    )

    st.markdown(
        """
        <div class="graph-note">

        <b>Lecture relationship:</b>

        <br><br>

        The reference water contents at 50 mm slump are:

        <br>

        • 10 mm aggregate → 208 kg/m³

        <br>

        • 20 mm aggregate → 186 kg/m³

        <br>

        • 40 mm aggregate → 165 kg/m³

        <br><br>

        For every <b>25 mm increase above 50 mm slump</b>,
        water increases by approximately <b>3%</b>.

        </div>
        """,
        unsafe_allow_html=True
    )

    slump_values = np.arange(
        25,
        201,
        25
    )

    fig2 = go.Figure()

    for size in [10, 20, 40]:

        values = []

        for s in slump_values:

            base = base_water_table[size]

            if s > 50:

                increments = (s - 50) / 25

                value = base * (
                    1 + 0.03 * increments
                )

            else:

                value = base

            values.append(value)

        fig2.add_trace(
            go.Scatter(
                x=slump_values,
                y=values,
                mode="lines+markers",
                name=f"{size} mm aggregate"
            )
        )

    fig2.update_layout(
        title="Reference Water Content vs Slump",
        xaxis_title="Slump (mm)",
        yaxis_title="Water content (kg/m³)",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.success(
        f"""
        Your input:

        Aggregate size = {aggregate_size} mm

        Slump = {slump} mm

        Water before SP reduction = {water_after_slump:.2f} kg/m³

        Water after SP reduction = {water:.2f} kg/m³
        """
    )


# ============================================================
# GRAPH 3 — CA CORRECTION
# ============================================================

with tab3:

    st.subheader(
        "Coarse Aggregate Fraction Correction"
    )

    st.markdown(
        """
        <div class="graph-note">

        <b>IS 10262 adjustment rule used in your lectures:</b>

        <br><br>

        For every <b>0.05 decrease in W/C ratio</b>,
        increase the coarse aggregate volume fraction by <b>0.01</b>.

        <br><br>

        Example from your lecture:

        <br>

        Reference W/C = 0.50

        <br>

        Actual W/C = 0.36

        <br>

        Decrease = 0.14

        <br>

        Correction = 0.14 / 0.05 × 0.01 = 0.028

        </div>
        """,
        unsafe_allow_html=True
    )

    wc_values = np.arange(
        0.30,
        0.61,
        0.01
    )

    ca_values = []

    for wc in wc_values:

        if wc < 0.50:

            correction_value = (
                (0.50 - wc) / 0.05
            ) * 0.01

            ca_value = (
                ca_fraction_reference
                + correction_value
            )

        else:

            correction_value = (
                (wc - 0.50) / 0.05
            ) * 0.01

            ca_value = (
                ca_fraction_reference
                - correction_value
            )

        ca_values.append(ca_value)

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=wc_values,
            y=ca_values,
            mode="lines",
            name="CA fraction",
            line=dict(width=4)
        )
    )

    fig3.add_trace(
        go.Scatter(
            x=[adopted_wc],
            y=[ca_fraction],
            mode="markers",
            name="Your mix",
            marker=dict(
                color="green",
                size=14
            )
        )
    )

    fig3.add_vline(
        x=adopted_wc,
        line_color="green",
        line_dash="dash"
    )

    fig3.add_hline(
        y=ca_fraction,
        line_color="green",
        line_dash="dash"
    )

    fig3.update_layout(
        title="Coarse Aggregate Fraction vs W/C",
        xaxis_title="Water-cement ratio",
        yaxis_title="Coarse aggregate fraction",
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.success(
        f"""
        Reference CA fraction = {ca_fraction_reference:.3f}

        Adopted W/C = {adopted_wc:.3f}

        Correction = {ca_fraction - ca_fraction_reference:+.3f}

        Final CA fraction = {ca_fraction:.3f}

        Final FA fraction = {fa_fraction:.3f}
        """
    )


# ============================================================
# CALCULATION STEPS
# ============================================================

st.header("🧮 Detailed Calculation Steps")


# Step 1

with st.expander(
    "Step 1 — Target Mean Strength",
    expanded=True
):

    st.markdown(
        f"""
        <div class="step-box">

        Characteristic strength:

        <br>

        <b>fck = {grade} MPa</b>

        <br><br>

        First expression:

        <br>

        fck + 1.65s

        <br>

        = {grade} + 1.65 × {sd:.2f}

        <br>

        = <b>{target_1:.2f} MPa</b>

        <br><br>

        Second expression:

        <br>

        fck + X

        <br>

        = {grade} + {X:.2f}

        <br>

        = <b>{target_2:.2f} MPa</b>

        <br><br>

        Therefore:

        <br>

        <b>Target mean strength = {target_mean:.2f} MPa</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# Step 2

with st.expander(
    "Step 2 — Water-Cement Ratio"
):

    st.write(
        f"Strength-curve W/C = "
        f"{graph_wc:.3f}" if graph_wc is not None
        else "Strength-curve W/C is outside the displayed graph range."
    )

    st.write(
        f"Maximum W/C for {exposure} exposure = {max_wc:.2f}"
    )

    st.write(
        f"Adopted W/C = lower of strength and durability requirements = "
        f"{adopted_wc:.3f}"
    )


# Step 3

with st.expander(
    "Step 3 — Water Content"
):

    st.write(
        f"Reference water at 50 mm slump = "
        f"{base_water:.0f} kg/m³"
    )

    st.write(
        f"Slump = {slump} mm"
    )

    st.write(
        f"Water after slump correction = "
        f"{water_after_slump:.2f} kg/m³"
    )

    if use_sp:

        st.write(
            f"SP water reduction = {water_reduction:.1f}%"
        )

        st.write(
            f"Water after SP reduction = "
            f"{water:.2f} kg/m³"
        )

    else:

        st.write(
            f"No SP used. Water = "
            f"{water:.2f} kg/m³"
        )


# Step 4

with st.expander(
    "Step 4 — Cement Content"
):

    st.write(
        f"Cement = Water / W/C"
    )

    st.write(
        f"= {water:.2f} / {adopted_wc:.3f}"
    )

    st.write(
        f"= {water / adopted_wc:.2f} kg/m³"
    )

    st.write(
        f"Minimum cement required for {exposure} exposure = "
        f"{minimum_cement} kg/m³"
    )

    st.write(
        f"Adopted cement = {cement:.2f} kg/m³"
    )


# Step 5

with st.expander(
    "Step 5 — Coarse Aggregate Fraction"
):

    st.write(
        f"Reference CA fraction = "
        f"{ca_fraction_reference:.3f}"
    )

    st.write(
        f"Reference W/C = 0.50"
    )

    st.write(
        f"Actual W/C = {adopted_wc:.3f}"
    )

    if adopted_wc < 0.50:

        decrease = 0.50 - adopted_wc

        st.write(
            f"Decrease = 0.50 - {adopted_wc:.3f} "
            f"= {decrease:.3f}"
        )

        st.write(
            f"Correction = "
            f"{decrease:.3f}/0.05 × 0.01 "
            f"= {correction:.3f}"
        )

    st.write(
        f"Final CA fraction = "
        f"{ca_fraction:.3f}"
    )

    st.write(
        f"Final FA fraction = "
        f"1 - {ca_fraction:.3f} "
        f"= {fa_fraction:.3f}"
    )


# Step 6

with st.expander(
    "Step 6 — Absolute Volume Method"
):

    st.write(
        f"Cement volume = {cement_volume:.4f} m³"
    )

    st.write(
        f"Water volume = {water_volume:.4f} m³"
    )

    st.write(
        f"SP volume = {sp_volume:.4f} m³"
    )

    st.write(
        f"Entrapped air volume = {air_volume:.4f} m³"
    )

    st.write(
        f"Total aggregate volume = "
        f"{aggregate_volume:.4f} m³"
    )

    st.write(
        f"Coarse aggregate volume = "
        f"{ca_volume:.4f} m³"
    )

    st.write(
        f"Fine aggregate volume = "
        f"{fa_volume:.4f} m³"
    )


# Step 7

with st.expander(
    "Step 7 — Aggregate Moisture Correction"
):

    st.write(
        f"SSD CA = {ca_ssd:.2f} kg/m³"
    )

    st.write(
        f"Dry CA = {ca_dry:.2f} kg/m³"
    )

    st.write(
        f"SSD FA = {fa_ssd:.2f} kg/m³"
    )

    st.write(
        f"Dry FA = {fa_dry:.2f} kg/m³"
    )

    st.write(
        "SSD mass = Dry mass × (1 + water absorption)"
    )

    st.write(
        f"Final batch water = {batch_water:.2f} kg/m³"
    )


# ============================================================
# MATERIAL TABLE
# ============================================================

st.header("📋 Final Material Quantities")

material_data = {
    "Material": [
        "Cement",
        "Water",
        "Fine Aggregate",
        "Coarse Aggregate",
        "Superplasticizer"
    ],

    "Per m³": [
        f"{cement:.2f} kg",
        f"{batch_water:.2f} kg",
        f"{fa_dry:.2f} kg",
        f"{ca_dry:.2f} kg",
        f"{sp_mass:.2f} kg"
    ],

    f"For {volume:g} m³": [
        f"{cement_total:.2f} kg",
        f"{water_total:.2f} kg",
        f"{fa_total:.2f} kg",
        f"{ca_total:.2f} kg",
        f"{sp_total:.2f} kg"
    ]
}

st.table(material_data)


# ============================================================
# CHECKS
# ============================================================

st.header("✅ Design Checks")

check1 = cement >= minimum_cement

check2 = adopted_wc <= max_wc

check3 = (
    aggregate_volume > 0
    and fa_volume > 0
    and ca_volume > 0
)

check4 = abs(
    fa_fraction + ca_fraction - 1
) < 0.001


if check1:
    st.success(
        f"✓ Cement content satisfies the minimum requirement "
        f"({cement:.1f} ≥ {minimum_cement} kg/m³)."
    )
else:
    st.error(
        "✗ Cement content does not satisfy the minimum requirement."
    )


if check2:
    st.success(
        f"✓ Adopted W/C satisfies the maximum limit "
        f"({adopted_wc:.3f} ≤ {max_wc:.2f})."
    )
else:
    st.error(
        "✗ Adopted W/C exceeds the exposure limit."
    )


if check3:
    st.success(
        "✓ Aggregate volumes are positive."
    )
else:
    st.error(
        "✗ Aggregate volume calculation needs checking."
    )


if check4:
    st.success(
        "✓ FA fraction + CA fraction = 1.00"
    )
else:
    st.error(
        "✗ Aggregate fractions do not sum to 1."
    )


# ============================================================
# CE203 LEARNING SECTION
# ============================================================

st.header("📚 CE 203 Quick Learning")

with st.expander(
    "What should I remember for the exam?"
):

    st.markdown("""
### 1. Target mean strength

The mix is designed for a strength higher than the characteristic strength because actual concrete strength varies.

### 2. Water-cement ratio

Lower W/C generally gives higher strength, subject to workability and other requirements.

The adopted W/C must satisfy both:

- strength requirement
- durability requirement

The more stringent requirement governs.

### 3. Water content

For 50 mm slump:

| Aggregate | Water |
|---|---:|
| 10 mm | 208 kg/m³ |
| 20 mm | 186 kg/m³ |
| 40 mm | 165 kg/m³ |

For every 25 mm increase in slump above 50 mm:

**Water increases by 3%.**

### 4. Superplasticizer

A superplasticizer can reduce the water required for the same workability.

### 5. Coarse aggregate correction

For every **0.05 decrease in W/C**:

**CA fraction increases by 0.01.**

### 6. Absolute volume method

The basic idea is:

**Cement volume + water volume + aggregate volume + admixture volume + air volume = 1 m³**

### 7. SSD condition

Mix-design aggregate quantities are initially considered on an SSD basis.

Actual field moisture conditions require correction.

### 8. Cement : FA : CA

The final mix proportion is expressed as:

**1 : FA/Cement : CA/Cement**
""")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "CE 203 Civil Engineering Materials | Concrete Mix Design | "
    "Based on the supplied CE203 lecture material and IS 10262 concepts taught in the lectures."
)
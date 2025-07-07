import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Electricity Consumption Calculator",
    page_icon="⚡",
    layout="wide"
)

# Title and header
st.title("⚡ Electricity Consumption Calculator")
st.markdown("Calculate your daily electricity consumption based on your apartment size and appliance usage.")

# Sidebar for inputs
with st.sidebar:
    st.header("📊 Input Parameters")
    
    # BHK input
    bhk = st.number_input(
        "Enter your BHK:",
        min_value=1,
        max_value=10,
        value=2,
        help="Number of bedrooms in your apartment"
    )
    
    st.markdown("---")
    st.subheader("Daily Appliance Usage")
    st.markdown("Select which appliances you used each day:")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Weekly Consumption Tracker")
    
    # Create form for daily inputs
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_short = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    days_elec = {}
    
    # Create tabs for each day
    tabs = st.tabs(days)
    
    for i, (day, day_short, tab) in enumerate(zip(days, days_short, tabs)):
        with tab:
            st.markdown(f"### {day}")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                ac_used = st.checkbox(
                    "Air Conditioner",
                    key=f"ac_{i}",
                    help="3 kWh consumption"
                )
            
            with col_b:
                fridge_used = st.checkbox(
                    "Refrigerator",
                    key=f"fridge_{i}",
                    help="3 kWh consumption"
                )
            
            with col_c:
                washing_used = st.checkbox(
                    "Washing Machine",
                    key=f"washing_{i}",
                    help="3 kWh consumption"
                )
            
            # Calculate energy for this day
            base_energy = ((bhk + 1) * 0.4) + ((bhk + 1) * 0.8)
            additional_energy = 0
            
            if ac_used:
                additional_energy += 3
            if fridge_used:
                additional_energy += 3
            if washing_used:
                additional_energy += 3
            
            total_energy = base_energy + additional_energy
            days_elec[day_short] = total_energy
            
            # Display daily consumption
            st.metric(
                f"{day} Total Consumption",
                f"{total_energy:.2f} kWh",
                help=f"Base: {base_energy:.2f} kWh + Appliances: {additional_energy} kWh"
            )

with col2:
    st.subheader("📈 Summary")
    
    # Calculate totals
    total_consumption = sum(days_elec.values())
    avg_consumption = total_consumption / 7
    
    # Display key metrics
    st.metric("Total Weekly Consumption", f"{total_consumption:.2f} kWh")
    st.metric("Average Daily Consumption", f"{avg_consumption:.2f} kWh")
    
    # Base consumption info
    base_daily = ((bhk + 1) * 0.4) + ((bhk + 1) * 0.8)
    st.info(f"Base consumption for {bhk} BHK: {base_daily:.2f} kWh/day")

# Charts section
st.markdown("---")
st.subheader("📊 Consumption Analysis")

col1, col2 = st.columns(2)

with col1:
    # Daily consumption bar chart
    df = pd.DataFrame(list(days_elec.items()), columns=['Day', 'Consumption'])
    
    fig_bar = px.bar(
        df,
        x='Day',
        y='Consumption',
        title='Daily Electricity Consumption',
        color='Consumption',
        color_continuous_scale='viridis'
    )
    fig_bar.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Consumption (kWh)",
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Pie chart for weekly distribution
    fig_pie = px.pie(
        df,
        values='Consumption',
        names='Day',
        title='Weekly Consumption Distribution'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Detailed breakdown table
st.subheader("📋 Detailed Breakdown")

# Create detailed DataFrame
detailed_data = []
for i, (day, day_short) in enumerate(zip(days, days_short)):
    ac_used = st.session_state.get(f"ac_{i}", False)
    fridge_used = st.session_state.get(f"fridge_{i}", False)
    washing_used = st.session_state.get(f"washing_{i}", False)
    
    base_energy = ((bhk + 1) * 0.4) + ((bhk + 1) * 0.8)
    appliance_energy = (3 if ac_used else 0) + (3 if fridge_used else 0) + (3 if washing_used else 0)
    
    detailed_data.append({
        'Day': day,
        'Base Consumption (kWh)': f"{base_energy:.2f}",
        'AC': "✓" if ac_used else "✗",
        'Fridge': "✓" if fridge_used else "✗",
        'Washing Machine': "✓" if washing_used else "✗",
        'Appliance Consumption (kWh)': appliance_energy,
        'Total Consumption (kWh)': f"{base_energy + appliance_energy:.2f}"
    })

detailed_df = pd.DataFrame(detailed_data)
st.dataframe(detailed_df, use_container_width=True)

# Cost estimation
st.markdown("---")
st.subheader("💰 Cost Estimation")

col1, col2 = st.columns(2)

with col1:
    rate_per_unit = st.number_input(
        "Electricity Rate (₹/kWh):",
        min_value=0.0,
        value=5.0,
        step=0.1,
        help="Enter your local electricity rate per unit"
    )

with col2:
    weekly_cost = total_consumption * rate_per_unit
    monthly_cost = weekly_cost * 4.33  # Average weeks per month
    
    st.metric("Estimated Weekly Cost", f"₹{weekly_cost:.2f}")
    st.metric("Estimated Monthly Cost", f"₹{monthly_cost:.2f}")

# Tips section
st.markdown("---")
st.subheader("💡 Energy Saving Tips")

tips = [
    "Use AC at 24°C or higher to save energy",
    "Unplug appliances when not in use",
    "Use LED lights instead of incandescent bulbs",
    "Regular maintenance of AC and fridge improves efficiency",
    "Use washing machine with full load to optimize energy usage"
]

for tip in tips:
    st.write(f"• {tip}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Energy consumption values are approximate")
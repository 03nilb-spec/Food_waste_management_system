import streamlit as st
from queries import (
    total_food_donated_by_provider,
    total_quantity_of_food_available_from_all_providers,
    most_claimed_meal_by_type,
    most_commomn_available_food_by_type,
    average_food_claimed_per_receiver,
    food_claim_made_for_each_item,
    food_claim_percentage_by_status,
    highest_number_of_food_claims_by_provider,
    top_city_with_highest_food_listing,
    top_food_receiver,
    top_provider_type_by_food,
    get_providers_contact_info_by_city,
    count_providers_and_receivers_per_city,
    add_food_listing,
    update_claim_status,
    delete_food_listing 
)

# Streamlit app layout
st.title("Food Wastage Data Dashboard")

# --- Replace buttons with a dropdown ---
options = {
    "Top Providers by Food Donated": total_food_donated_by_provider,
    "Total Quantity of Food Available": total_quantity_of_food_available_from_all_providers,
    "Most Claimed Meal Type": most_claimed_meal_by_type,
    "Most Commonly Available Food Type": most_commomn_available_food_by_type,
    "Average Quantity of Food Claimed per Receiver": average_food_claimed_per_receiver,
    "Food Claims Made for Each Item": food_claim_made_for_each_item,
    "Provider with Highest Number of Food Claims": highest_number_of_food_claims_by_provider,
    "Food Claim Status in Percentage": food_claim_percentage_by_status,
    "Top 10 Cities by Food Listing": top_city_with_highest_food_listing,
    "Most Food Claimed by Receiver": top_food_receiver,
    "Top Food Contributor by Provider Type": top_provider_type_by_food,
    "Providers and Receivers per City": count_providers_and_receivers_per_city,
}

choice = st.selectbox("📊 Select a Query to Run:", list(options.keys()))

if st.button("Run Query"):
    try:
        df = options[choice]()   # call the selected function
        st.write(df)
    except Exception as e:
        st.error(f"Error running query: {e}")

# --- Contacts ---
st.header("Contacts")
contact_city = st.text_input("Providers in city (for contact list)").strip()
if st.button("Show Provider Contacts") and contact_city:
    df = get_providers_contact_info_by_city(contact_city)
    for _, r in df.iterrows():
        contact = str(r["contact"]).strip()
        link = None
        if "@" in contact:
            link = f"mailto:{contact}"
        elif contact.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            link = f"tel:{contact}"
        if link:
            st.markdown(f"**{r['name']}** — [{contact}]({link})")
        else:
            st.markdown(f"**{r['name']}** — {contact}")

st.header("Manage Data (CRUD)")

# CREATE
with st.expander("➕ Add Food Listing"):
    col1, col2 = st.columns(2)
    with col1:
        food_id = st.number_input("Food_ID", min_value=1, step=1)
        food_name = st.text_input("Food_Name")
        qty = st.number_input("Quantity", min_value=0, step=1)
        expiry = st.date_input("Expiry_Date")
        provider_id = st.number_input("Provider_ID", min_value=1, step=1)
    with col2:
        provider_type = st.text_input("Provider_Type")
        location = st.text_input("Location")
        food_type = st.text_input("Food_Type")
        meal_type = st.text_input("Meal_Type")
    if st.button("Add Listing"):
        try:
            add_food_listing(
                int(food_id), food_name, int(qty), expiry, int(provider_id),
                provider_type, location, food_type, meal_type
            )
            st.success("Listing added ✅")
        except Exception as e:
            st.error(f"Failed: {e}")

# UPDATE
with st.expander("✏️ Update Claim Status"):
    claim_id = st.number_input("Claim_ID", min_value=1, step=1)
    new_status = st.selectbox("New Status", ["pending", "completed", "canceled"])
    if st.button("Update Status"):
        try:
            update_claim_status(int(claim_id), new_status)
            st.success("Claim status updated ✅")
        except Exception as e:
            st.error(f"Failed: {e}")

# DELETE
with st.expander("🗑️ Delete Food Listing"):
    del_food_id = st.number_input("Food_ID to delete", min_value=1, step=1)
    if st.button("Delete Listing"):
        try:
            delete_food_listing(int(del_food_id))
            st.success("Listing deleted ✅")
        except Exception as e:
            st.error(f"Failed: {e}")
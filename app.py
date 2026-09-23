import streamlit as st
import pandas as pd
from pypdf import PdfReader
from database import insert_invoice, get_all_invoices, update_status, get_dashboard_stats, get_filtered_invoices
from ai_extractor import extract_invoice_data

st.set_page_config(page_title="Enterprise Invoice AI", layout="wide", page_icon="🤖")

# --- SIDEBAR: Role Selection & Upload ---
with st.sidebar:
    st.header("👤 User Role")
    role = st.selectbox("Select Role", ["Admin", "Viewer"])
    st.markdown("---")
    
    st.header("📄 Upload Invoice")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Extract & Save"):
            with st.spinner("AI is reading the invoice..."):
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                data = extract_invoice_data(text)
                
                if data:
                    insert_invoice(
                        data.get('vendor_name'), 
                        data.get('invoice_number'), 
                        data.get('invoice_date'), 
                        data.get('total_amount')
                    )
                    st.success(f"Saved! Vendor: {data.get('vendor_name')}")
                    st.rerun()
                else:
                    st.error("AI failed to parse the document.")

# --- MAIN DASHBOARD ---
st.title("🤖 Enterprise AI Invoice Extractor")
st.markdown("AI-powered document extraction and approval workflow system.")

# 1. KPI METRICS
stats = get_dashboard_stats()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Invoices", stats["total_count"])
col2.metric("Pending Amount", f"${stats['pending_amt']:,.2f}")
col3.metric("Approved Amount", f"${stats['approved_amt']:,.2f}")
col4.metric("Total Value", f"${stats['total_amt']:,.2f}")

st.markdown("---")

# 2. FILTER & CHART
col_search, col_chart = st.columns([1, 2])

with col_search:
    st.subheader("🔍 Filter Invoices")
    search_query = st.text_input("Search by Vendor Name")
    if search_query:
        invoices = get_filtered_invoices(search_query)
    else:
        invoices = get_all_invoices()

with col_chart:
    if invoices:
        st.subheader("📊 Top Vendors by Amount")
        df = pd.DataFrame(invoices, columns=["ID", "Vendor", "Invoice No", "Date", "Amount", "Status", "Created At"])
        vendor_df = df.groupby("Vendor")["Amount"].sum().reset_index()
        st.bar_chart(vendor_df.set_index("Vendor"), height=250)

# 3. DATA TABLE & APPROVALS
st.markdown("---")
st.subheader("📋 Invoice Dashboard")

if invoices:
    df = pd.DataFrame(invoices, columns=["ID", "Vendor", "Invoice No", "Date", "Amount", "Status", "Created At"])
    
    # CSV Export (Shows reporting skills)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Report as CSV",
        data=csv,
        file_name='invoice_report.csv',
        mime='text/csv',
    )
    
    st.dataframe(df, use_container_width=True)
    
    # 4. ROLE-BASED ACCESS CONTROL (RBAC)
    if role == "Admin":
        st.subheader("⚙️ Manage Approvals")
        col1, col2, col3 = st.columns(3)
        with col1:
            inv_id = st.number_input("Invoice ID", min_value=1, step=1)
        with col2:
            if st.button("✅ Approve"):
                update_status(inv_id, "Approved")
                st.success(f"Invoice {inv_id} Approved!")
                st.rerun()
        with col3:
            if st.button("❌ Reject"):
                update_status(inv_id, "Rejected")
                st.error(f"Invoice {inv_id} Rejected!")
                st.rerun()
    else:
        st.info("🔒 You are viewing as a Viewer. Only Admins can approve or reject invoices.")
else:
    st.info("No invoices uploaded yet. Upload one from the sidebar!")
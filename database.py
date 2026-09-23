import sqlite3

def init_db():
    conn = sqlite3.connect('invoices.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT,
            invoice_number TEXT,
            invoice_date TEXT,
            total_amount REAL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_invoice(vendor, inv_num, inv_date, amount):
    conn = sqlite3.connect('invoices.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO invoices (vendor_name, invoice_number, invoice_date, total_amount)
        VALUES (?, ?, ?, ?)
    ''', (vendor, inv_num, inv_date, amount))
    conn.commit()
    conn.close()

def get_all_invoices():
    conn = sqlite3.connect('invoices.db')
    c = conn.cursor()
    c.execute('SELECT * FROM invoices ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def update_status(inv_id, status):
    conn = sqlite3.connect('invoices.db')
    c = conn.cursor()
    c.execute('UPDATE invoices SET status = ? WHERE id = ?', (status, inv_id))
    conn.commit()
    conn.close()

# NEW FUNCTION 1: Get Dashboard Stats for KPIs
def get_dashboard_stats():
    conn = sqlite3.connect('invoices.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(total_amount) FROM invoices")
    total_count, total_amt = c.fetchone()
    
    c.execute("SELECT COUNT(*), SUM(total_amount) FROM invoices WHERE status='Pending'")
    pending_count, pending_amt = c.fetchone()
    
    c.execute("SELECT COUNT(*), SUM(total_amount) FROM invoices WHERE status='Approved'")
    approved_count, approved_amt = c.fetchone()
    
    conn.close()
    
    return {
        "total_count": total_count or 0,
        "total_amt": total_amt or 0.0,
        "pending_count": pending_count or 0,
        "pending_amt": pending_amt or 0.0,
        "approved_count": approved_count or 0,
        "approved_amt": approved_amt or 0.0
    }

# NEW FUNCTION 2: Filter by Vendor
def get_filtered_invoices(vendor_search):
    conn = sqlite3.connect('invoices.db')
    c = conn.cursor()
    query = "SELECT * FROM invoices WHERE vendor_name LIKE ? ORDER BY id DESC"
    c.execute(query, ('%' + vendor_search + '%',))
    rows = c.fetchall()
    conn.close()
    return rows

init_db()
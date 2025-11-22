def insert_ticket(ticket_id, priority, status, category, subject,
                   description, created_date, resolved_date,
                   assigned_to):
    """Insert a new IT ticket."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject,
         description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_id, priority, status, category, subject,
        description, created_date, resolved_date, assigned_to
    ))

    conn.commit()
    ticket_row_id = cursor.lastrowid
    conn.close()

    return ticket_row_id


def get_all_tickets():
    """Return all tickets as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df

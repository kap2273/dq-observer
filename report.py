
def build_report(table):
    small = table[["file","verdict","rule_failures","score"]]
    html_table = small.to_html(index=False)
    counts = table["verdict"].value_counts()
    page = f"""
    <style>
    body  {{ font-family: sans-serif; margin: 40px; }}
    table {{ border-collapse: collapse; }}
    th, td {{ border: 1px solid #ccc; padding: 6px 12px; }}
    th {{ background: #f0f0f0; }}
    </style>
    <h1>Data Quality Report</h1>
    <h2>Summary</h2>
    <p>{counts["Block"]} Blocked, {counts["Warn"]} Warned, {counts["Pass"]} Passed</p>
    {html_table}
    """

    with open("report.html","w") as f:
        f.write(page)
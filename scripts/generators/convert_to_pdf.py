#!/usr/bin/env python3
"""Convert README.md to PDF"""
import os
import sys

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Installing weasyprint...")
    os.system("pip install weasyprint -q")
    from weasyprint import HTML, CSS

try:
    import markdown2
except ImportError:
    print("Installing markdown2...")
    os.system("pip install markdown2 -q")
    import markdown2

# Read markdown file
with open('README.md', 'r') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'tables'])

# Create full HTML document with styling
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Salary Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #fff;
            padding: 40px;
            max-width: 1000px;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }}
        
        h2 {{
            color: #34495e;
            font-size: 1.8em;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        
        h3 {{
            color: #34495e;
            font-size: 1.3em;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        h4 {{
            color: #555;
            font-size: 1.1em;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        
        p {{
            margin-bottom: 12px;
            line-height: 1.8;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
            line-height: 1.7;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
            word-break: break-all;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
        }}
        
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            border-radius: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-left: 0;
            margin-bottom: 15px;
            color: #555;
            font-style: italic;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #3498db;
            margin: 30px 0;
        }}
        
        .meta {{
            color: #7f8c8d;
            font-size: 0.95em;
            margin-bottom: 5px;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        
        em {{
            color: #555;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            h2 {{
                font-size: 1.5em;
            }}
        }}
        
        .page-break {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Write to temporary HTML file
with open('/tmp/readme.html', 'w') as f:
    f.write(full_html)

# Convert HTML to PDF
print("Converting to PDF...")
HTML('/tmp/readme.html').write_pdf('README.pdf')
print("✓ Successfully created README.pdf")

# Clean up
os.remove('/tmp/readme.html')

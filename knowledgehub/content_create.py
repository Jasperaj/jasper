import os
import re

# Define the directory containing your HTML files
html_directory = '../knowledgehub'

# Define categories for each file pattern (adjust as needed)
# Map keywords in file names to categories
category_map = {
    r'taxation': 'Taxation',  # Matches 'tax' or 'taxation'
    r'account(ing)?': 'Accounting',  # Matches 'account' or 'accounting'
    r'finance': 'Finance',
    r'python': 'Technology',
    r'excel': 'Finance',
    r'registration': 'Business',
    r'business': 'Business',
    r'vat': 'Taxation',
    r'resources': 'Resources',
    # Add more keywords and categories as needed
}

# Helper function to determine category based on file name
def determine_category(filename):
    for keyword_pattern, category in category_map.items():
        if re.search(keyword_pattern, filename, re.IGNORECASE):
            return category
    return 'Uncategorized'  # Default category if no match is found

# List to hold topics information
topics = []

# Process each HTML file in the directory
for filename in os.listdir(html_directory):
    if filename.endswith('.html'):
        filepath = os.path.join(html_directory, filename)
        
        # Read the HTML file content
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Extract the title from the HTML file if it exists
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else filename.replace('.html', '').replace('-', ' ').title()
            
            # Extract description from a meta tag (if available) or use a default description
            description_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
            description = description_match.group(1) if description_match else "Description not available."
            
            # Extract the first image URL if it exists
            image_match = re.search(r'<img.*?src=["\'](.*?)["\']', content, re.IGNORECASE)
            image = image_match.group(1) if image_match else "default-image.png"  # Fallback image if not found
            
            # Determine the category based on file name or other logic
            category = determine_category(filename)
            
            # Append to topics list
            topics.append({
                "file": filename,
                "title": title,
                "description": description,
                "category": category,
                "image": image
            })

# Generate the JavaScript array syntax
js_array_content = 'const topics = [\n'
for topic in topics:
    js_array_content += f'  {{ "file": "{topic["file"]}", "title": "{topic["title"]}", "description": "{topic["description"]}", "category": "{topic["category"]}", "image": "{topic["image"]}" }},\n'
js_array_content = js_array_content.rstrip(',\n') + '\n];'

# Write to a JavaScript file or display it
output_file = 'topics_array.js'
with open(output_file, 'w', encoding='utf-8') as js_file:
    js_file.write(js_array_content)

print(f"JavaScript array generated and saved to {output_file}")
print(js_array_content)  # Optionally print the generated JavaScript array

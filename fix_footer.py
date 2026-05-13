import sys

with open('templates/includes/footer.html', 'r') as f:
    content = f.read()

# 1. Company Info
content = content.replace(
    'class="h-44 w-auto rounded-lg transition-all duration-300 group-hover:scale-105"',
    'class="h-32 md:h-44 w-auto rounded-lg transition-all duration-300 group-hover:scale-105"'
)

# 2. Newsletter Heading
content = content.replace(
    '<h3 class="text-2xl font-bold mb-3 text-white">Stay Connected</h3>',
    '<h3 class="text-xl md:text-2xl font-bold mb-3 text-white">Stay Connected</h3>'
)

# 3. Newsletter Alignment (Left on mobile, Center on desktop)
content = content.replace(
    '<div class="max-w-2xl mx-auto text-center">',
    '<div class="max-w-2xl mx-auto text-left md:text-center">'
)
content = content.replace(
    '<form class="flex flex-col sm:flex-row gap-3 justify-center max-w-md mx-auto">',
    '<form class="flex flex-col sm:flex-row gap-3 justify-start md:justify-center max-w-md md:mx-auto">'
)

# 4. Bottom Footer alignment
bottom_old = """      <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        <div class="text-sm text-gray-500">
          © {% now "Y" %} Development Decision Support (DDS). All rights reserved.
        </div>
        <div class="flex flex-wrap justify-center gap-6 text-sm">"""

bottom_new = """      <div class="flex flex-col md:flex-row justify-between items-center space-y-6 md:space-y-0">
        <div class="text-sm text-gray-500 text-center md:text-left">
          © {% now "Y" %} Development Decision Support (DDS). All rights reserved.
        </div>
        <div class="flex flex-col sm:flex-row flex-wrap justify-center sm:justify-end items-center gap-4 sm:gap-6 text-sm text-center sm:text-left">"""

content = content.replace(bottom_old, bottom_new)

# 5. Fix Quick Links / Services / Contact layout alignment on mobile if needed.
# By default, they are left-aligned because they have no text-center. This is good.

with open('templates/includes/footer.html', 'w') as f:
    f.write(content)


import sys

with open('templates/includes/header.html', 'r') as f:
    content = f.read()

# 1. Extract mobile-menu-overlay
start_idx = content.find('  <!-- Full-screen Mobile Overlay Menu -->')
end_idx = content.find('    <!-- Logo for Desktop: Hidden on mobile -->')

overlay_content = content[start_idx:end_idx]

# Remove overlay from its original place
content = content[:start_idx] + content[end_idx:]

# 2. Put desktop logo into navbar-start
# Find navbar-start closing div (which is just before the place where overlay was)
# The text right before `start_idx` is:
#       </button>
#     </div>
#   </div>
#
navbar_start_close = content.rfind('  </div>', 0, start_idx)

logo_start = content.find('    <!-- Logo for Desktop: Hidden on mobile -->')
logo_end = content.find('    </a>\n  </div>\n\n  <!-- =================================================== -->')
# Note: we want to include `</a>\n` but we want to remove the `  </div>` which closes the container.
logo_end = content.find('</a>', logo_start) + 4

desktop_logo = content[logo_start:logo_end]

# Remove desktop logo and the container closing div
# The container closing div is right after the logo
container_close_idx = content.find('  </div>\n\n  <!-- =================================================== -->', logo_end)

content = content[:logo_start] + content[container_close_idx + 9:] # skip the `  </div>\n\n`

# Insert desktop logo before the navbar-start closing div
content = content[:navbar_start_close] + '\n' + desktop_logo + '\n  </div>\n' + content[navbar_start_close + 9:] # skip `  </div>\n`

# 3. Add overlay right before <script>
script_idx = content.find('<script>')
content = content[:script_idx] + overlay_content + '\n' + content[script_idx:]

# 4. Remove the extra closing div at the end of the navbar
# Find the end of navbar-end
end_of_navbar = content.find('</div>\n\n  <!-- Full-screen Mobile Overlay Menu -->')
if end_of_navbar == -1:
    # Just find the end of the navbar container
    navbar_end_close = content.find('    </a>\n  </div>\n  </div>\n</div>\n\n<script>')
    if navbar_end_close != -1:
        # replace `  </div>\n  </div>\n</div>` with `  </div>\n</div>`
        content = content.replace('  </div>\n  </div>\n</div>', '  </div>\n</div>')

# 5. Add h-full to container
content = content.replace('flex items-center justify-between w-full gap-8"', 'flex items-center justify-between w-full h-full gap-8"')

with open('templates/includes/header.html', 'w') as f:
    f.write(content)

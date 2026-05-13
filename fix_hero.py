import sys

with open('templates/pages/home.html', 'r') as f:
    content = f.read()

# 1. Fix h-screen -> h-[100dvh]
content = content.replace(
    '<section class="relative w-full h-screen text-white overflow-hidden">',
    '<section class="relative w-full h-[100dvh] text-white overflow-hidden">'
)

# 2. Fix h1 text size for mobile
content = content.replace(
    'class="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight mb-6 text-white"',
    'class="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-bold leading-tight mb-4 md:mb-6 text-white"'
)

# 3. Fix p text size for mobile
content = content.replace(
    'class="text-xl md:text-2xl text-gray-200 mb-8 leading-relaxed max-w-3xl"',
    'class="text-base sm:text-lg md:text-2xl text-gray-200 mb-6 md:mb-8 leading-relaxed max-w-3xl"'
)
content = content.replace(
    'class="text-xl md:text-2xl text-white mb-8 leading-relaxed max-w-3xl"',
    'class="text-base sm:text-lg md:text-2xl text-white mb-6 md:mb-8 leading-relaxed max-w-3xl"'
)

# 4. Fix stats bar
stats_old = """  <div class="hero-stats-bar py-10 md:py-14">
    <div class="container mx-auto px-4 lg:px-8">
      <div class="flex flex-wrap md:flex-nowrap items-center justify-between gap-6 md:gap-4 lg:gap-12">
        <div class="flex items-center gap-3 whitespace-nowrap">
          <div class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-white">10+</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight w-20 md:w-24">Years of Operation</div>
        </div>
        <div class="hidden md:block w-px h-10 bg-white/10"></div>
        <div class="flex items-center gap-3 whitespace-nowrap">
          <div class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-white">30+</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight w-20 md:w-24">Projects Delivered</div>
        </div>
        <div class="hidden md:block w-px h-10 bg-white/10"></div>
        <div class="flex items-center gap-3 whitespace-nowrap">
          <div class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-white">15+</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight w-24 md:w-28">Institutional Clients</div>
        </div>
        <div class="hidden md:block w-px h-10 bg-white/10"></div>
        <div class="flex items-center gap-3 whitespace-nowrap">
          <div class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-white">16</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight w-20 md:w-24">Districts Covered</div>
        </div>
      </div>
    </div>
  </div>"""

stats_new = """  <div class="hero-stats-bar py-6 md:py-14">
    <div class="container mx-auto px-4 lg:px-8">
      <div class="grid grid-cols-2 md:flex md:flex-nowrap items-center justify-between gap-y-6 gap-x-4 md:gap-4 lg:gap-12">
        <div class="flex items-center gap-3">
          <div class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white">10+</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight">Years of Operation</div>
        </div>
        <div class="hidden md:block w-px h-10 bg-white/10"></div>
        <div class="flex items-center gap-3">
          <div class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white">30+</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight">Projects Delivered</div>
        </div>
        <div class="hidden md:block w-px h-10 bg-white/10"></div>
        <div class="flex items-center gap-3">
          <div class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white">15+</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight">Institutional Clients</div>
        </div>
        <div class="hidden md:block w-px h-10 bg-white/10"></div>
        <div class="flex items-center gap-3">
          <div class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white">16</div>
          <div class="text-[10px] md:text-[11px] text-gray-400 uppercase tracking-widest font-bold leading-tight">Districts Covered</div>
        </div>
      </div>
    </div>
  </div>"""

content = content.replace(stats_old, stats_new)

with open('templates/pages/home.html', 'w') as f:
    f.write(content)


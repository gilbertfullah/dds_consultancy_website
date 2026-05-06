import os

file_path = '/Users/darlington/Desktop/dds_website/templates/pages/about.html'

with open(file_path, 'r') as f:
    lines = f.readlines()

start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if '<!-- ======================= OUR APPROACH ======================= -->' in line:
        start_line = i
    if '</section>' in line and start_line != -1 and i > start_line:
        end_line = i
        break

if start_line != -1 and end_line != -1:
    new_section = """<!-- ======================= OUR APPROACH ======================= -->
<section class="py-24 md:py-32 bg-slate-900 relative overflow-hidden">
  <!-- Studio HUD Decorative Background -->
  <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(white 1px, transparent 1px); background-size: 32px 32px;"></div>
  <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-px bg-gradient-to-r from-transparent via-emerald-500/20 to-transparent"></div>
  
  <div class="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
    <!-- Section Header -->
    <div class="text-center max-w-3xl mx-auto mb-24" data-aos="fade-up">
      <div class="inline-flex items-center gap-3 mb-6">
        <span class="text-[10px] font-black uppercase tracking-[0.5em] text-emerald-500">How We Work</span>
      </div>
      <h2 class="text-4xl md:text-6xl font-extrabold text-white mb-8 leading-tight tracking-tight">
        The Strategic <span class="text-emerald-400">Pipeline</span>
      </h2>
      <p class="text-lg text-gray-400 leading-relaxed">
        We believe in collaborative, client-centred engagements combining rigorous research with pragmatic delivery.
      </p>
    </div>

    <!-- Process Pipeline -->
    <div class="relative max-w-6xl mx-auto mb-24">
      <!-- Connection Line -->
      <div class="absolute top-1/2 left-0 w-full h-px bg-white/5 -translate-y-1/2 hidden lg:block"></div>
      
      <div class="grid lg:grid-cols-4 gap-12 lg:gap-8">
        <!-- Step 01 -->
        <div class="group relative" data-aos="fade-up">
          <div class="relative z-10 bg-slate-900 border border-white/5 rounded-[2.5rem] p-10 hover:border-emerald-500/30 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2">
            <div class="flex items-center justify-between mb-8">
              <span class="text-4xl font-black text-white/5 group-hover:text-emerald-500/20 transition-colors">01</span>
              <div class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-emerald-500/30 transition-colors">
                <svg class="w-5 h-5 text-gray-400 group-hover:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              </div>
            </div>
            <h4 class="text-xl font-bold text-white mb-4">Understand</h4>
            <p class="text-gray-500 text-sm leading-relaxed">Deep dive into your goals, constraints, and the communities you serve.</p>
          </div>
        </div>

        <!-- Step 02 -->
        <div class="group relative" data-aos="fade-up" data-aos-delay="100">
          <div class="relative z-10 bg-slate-900 border border-white/5 rounded-[2.5rem] p-10 hover:border-blue-500/30 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2">
            <div class="flex items-center justify-between mb-8">
              <span class="text-4xl font-black text-white/5 group-hover:text-blue-500/20 transition-colors">02</span>
              <div class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-blue-500/30 transition-colors">
                <svg class="w-5 h-5 text-gray-400 group-hover:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              </div>
            </div>
            <h4 class="text-xl font-bold text-white mb-4">Analyse</h4>
            <p class="text-gray-500 text-sm leading-relaxed">Evidence-based research and rigorous data analysis to uncover insights.</p>
          </div>
        </div>

        <!-- Step 03 -->
        <div class="group relative" data-aos="fade-up" data-aos-delay="200">
          <div class="relative z-10 bg-slate-900 border border-white/5 rounded-[2.5rem] p-10 hover:border-teal-500/30 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2">
            <div class="flex items-center justify-between mb-8">
              <span class="text-4xl font-black text-white/5 group-hover:text-teal-500/20 transition-colors">03</span>
              <div class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-teal-500/30 transition-colors">
                <svg class="w-5 h-5 text-gray-400 group-hover:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              </div>
            </div>
            <h4 class="text-xl font-bold text-white mb-4">Design</h4>
            <p class="text-gray-500 text-sm leading-relaxed">Tailor-made strategies, frameworks, and actionable roadmaps.</p>
          </div>
        </div>

        <!-- Step 04 -->
        <div class="group relative" data-aos="fade-up" data-aos-delay="300">
          <div class="relative z-10 bg-slate-900 border border-white/5 rounded-[2.5rem] p-10 hover:border-emerald-500/30 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2">
            <div class="flex items-center justify-between mb-8">
              <span class="text-4xl font-black text-white/5 group-hover:text-emerald-500/20 transition-colors">04</span>
              <div class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-emerald-500/30 transition-colors">
                <svg class="w-5 h-5 text-gray-400 group-hover:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              </div>
            </div>
            <h4 class="text-xl font-bold text-white mb-4">Support</h4>
            <p class="text-gray-500 text-sm leading-relaxed">Implementation support, M&E, and capacity-building for lasting impact.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Operating Principles -->
    <div class="max-w-4xl mx-auto">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white/5 border border-white/10 rounded-2xl p-6 text-center group hover:bg-white/10 transition-colors">
          <span class="text-[10px] font-black uppercase tracking-widest text-emerald-500 block mb-2">Core Value</span>
          <p class="text-white font-bold text-xs uppercase tracking-wider">Client-Centred</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-2xl p-6 text-center group hover:bg-white/10 transition-colors">
          <span class="text-[10px] font-black uppercase tracking-widest text-blue-500 block mb-2">Core Value</span>
          <p class="text-white font-bold text-xs uppercase tracking-wider">Collaborative</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-2xl p-6 text-center group hover:bg-white/10 transition-colors">
          <span class="text-[10px] font-black uppercase tracking-widest text-teal-500 block mb-2">Core Value</span>
          <p class="text-white font-bold text-xs uppercase tracking-wider">Research-Driven</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-2xl p-6 text-center group hover:bg-white/10 transition-colors">
          <span class="text-[10px] font-black uppercase tracking-widest text-emerald-500 block mb-2">Core Value</span>
          <p class="text-white font-bold text-xs uppercase tracking-wider">Results-Focused</p>
        </div>
      </div>
    </div>
  </div>
</section>"""
    lines[start_line:end_line+1] = [new_section + '\\n']
    with open(file_path, 'w') as f:
        f.writelines(lines)
    print("Success")
else:
    print("Section markers not found")

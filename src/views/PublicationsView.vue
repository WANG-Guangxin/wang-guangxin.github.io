<script setup>
import { ref } from 'vue'

const publications = [
  {
    type: 'paper',
    title: 'A natural-based fusion strategy for underwater image enhancement',
    venue: 'Multimedia Tools and Applications',
    year: 2022,
    doi: '10.1007/s11042-022-12267-7',
    url: 'https://doi.org/10.1007/s11042-022-12267-7',
    authors: 'Xiaohong Yan, Guangxin Wang, Guangqi Jiang, Yafei Wang, Zetian Mi, Xianping Fu',
    bibtex: `@Article{Yan2022,
  author  = {Yan, Xiaohong and Wang, Guangxin and Jiang, Guangqi and Wang, Yafei and Mi, Zetian and Fu, Xianping},
  title   = {A natural-based fusion strategy for underwater image enhancement},
  journal = {Multimedia Tools and Applications},
  year    = {2022},
  month   = {Sep},
  day     = {01},
  volume  = {81},
  number  = {21},
  pages   = {30051-30068},
  issn    = {1573-7721},
  doi     = {10.1007/s11042-022-12267-7},
  url     = {https://doi.org/10.1007/s11042-022-12267-7}
}`,
  },
  {
    type: 'paper',
    title: 'A novel biologically-inspired method for underwater image enhancement',
    venue: 'Signal Processing: Image Communication',
    year: 2022,
    doi: '10.1016/j.image.2022.116670',
    url: 'https://doi.org/10.1016/j.image.2022.116670',
    authors: 'Xiaohong Yan, Guangxin Wang, Guangyuan Wang, Yafei Wang, Xianping Fu',
    bibtex: `@article{YAN2022116670,
  title   = {A novel biologically-inspired method for underwater image enhancement},
  journal = {Signal Processing: Image Communication},
  volume  = {104},
  pages   = {116670},
  year    = {2022},
  issn    = {0923-5965},
  doi     = {10.1016/j.image.2022.116670},
  url     = {https://www.sciencedirect.com/science/article/pii/S0923596522000248},
  author  = {Xiaohong Yan and Guangxin Wang and Guangyuan Wang and Yafei Wang and Xianping Fu}
}`,
  },
  {
    type: 'patent',
    title: 'Underwater Image Enhancement Method Based on Contrast Perception Loss',
    venue: 'Chinese Patent CN116402721A',
    year: 2023,
    url: 'https://kns.cnki.net/kcms2/article/abstract?v=eoCTaIZmBONhPM4L1JEn4QMh6JvGVb7InF89IykMmLzvZSBK86mVG-GuL-2eoF4yN3gCttr-UptZ7eV4JoWiIS83MjEaXwbtypAOisB_vI-pjxwpfSHVf-4uegffKNx3j9j_yibN9RA=&uniplatform=NZKPT&language=CHS',
    authors: '付先平, 曹楠, 汪广鑫, 闫小红, 王亚飞',
    bibtex: `@manual{CN116402721A,
  author  = {付先平 and 曹楠 and 汪广鑫 and 闫小红 and 王亚飞},
  title   = {基于对比感知损失的水下图像增强方法},
  edition = {CN116402721A},
  year    = {2023},
  pages   = {18},
  address = {116026 辽宁省大连市高新园区凌海路1号}
}`,
  },
]

const openBib = ref({})

function toggleBib(index) {
  openBib.value[index] = !openBib.value[index]
}

function copyBib(bibtex, index) {
  navigator.clipboard.writeText(bibtex)
  openBib.value[index] = true
  // 简单反馈
  const btn = document.querySelector(`[data-copy="${index}"]`)
  if (btn) {
    btn.textContent = 'Copied!'
    setTimeout(() => (btn.textContent = 'Copy'), 1500)
  }
}
</script>

<template>
  <div class="publications-view">
    <h1 class="page-title">Publications</h1>

    <section class="pub-section">
      <h2 class="section-title">Papers</h2>
      <div class="pub-list">
        <article
          v-for="(pub, i) in publications.filter(p => p.type === 'paper')"
          :key="pub.title"
          class="card pub-card"
        >
          <div class="pub-badge">Paper</div>
          <h3 class="pub-title">
            <a :href="pub.url" target="_blank" rel="noopener">{{ pub.title }}</a>
          </h3>
          <p class="pub-authors">{{ pub.authors }}</p>
          <p class="pub-venue">{{ pub.venue }} · {{ pub.year }}</p>
          <div class="pub-actions">
            <a class="btn btn-sm btn-primary" :href="pub.url" target="_blank" rel="noopener">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              DOI
            </a>
            <button class="btn btn-sm btn-outline" @click="toggleBib(i)" :data-copy="i">
              {{ openBib[i] ? 'Hide BibTeX' : 'BibTeX' }}
            </button>
          </div>
          <pre v-if="openBib[i]" class="bibtex"><code>{{ pub.bibtex }}</code></pre>
        </article>
      </div>
    </section>

    <section class="pub-section">
      <h2 class="section-title">Patents</h2>
      <div class="pub-list">
        <article
          v-for="(pub, i) in publications.filter(p => p.type === 'patent')"
          :key="pub.title"
          class="card pub-card"
        >
          <div class="pub-badge pub-badge-patent">Patent</div>
          <h3 class="pub-title">
            <a :href="pub.url" target="_blank" rel="noopener">{{ pub.title }}</a>
          </h3>
          <p class="pub-authors">{{ pub.authors }}</p>
          <p class="pub-venue">{{ pub.venue }} · {{ pub.year }}</p>
          <div class="pub-actions">
            <a class="btn btn-sm btn-primary" :href="pub.url" target="_blank" rel="noopener">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              Link
            </a>
            <button class="btn btn-sm btn-outline" @click="toggleBib(i + 100)">
              {{ openBib[i + 100] ? 'Hide BibTeX' : 'BibTeX' }}
            </button>
          </div>
          <pre v-if="openBib[i + 100]" class="bibtex"><code>{{ pub.bibtex }}</code></pre>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.publications-view {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--accent-soft);
}

.pub-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pub-card {
  position: relative;
  padding: 24px;
}

.pub-card:hover {
  box-shadow: var(--shadow-md);
}

.pub-badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 10px;
}

.pub-badge-patent {
  background: rgba(217, 119, 6, 0.12);
  color: var(--warning);
}

.pub-title {
  font-size: 1.1rem;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 8px;
}

.pub-title a {
  color: var(--text);
}

.pub-title a:hover {
  color: var(--accent);
}

.pub-authors {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.pub-venue {
  color: var(--text-muted);
  font-size: 0.85rem;
  font-style: italic;
  margin-bottom: 16px;
}

.pub-actions {
  display: flex;
  gap: 10px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  font-family: inherit;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.btn-primary {
  background: var(--accent);
  color: #fff;
}

.btn-primary:hover {
  background: var(--accent-hover);
  color: #fff;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-secondary);
}

.btn-outline:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.bibtex {
  margin-top: 16px;
  padding: 16px;
  background: var(--bg-hover);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  line-height: 1.5;
  overflow-x: auto;
  color: var(--text-secondary);
  white-space: pre-wrap;
  word-break: break-word;
}
</style>

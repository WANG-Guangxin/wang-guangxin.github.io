<script setup>
const highlights = [
  {
    icon: 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5',
    title: 'Embedded Systems',
    desc: 'Wireless module driver development for Android devices at Neusoft.',
  },
  {
    icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    title: 'Computer Vision',
    desc: 'Underwater image enhancement research with deep learning methods.',
  },
  {
    icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    title: 'Research',
    desc: 'Published papers on natural-based and biologically-inspired underwater image enhancement.',
  },
]
</script>

<template>
  <div class="home-view">
    <section class="card hero">
      <h1 class="hero-title">Hi, I'm Guangxin Wang 👋</h1>
      <p class="hero-subtitle">Embedded System Engineer &amp; Researcher</p>
      <p class="hero-desc">
        I'm an embedded system engineer specializing in mobile wireless module driver development,
        with a research background in underwater image enhancement and deep learning.
      </p>
      <div class="hero-actions">
        <a href="#/publications" class="btn btn-primary">View Publications</a>
        <a href="#/about" class="btn btn-outline">About Me</a>
      </div>
    </section>

    <section class="highlights">
      <div v-for="item in highlights" :key="item.title" class="card highlight-card">
        <div class="highlight-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path :d="item.icon" />
          </svg>
        </div>
        <h3 class="highlight-title">{{ item.title }}</h3>
        <p class="highlight-desc">{{ item.desc }}</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero {
  padding: 40px 32px;
  background: linear-gradient(135deg, var(--accent-soft), transparent 60%);
}

.hero-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 8px;
}

.hero-subtitle {
  color: var(--accent);
  font-weight: 600;
  font-size: 1.05rem;
  margin-bottom: 16px;
}

.hero-desc {
  color: var(--text-secondary);
  max-width: 560px;
  margin-bottom: 24px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.92rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-primary {
  background: var(--accent);
  color: #fff;
}

.btn-primary:hover {
  background: var(--accent-hover);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-outline {
  border: 1px solid var(--border);
  color: var(--text-secondary);
}

.btn-outline:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.highlights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.highlight-card {
  padding: 24px;
}

.highlight-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.highlight-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  background: var(--accent-soft);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}

.highlight-title {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 6px;
}

.highlight-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
}
</style>

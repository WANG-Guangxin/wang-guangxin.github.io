<script setup>
const education = [
  {
    school: 'Northeast Petroleum University',
    period: 'September 2015 ~ June 2019',
    degree: 'Electronic Information Science and Technology',
    majors: ['Data Structures', 'Computer Networks', 'Operating Systems', 'Digital Image Processing'],
  },
  {
    school: 'Dalian Maritime University',
    period: 'September 2020 ~ June 2023',
    degree: 'Computer Science and Technology',
    majors: ['Underwater image enhancement', 'Deep learning'],
  },
]

const work = [
  {
    company: 'Hikvision',
    period: 'June 2022 ~ September 2022',
    position: 'Video Surveillance Software Client Development Engineer',
    language: 'CPP, Qt',
    description: 'Responsible for video surveillance client customization project. The customization requirements involve modules such as monitoring point resource tree, key personnel identification event linkage, video playback calendar, real-time preview window, etc.',
  },
  {
    company: 'Neusoft',
    period: 'June 2023 ~ Now',
    position: 'Mobile Wireless Module Development Engineer',
    language: 'CPP, C',
    description: 'Responsible for Android cell phone wireless module driver development and maintenance.',
    current: true,
  },
]
</script>

<template>
  <div class="about-view">
    <h1 class="page-title">About Me</h1>

    <section class="about-section">
      <h2 class="section-title">Education</h2>
      <div class="timeline">
        <div v-for="item in education" :key="item.school" class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="card timeline-card">
            <div class="timeline-head">
              <div>
                <h3 class="timeline-title">{{ item.school }}</h3>
                <p class="timeline-period">{{ item.period }}</p>
              </div>
            </div>
            <p class="timeline-degree">{{ item.degree }}</p>
            <div class="tag-list">
              <span v-for="m in item.majors" :key="m" class="tag">{{ m }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="about-section">
      <h2 class="section-title">Work Experience</h2>
      <div class="timeline">
        <div v-for="item in work" :key="item.company" class="timeline-item">
          <div class="timeline-marker" :class="{ current: item.current }"></div>
          <div class="card timeline-card">
            <div class="timeline-head">
              <div>
                <h3 class="timeline-title">
                  {{ item.company }}
                  <span v-if="item.current" class="current-badge">Current</span>
                </h3>
                <p class="timeline-period">{{ item.period }}</p>
              </div>
            </div>
            <p class="timeline-position">{{ item.position }}</p>
            <p class="timeline-lang">Language: {{ item.language }}</p>
            <p class="timeline-desc">{{ item.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-view {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 20px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--accent-soft);
}

.timeline {
  position: relative;
  padding-left: 24px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 4px;
  bottom: 4px;
  width: 2px;
  background: var(--border);
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.timeline-marker {
  position: absolute;
  left: -24px;
  top: 20px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--accent);
  border: 3px solid var(--bg-card);
  box-shadow: 0 0 0 2px var(--accent);
}

.timeline-marker.current {
  background: var(--success);
  box-shadow: 0 0 0 2px var(--success);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 2px var(--success); }
  50% { box-shadow: 0 0 0 6px rgba(74, 222, 128, 0.2); }
}

.timeline-card {
  padding: 20px 24px;
}

.timeline-card:hover {
  box-shadow: var(--shadow-md);
}

.timeline-head {
  margin-bottom: 10px;
}

.timeline-title {
  font-size: 1.1rem;
  font-weight: 700;
}

.current-badge {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(74, 222, 128, 0.15);
  color: var(--success);
  vertical-align: middle;
  margin-left: 6px;
}

.timeline-period {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.timeline-degree,
.timeline-position {
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.timeline-lang {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.timeline-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-style: italic;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.tag {
  font-size: 0.78rem;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 500;
}
</style>

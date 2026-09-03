<script setup>
import { ref, onMounted } from 'vue'

const data = ref(null)
const loading = ref(true)
const error = ref(false)

function sslColor(days) {
  if (days === null || days === undefined) return 'muted'
  if (days <= 0) return 'danger'
  if (days <= 15) return 'warning'
  if (days >= 60) return 'success'
  return 'info'
}

function sslLabel(days) {
  if (days === null || days === undefined) return 'N/A'
  return `${days} days`
}

function uptimeColor(pct) {
  if (pct === null || pct === undefined) return 'muted'
  if (pct >= 90) return 'success'
  if (pct >= 70) return 'info'
  if (pct >= 50) return 'warning'
  return 'danger'
}

onMounted(async () => {
  try {
    const res = await fetch('./sites-data.json')
    if (!res.ok) throw new Error('not found')
    data.value = await res.json()
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="sites-view">
    <h1 class="page-title">My Sites</h1>

    <div v-if="loading" class="card loading-card">
      <div class="spinner"></div>
      <p>Checking site status...</p>
    </div>

    <div v-else-if="error" class="card error-card">
      <p>⚠️ Status data not available. Run <code>python3 uptime.py</code> to generate it.</p>
    </div>

    <template v-else>
      <div class="update-info">
        <span class="update-badge">Last updated</span>
        <span>{{ data.updated_at_cst }} (CST)</span>
      </div>

      <div class="sites-grid">
        <a
          v-for="site in data.sites"
          :key="site.url"
          :href="site.url"
          target="_blank"
          rel="noopener"
          class="card site-card"
        >
          <div class="site-head">
            <span class="status-dot" :class="site.up ? 'up' : 'down'"></span>
            <h3 class="site-name">{{ site.name }}</h3>
            <span class="status-text" :class="site.up ? 'up' : 'down'">
              {{ site.up ? 'Online' : 'Offline' }}
            </span>
          </div>

          <p class="site-url">{{ site.url.replace(/^https?:\/\//, '') }}</p>

          <div class="site-badges">
            <span v-for="b in site.badges" :key="b" class="site-badge">{{ b }}</span>
          </div>

          <div class="site-stats">
            <div class="stat">
              <span class="stat-label">Uptime 7d</span>
              <span class="stat-value" :class="uptimeColor(site.uptime_7d)">
                {{ site.uptime_7d !== null ? site.uptime_7d + '%' : 'N/A' }}
              </span>
            </div>
            <div class="stat">
              <span class="stat-label">Uptime 24h</span>
              <span class="stat-value" :class="uptimeColor(site.uptime_24h)">
                {{ site.uptime_24h !== null ? site.uptime_24h + '%' : 'N/A' }}
              </span>
            </div>
            <div class="stat">
              <span class="stat-label">SSL</span>
              <span class="stat-value" :class="sslColor(site.ssl_days)">
                {{ sslLabel(site.ssl_days) }}
              </span>
            </div>
          </div>
        </a>
      </div>
    </template>
  </div>
</template>

<style scoped>
.sites-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.update-info {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.update-badge {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent);
}

.sites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.site-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  color: var(--text);
  transition: all 0.2s ease;
}

.site-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: var(--accent);
}

.site-head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot.up {
  background: var(--success);
  box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.2);
}

.status-dot.down {
  background: var(--danger);
  box-shadow: 0 0 0 3px rgba(248, 113, 113, 0.2);
}

.site-name {
  font-size: 1.05rem;
  font-weight: 700;
  flex: 1;
}

.status-text {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 2px 10px;
  border-radius: 999px;
}

.status-text.up {
  color: var(--success);
  background: rgba(74, 222, 128, 0.12);
}

.status-text.down {
  color: var(--danger);
  background: rgba(248, 113, 113, 0.12);
}

.site-url {
  color: var(--text-muted);
  font-size: 0.82rem;
  font-family: var(--font-mono);
  word-break: break-all;
}

.site-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.site-badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--bg-hover);
  color: var(--text-secondary);
  border: 1px solid var(--border);
}

.site-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 4px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  font-size: 0.7rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.stat-value {
  font-size: 0.95rem;
  font-weight: 700;
}

.stat-value.success { color: var(--success); }
.stat-value.warning { color: var(--warning); }
.stat-value.danger { color: var(--danger); }
.stat-value.info { color: var(--accent); }
.stat-value.muted { color: var(--text-muted); }

.loading-card,
.error-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 32px;
  color: var(--text-secondary);
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

code {
  font-family: var(--font-mono);
  background: var(--bg-hover);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85em;
}
</style>

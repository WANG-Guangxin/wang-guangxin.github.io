<script setup>
import { ref, onMounted } from 'vue'
import SideCard from './components/SideCard.vue'
import HomeView from './views/HomeView.vue'
import PublicationsView from './views/PublicationsView.vue'
import AboutView from './views/AboutView.vue'
import SitesView from './views/SitesView.vue'

const currentView = ref('home')
const darkMode = ref(false)

// 简单的 hash 路由
const routes = {
  '#/': 'home',
  '#/publications': 'publications',
  '#/about': 'about',
  '#/sites': 'sites',
}

function parseHash() {
  const hash = window.location.hash || '#/'
  currentView.value = routes[hash] || 'home'
}

function navigate(view) {
  currentView.value = view
  window.location.hash = view === 'home' ? '/' : `/${view}`
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function toggleDark() {
  darkMode.value = !darkMode.value
  document.documentElement.classList.toggle('dark', darkMode.value)
  localStorage.setItem('theme', darkMode.value ? 'dark' : 'light')
}

onMounted(() => {
  parseHash()
  window.addEventListener('hashchange', parseHash)
  // 恢复主题偏好
  const saved = localStorage.getItem('theme')
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    darkMode.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>

<template>
  <div class="app-shell">
    <header class="site-header">
      <nav class="nav-container">
        <a class="site-logo" href="#/" @click="navigate('home')">Guangxin Wang</a>
        <button class="theme-toggle" @click="toggleDark" :aria-label="darkMode ? 'Switch to light mode' : 'Switch to dark mode'">
          <svg v-if="!darkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
        </button>
        <ul class="nav-menu">
          <li><a :class="{ active: currentView === 'home' }" href="#/" @click="navigate('home')">Home</a></li>
          <li><a :class="{ active: currentView === 'publications' }" href="#/publications" @click="navigate('publications')">Publications</a></li>
          <li><a :class="{ active: currentView === 'about' }" href="#/about" @click="navigate('about')">About</a></li>
          <li><a :class="{ active: currentView === 'sites' }" href="#/sites" @click="navigate('sites')">Sites</a></li>
        </ul>
      </nav>
    </header>

    <main class="main-container">
      <SideCard />
      <div class="content-area">
        <HomeView v-if="currentView === 'home'" />
        <PublicationsView v-else-if="currentView === 'publications'" />
        <AboutView v-else-if="currentView === 'about'" />
        <SitesView v-else />
      </div>
    </main>

    <footer class="site-footer">
      <p>©2020 - {{ new Date().getFullYear() }} by Guangxin Wang</p>
      <p class="footer-powered">Built with <a href="https://vuejs.org" target="_blank" rel="noopener">Vue 3</a> &amp; <a href="https://vitejs.dev" target="_blank" rel="noopener">Vite</a></p>
    </footer>
  </div>
</template>

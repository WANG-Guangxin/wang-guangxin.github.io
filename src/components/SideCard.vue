<script setup>
import { ref } from 'vue'

const socialLinks = [
  { icon: 'home', url: 'https://wgxls.site', label: 'Website' },
  { icon: 'github', url: 'https://github.com/WANG-Guangxin', label: 'GitHub' },
  { icon: 'qq', url: 'tencent://AddContact/?fromId=50&fromSubId=1&subcmd=all&uin=2401881997', label: 'QQ' },
  { icon: 'mail', url: 'mailto:wgxls@foxmail.com', label: 'Email' },
]

const icons = {
  home: 'M3 12l9-9 9 9M5 10v10a1 1 0 001 1h4v-6h4v6h4a1 1 0 001-1V10',
  github: 'M12 2C6.48 2 2 6.58 2 12.25c0 4.53 2.87 8.37 6.84 9.73.5.09.68-.22.68-.49 0-.24-.01-.87-.01-1.7-2.78.62-3.37-1.37-3.37-1.37-.45-1.18-1.11-1.5-1.11-1.5-.91-.63.07-.62.07-.62 1 .07 1.53 1.06 1.53 1.06.89 1.56 2.34 1.11 2.91.85.09-.66.35-1.11.63-1.37-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.7 0 0 .84-.28 2.75 1.05a9.36 9.36 0 015 0c1.91-1.33 2.75-1.05 2.75-1.05.55 1.4.2 2.44.1 2.7.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9 0 1.37-.01 2.47-.01 2.81 0 .27.18.59.69.49A10.25 10.25 0 0022 12.25C22 6.58 17.52 2 12 2z',
  qq: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z',
  mail: 'M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z',
}
</script>

<template>
  <aside class="side-card">
    <div class="card profile-card">
      <div class="avatar-wrap">
        <img class="avatar" src="/img/avatar_rmbg.png" alt="Guangxin Wang avatar" />
      </div>
      <h3 class="profile-name">Guangxin Wang</h3>
      <p class="profile-bio">Embedded System Engineer</p>
      <div class="social-links">
        <a
          v-for="link in socialLinks"
          :key="link.label"
          :href="link.url"
          :title="link.label"
          target="_blank"
          rel="noopener"
          class="social-link"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path :d="icons[link.icon]" />
          </svg>
        </a>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.side-card {
  position: sticky;
  top: 92px;
  align-self: start;
}

.profile-card {
  text-align: center;
  padding: 32px 24px;
}

.avatar-wrap {
  width: 120px;
  height: 120px;
  margin: 0 auto 16px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--accent-soft);
  box-shadow: var(--shadow-md);
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.profile-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.profile-bio {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 4px;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.social-link:hover {
  color: var(--accent);
  border-color: var(--accent);
  background: var(--accent-soft);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .side-card {
    position: static;
  }
}
</style>

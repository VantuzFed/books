<template>
  <div class="app-root" :data-theme="theme" :data-stalker-bg="stalkerBg">
<div class="container">
    <!-- Шапка -->
    <header class="header">
      <div class="brand">
        <div class="logo" aria-hidden="true">
          <!-- Иконка радиации в стиле Сталкера, иначе книга -->
          <svg v-if="theme === 'stalker'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M12 9V3M14.6 13.5l5.2 3M9.4 13.5l-5.2 3"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            <path d="M8 7h8"/><path d="M8 11h8"/>
          </svg>
        </div>
        <div>
          <h1>{{ brandTitle }}</h1>
          <p>{{ brandSubtitle }}</p>
        </div>
      </div>

      <div class="header-actions">
        <!-- Переключатель тем: Светлая / Тёмная / Сталкер -->
        <div class="theme-switch" role="group" aria-label="Тема оформления">
          <button
            class="theme-btn"
            :class="{ active: theme === 'light' }"
            @click="setTheme('light')"
            title="Светлая тема"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
            <span>Светлая</span>
          </button>
          <button
            class="theme-btn"
            :class="{ active: theme === 'dark' }"
            @click="setTheme('dark')"
            title="Тёмная тема"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            <span>Тёмная</span>
          </button>
          <button
            class="theme-btn"
            :class="{ active: theme === 'stalker' }"
            @click="setTheme('stalker')"
            title="S.T.A.L.K.E.R. Главное меню & КПК"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 9V3M14.6 13.5l5.2 3M9.4 13.5l-5.2 3"/></svg>
            <span>S.T.A.L.K.E.R.</span>
          </button>
        </div>

        <!-- Переключатель обоев меню S.T.A.L.K.E.R. -->
        <div v-if="theme === 'stalker'" class="stalker-bg-switch" role="group" aria-label="Фон главного меню">
          <span class="stalker-bg-label">Фон:</span>
          <button
            class="stalker-bg-btn"
            :class="{ active: stalkerBg === 'menu' }"
            @click="setStalkerBg('menu')"
            title="Оригинальное главное меню: Штаб с плакатом и снайперской винтовкой"
          >Штаб</button>
          <button
            class="stalker-bg-btn"
            :class="{ active: stalkerBg === 'tractor' }"
            @click="setStalkerBg('tractor')"
            title="Заброшенный трактор на Свалке"
          >Свалка</button>
          <button
            class="stalker-bg-btn"
            :class="{ active: stalkerBg === 'barrel' }"
            @click="setStalkerBg('barrel')"
            title="Разрушенная стена с костром и бочкой"
          >Костёр</button>
        </div>

        <!-- Экспорт / Импорт / Демо -->
        <label class="btn btn-ghost" for="importFile" title="Загрузить список из JSON или CSV">
          ⤓ Импорт
        </label>
        <input id="importFile" class="file-input" type="file" accept=".json,.csv" @change="handleFileImport"/>

        <button class="btn" @click="exportJson" title="Выгрузить в формате JSON">⬇ JSON</button>
        <button class="btn" @click="exportCsv" title="Выгрузить в формате CSV">⬇ CSV</button>
        <button class="btn btn-primary" @click="loadDemo" title="Добавить демонстрационные книги">+ Демо-книги</button>
      </div>
    </header>

    <!-- Панель статистики -->
    <div class="stats-bar">
      <span class="stats-main">{{ theme === 'stalker' ? '[АРХИВ КПК]' : 'Всего книг' }}: <b>{{ stats.total }}</b></span>
      <span v-show="statsExpanded" class="stats-details">
        <span>· Прочитано: <b style="color:var(--green)">{{ stats.read }}</b></span>
        <span>· Читаю: <b style="color:var(--blue)">{{ stats.reading }}</b></span>
        <span>· В планах: <b style="color:var(--orange)">{{ stats.planned }}</b></span>
        <span>· Отложено: <b style="color:var(--violet)">{{ stats.dropped }}</b></span>
      </span>
      <button class="stats-toggle" @click="statsExpanded = !statsExpanded">
        {{ statsExpanded ? 'Скрыть детали' : 'Подробная статистика' }}
      </button>
    </div>

    <!-- Тулбар -->
    <div class="toolbar">
      <div class="toolbar-left">
        <!-- Поиск -->
        <div class="search">
          <span class="search-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          </span>
          <input
            v-model="query"
            :placeholder="theme === 'stalker' ? '[ПОИСК ПО БАЗЕ ДАННЫХ КПК...]' : 'Поиск по автору, названию, героям...'"
          />
          <button v-if="query" class="search-clear" @click="query = ''" title="Очистить поиск">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>

        <!-- Сортировка -->
        <select v-model="sort" class="sort-select">
          <option value="newest">Сначала новые</option>
          <option value="author">По автору (А→Я)</option>
          <option value="title">По названию (А→Я)</option>
          <option value="status">По статусу</option>
        </select>

        <!-- Переключатель Сетка / Таблица -->
        <div class="view-switch" role="group" aria-label="Режим отображения">
          <button
            :class="{ active: viewMode === 'grid' }"
            @click="setViewMode('grid')"
            title="Сетка карточек"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          </button>
          <button
            :class="{ active: viewMode === 'table' }"
            @click="setViewMode('table')"
            title="Табличный вид"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
          </button>
        </div>
      </div>

      <div class="toolbar-right">
        <span>{{ filteredBooks.length }} {{ plural(filteredBooks.length) }}</span>
      </div>
    </div>

    <!-- Фильтры статусов -->
    <div class="filters">
      <button
        class="filter-btn"
        :class="{ active: filter === 'all' }"
        @click="filter = 'all'"
      >
        Все <span class="filter-count">{{ counts.all }}</span>
      </button>
      <button
        class="filter-btn"
        :class="{ active: filter === 'planned' }"
        @click="filter = 'planned'"
      >
        <span class="dot dot-planned"></span> {{ theme === 'stalker' ? '[ЦЕЛЬ: ВЗЯТО]' : 'В планах' }}
        <span class="filter-count">{{ counts.planned }}</span>
      </button>
      <button
        class="filter-btn"
        :class="{ active: filter === 'reading' }"
        @click="filter = 'reading'"
      >
        <span class="dot dot-reading"></span> {{ theme === 'stalker' ? '[В ПРОЦЕССЕ]' : 'Читаю' }}
        <span class="filter-count">{{ counts.reading }}</span>
      </button>
      <button
        class="filter-btn"
        :class="{ active: filter === 'read' }"
        @click="filter = 'read'"
      >
        <span class="dot dot-read"></span> {{ theme === 'stalker' ? '[ВЫПОЛНЕНО]' : 'Прочитано' }}
        <span class="filter-count">{{ counts.read }}</span>
      </button>
      <button
        class="filter-btn"
        :class="{ active: filter === 'dropped' }"
        @click="filter = 'dropped'"
      >
        <span class="dot dot-dropped"></span> {{ theme === 'stalker' ? '[ОТМЕНЕНО]' : 'Отложено' }}
        <span class="filter-count">{{ counts.dropped }}</span>
      </button>

      <div style="margin-left:auto;display:flex;gap:6px">
        <button class="btn btn-sm" @click="copyJson" title="Скопировать JSON в буфер">Копировать JSON</button>
        <button class="btn btn-sm" @click="clearAll" title="Удалить все книги">Очистить список</button>
      </div>
    </div>

    <!-- Основной контент: СЕТКА -->
    <div v-if="viewMode === 'grid' && filteredBooks.length > 0" class="grid">
      <div v-for="b in filteredBooks" :key="b.id" class="book-card">
        <!-- Обложка -->
        <a v-if="b.link" :href="b.link" target="_blank" rel="noopener" class="cover" :title="'Открыть ссылку: ' + b.title">
          <img v-if="b.cover" :src="b.cover" :alt="b.title" loading="lazy" @error="b.cover = ''"/>
          <div v-else class="cover-placeholder">
            <svg class="ph-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            <div class="ph-author">{{ b.author }}</div>
            <div class="ph-title">{{ b.title }}</div>
          </div>
        </a>
        <div v-else class="cover">
          <img v-if="b.cover" :src="b.cover" :alt="b.title" loading="lazy" @error="b.cover = ''"/>
          <div v-else class="cover-placeholder">
            <svg class="ph-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            <div class="ph-author">{{ b.author }}</div>
            <div class="ph-title">{{ b.title }}</div>
          </div>
        </div>

        <!-- Контент карточки -->
        <div class="card-body">
          <div class="card-title" :title="b.title">{{ b.title }}</div>
          <div class="card-author" :title="b.author">{{ b.author }}</div>

          <!-- Главные герои -->
          <div v-if="b.characters" class="card-characters" :title="'Главные герои: ' + b.characters">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>{{ b.characters }}</span>
          </div>

          <!-- Описание -->
          <div v-if="b.description" class="card-desc" :title="b.description">
            {{ b.description }}
          </div>

          <!-- Статус -->
          <div class="card-meta">
            <span class="badge" :class="'badge-' + b.status">
              <svg v-if="b.status === 'read'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>
              <svg v-else-if="b.status === 'reading'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><path d="M8 7h6"/><path d="M8 11h6"/></svg>
              <svg v-else-if="b.status === 'planned'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 14.5 14.5"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              {{ statusLabels[b.status] || b.status }}
            </span>
          </div>

          <!-- Действия -->
          <div class="card-actions">
            <button class="icon-btn" @click="openEditModal(b)" title="Редактировать" aria-label="Редактировать">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>
            <button class="icon-btn" @click="deleteBook(b.id)" title="Удалить" aria-label="Удалить">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/></svg>
            </button>

            <!-- Быстрая смена статуса -->
            <div class="status-select-wrap" style="margin-left:auto">
              <button
                class="icon-btn"
                @click="toggleStatusMenu(b.id)"
                :title="'Сменить статус: ' + statusLabels[b.status]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
              </button>
              <div v-if="activeStatusMenu === b.id" class="status-menu">
                <button
                  class="status-option"
                  :class="{ 'is-active': b.status === 'planned' }"
                  @click="updateStatus(b.id, 'planned')"
                  title="В планах"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 14.5 14.5"/></svg>
                </button>
                <button
                  class="status-option"
                  :class="{ 'is-active': b.status === 'reading' }"
                  @click="updateStatus(b.id, 'reading')"
                  title="Читаю"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><path d="M8 7h6"/><path d="M8 11h6"/></svg>
                </button>
                <button
                  class="status-option"
                  :class="{ 'is-active': b.status === 'read' }"
                  @click="updateStatus(b.id, 'read')"
                  title="Прочитано"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>
                </button>
                <button
                  class="status-option"
                  :class="{ 'is-active': b.status === 'dropped' }"
                  @click="updateStatus(b.id, 'dropped')"
                  title="Отложено"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент: ТАБЛИЦА -->
    <div v-else-if="viewMode === 'table' && filteredBooks.length > 0" class="table-wrap">
      <table>
        <thead>
          <tr>
            <th style="width:20%">Автор (ФИО)</th>
            <th style="width:24%">Название</th>
            <th style="width:30%">Герои / Описание / Ссылка</th>
            <th style="width:14%">Статус</th>
            <th style="width:12%">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in filteredBooks" :key="b.id">
            <td><div class="table-author">{{ b.author }}</div></td>
            <td><div class="table-title">{{ b.title }}</div></td>
            <td>
              <div style="display:flex;flex-direction:column;gap:5px">
                <div v-if="b.characters" class="table-characters" :title="'Главные герои: ' + b.characters">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  <span><b>Герои:</b> {{ b.characters }}</span>
                </div>
                <div v-if="b.description" class="table-desc" :title="b.description">
                  {{ b.description }}
                </div>
                <div v-if="b.link">
                  <a :href="b.link" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:4px;font-size:12px">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" style="width:12px;height:12px"><path d="M10 13a5 5 0 0 1 0-7l1-1a5 5 0 0 1 7 7l-1 1"/><path d="M14 11a5 5 0 0 1 0 7l-1 1a5 5 0 0 1-7-7l1-1"/></svg>
                    {{ host(b.link) }}
                  </a>
                </div>
              </div>
            </td>
            <td>
              <span class="badge" :class="'badge-' + b.status">
                {{ statusLabels[b.status] || b.status }}
              </span>
            </td>
            <td>
              <div style="display:flex;gap:5px;align-items:center">
                <button class="icon-btn" @click="openEditModal(b)" title="Редактировать">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                </button>
                <button class="icon-btn" @click="deleteBook(b.id)" title="Удалить">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/></svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Пустое состояние -->
    <div v-if="filteredBooks.length === 0" class="empty">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
      <div style="font-weight:600;font-size:15px;margin-bottom:4px">
        {{ query ? 'Ничего не найдено по вашему запросу' : 'Список книг пуст' }}
      </div>
      <div style="font-size:13px;margin-bottom:14px">
        {{ query ? 'Попробуйте изменить поисковую фразу или сбросить фильтры' : 'Добавьте первую книгу вручную или загрузите демонстрационный список' }}
      </div>
      <div style="display:flex;gap:8px;justify-content:center">
        <button v-if="query" class="btn btn-sm" @click="query = ''">Сбросить поиск</button>
        <button v-else class="btn btn-primary btn-sm" @click="loadDemo">+ Загрузить демо-книги</button>
      </div>
    </div>
  </div>

  <!-- Плавающая кнопка добавления -->
  <button class="fab" @click="openAddModal" title="Добавить книгу" aria-label="Добавить книгу">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
  </button>

  <!-- Единое модальное окно: Добавление / Редактирование -->
  <div v-if="modalOpen" class="modal-backdrop" @click.self="closeModal">
    <div class="modal">
      <div class="modal-head">
        <h3>{{ modalMode === 'add' ? 'Добавить книгу' : 'Редактировать книгу' }}</h3>
        <button class="icon-btn" @click="closeModal" aria-label="Закрыть">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <form class="form" @submit.prevent="saveBook">
        <label>
          ФИО автора
          <input v-model.trim="form.author" placeholder="Напр. Лев Толстой" required ref="authorInput"/>
        </label>

        <label>
          Название книги
          <input v-model.trim="form.title" placeholder="Напр. Война и мир" required/>
        </label>

        <label>
          Главные герои
          <input v-model.trim="form.characters" placeholder="Напр. Пьер Безухов, Андрей Болконский, Наташа Ростова"/>
          <span class="hint">необязательно · через запятую</span>
        </label>

        <label>
          Описание книги
          <textarea v-model.trim="form.description" rows="3" placeholder="Краткое описание, сюжет или заметки о книге..."></textarea>
        </label>

        <label>
          Ссылка на книгу
          <input v-model.trim="form.link" type="url" placeholder="https://..."/>
          <span class="hint">необязательно · если есть — кликабельная</span>
        </label>

        <label>
          Обложка (URL)
          <div style="display:flex;gap:6px;align-items:center">
            <input v-model.trim="form.cover" type="url" placeholder="https://.../cover.jpg" style="flex:1"/>
            <button
              type="button"
              class="btn btn-sm"
              @click="findCover"
              :disabled="coverSearching"
              title="Найти обложку в Open Library / Google Books"
            >
              <svg v-if="coverSearching" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;animation:spin 1s linear infinite"><circle cx="12" cy="12" r="10" stroke-opacity=".25"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
              {{ coverSearching ? 'Поиск…' : 'Найти' }}
            </button>
          </div>
          <span class="hint">необязательно · автопоиск по автору и названию</span>
        </label>

        <!-- Превью найденной обложки -->
        <div v-if="form.cover" style="display:flex;gap:10px;align-items:center;padding:8px;background:var(--badge-bg);border:1px solid var(--border);border-radius:var(--radius-sm)">
          <img :src="form.cover" alt="" style="width:36px;height:48px;object-fit:cover;border-radius:3px"/>
          <span style="font-size:12px;color:var(--text-muted);flex:1">Обложка установлена</span>
          <button type="button" class="btn btn-sm" style="padding:4px 8px" @click="form.cover = ''">✕ Убрать</button>
        </div>

        <label>
          Статус
          <select v-model="form.status">
            <option value="planned">В планах</option>
            <option value="reading">Читаю</option>
            <option value="read">Прочитано</option>
            <option value="dropped">Отложено</option>
          </select>
        </label>

        <div class="row2" style="margin-top:6px">
          <button type="submit" class="btn btn-primary">
            {{ modalMode === 'add' ? 'Добавить' : 'Сохранить' }}
          </button>
          <button type="button" class="btn" @click="closeModal">Отмена</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Всплывающее уведомление (Toast) -->
  <div class="toast" :class="{ show: toast.show }">
    {{ toast.text }}
  </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, nextTick } from 'vue';

const LS_KEY = 'bookshelf_v2';
const LS_VIEW = 'bookshelf_view';
const LS_THEME = 'bookshelf_theme';
const LS_STALKER_BG = 'bookshelf_stalker_bg';

// --- Состояние данных ---
const books = ref([]);
const filter = ref('all');
const query = ref('');
const sort = ref('newest');
const viewMode = ref('grid');
const theme = ref('light');
const stalkerBg = ref('menu');
const statsExpanded = ref(false);
const activeStatusMenu = ref(null);

// Модальное окно
const modalOpen = ref(false);
const modalMode = ref('add'); // 'add' | 'edit'
const editingId = ref(null);
const coverSearching = ref(false);
const authorInput = ref(null);

const form = reactive({
  id: null,
  author: '',
  title: '',
  characters: '',
  description: '',
  link: '',
  cover: '',
  status: 'planned'
});

// Уведомления
const toast = reactive({ show: false, text: '' });
let toastTimeout = null;

// --- Звуки для темы S.T.A.L.K.E.R. ---
let audioCtx = null;
function playPdaBeep(freq = 900, duration = 0.04) {
  if (theme.value !== 'stalker') return;
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
  } catch (e) {}
}

function playMenuClick() {
  if (theme.value !== 'stalker') return;
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(320, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(90, audioCtx.currentTime + 0.04);
    gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.045);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.045);
  } catch(e) {}
}

function playMenuHover() {
  if (theme.value !== 'stalker') return;
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(700, audioCtx.currentTime + 0.02);
    gain.gain.setValueAtTime(0.015, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.02);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.02);
  } catch(e) {}
}

// --- Загрузка и инициализация ---
function loadStorage() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    books.value = raw ? JSON.parse(raw) : [];
  } catch (e) {
    books.value = [];
  }
  // Нормализация полей
  books.value.forEach(b => {
    if (!('characters' in b)) b.characters = '';
    if (!('description' in b)) b.description = '';
    if (!('cover' in b)) b.cover = '';
  });

  // Тема
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const urlTheme = urlParams.get('theme');
    if (['light', 'dark', 'stalker'].includes(urlTheme)) {
      theme.value = urlTheme;
    } else {
      const savedTheme = localStorage.getItem(LS_THEME);
      if (['light', 'dark', 'stalker'].includes(savedTheme)) {
        theme.value = savedTheme;
      } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        theme.value = 'dark';
      }
    }
    if (urlParams.get('demo') === '1' && books.value.length === 0) {
      loadDemo();
    }
  } catch (e) {}

  // Обои Сталкера
  try {
    const savedBg = localStorage.getItem(LS_STALKER_BG);
    if (['menu', 'tractor', 'barrel'].includes(savedBg)) {
      stalkerBg.value = savedBg;
    }
  } catch (e) {}
  document.documentElement.setAttribute('data-stalker-bg', stalkerBg.value);

  // Режим вида
  try {
    const savedView = localStorage.getItem(LS_VIEW);
    if (['grid', 'table'].includes(savedView)) viewMode.value = savedView;
  } catch (e) {}

  applyTheme(theme.value);
}

function saveStorage() {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(books.value));
  } catch (e) {}
}

// Автоматическое сохранение при изменении книг
watch(books, () => saveStorage(), { deep: true });

// --- Темы ---
function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  try { localStorage.setItem(LS_THEME, t); } catch (e) {}
}
function setTheme(t) {
  theme.value = t;
  applyTheme(t);
  playMenuClick();
  showToast('Тема: ' + (t === 'stalker' ? 'S.T.A.L.K.E.R. Главное меню & КПК' : t === 'dark' ? 'Тёмная' : 'Светлая'));
}
function setStalkerBg(bg) {
  stalkerBg.value = bg;
  try { localStorage.setItem(LS_STALKER_BG, bg); } catch (e) {}
  document.documentElement.setAttribute('data-stalker-bg', bg);
  playMenuClick();
}
function setViewMode(v) {
  viewMode.value = v;
  try { localStorage.setItem(LS_VIEW, v); } catch (e) {}
  playPdaBeep(850, 0.03);
}

// --- Вычисляемые свойства (Computed) ---
const stats = computed(() => {
  const total = books.value.length;
  const read = books.value.filter(b => b.status === 'read').length;
  const reading = books.value.filter(b => b.status === 'reading').length;
  const planned = books.value.filter(b => b.status === 'planned').length;
  const dropped = books.value.filter(b => b.status === 'dropped').length;
  return { total, read, reading, planned, dropped };
});

const counts = computed(() => ({
  all: books.value.length,
  planned: books.value.filter(b => b.status === 'planned').length,
  reading: books.value.filter(b => b.status === 'reading').length,
  read: books.value.filter(b => b.status === 'read').length,
  dropped: books.value.filter(b => b.status === 'dropped').length,
}));

const statusLabels = computed(() => {
  if (theme.value === 'stalker') {
    return {
      planned: '[ЦЕЛЬ: ВЗЯТО]',
      reading: '[В ПРОЦЕССЕ]',
      read: '[ВЫПОЛНЕНО]',
      dropped: '[ОТМЕНЕНО]'
    };
  }
  return {
    planned: 'В планах',
    reading: 'Читаю',
    read: 'Прочитано',
    dropped: 'Отложено'
  };
});

const brandTitle = computed(() => theme.value === 'stalker' ? 'КПК v2.04' : 'VFYARL');
const brandSubtitle = computed(() => theme.value === 'stalker' ? 'Архив Зоны // Список литературы' : "VantuzFed's Reading List");

const filteredBooks = computed(() => {
  let arr = [...books.value];
  if (filter.value !== 'all') {
    arr = arr.filter(b => b.status === filter.value);
  }
  if (query.value.trim()) {
    const q = query.value.toLowerCase().trim();
    arr = arr.filter(b =>
      [b.author, b.title, b.characters, b.description, b.link]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
        .includes(q)
    );
  }
  if (sort.value === 'author') {
    arr.sort((a, b) => a.author.localeCompare(b.author, 'ru'));
  } else if (sort.value === 'title') {
    arr.sort((a, b) => a.title.localeCompare(b.title, 'ru'));
  } else if (sort.value === 'status') {
    arr.sort((a, b) => a.status.localeCompare(b.status));
  } else {
    arr.sort((a, b) => (b.created || 0) - (a.created || 0));
  }
  return arr;
});

// --- Вспомогательные функции ---
function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

function host(url) {
  try {
    return new URL(url).hostname.replace('www.', '');
  } catch (e) {
    return (url || '').slice(0, 24);
  }
}

function plural(n) {
  if (n % 10 === 1 && n % 100 !== 11) return 'книга';
  if ([2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100)) return 'книги';
  return 'книг';
}

function showToast(msg) {
  toast.text = msg;
  toast.show = true;
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => { toast.show = false; }, 2300);
}

// --- Действия с книгами ---
function openAddModal() {
  modalMode.value = 'add';
  editingId.value = null;
  form.id = null;
  form.author = '';
  form.title = '';
  form.characters = '';
  form.description = '';
  form.link = '';
  form.cover = '';
  form.status = 'planned';
  modalOpen.value = true;
  playPdaBeep(1200, 0.04);
  nextTick(() => { authorInput.value?.focus(); });
}

function openEditModal(book) {
  modalMode.value = 'edit';
  editingId.value = book.id;
  form.id = book.id;
  form.author = book.author || '';
  form.title = book.title || '';
  form.characters = book.characters || '';
  form.description = book.description || '';
  form.link = book.link || '';
  form.cover = book.cover || '';
  form.status = book.status || 'planned';
  modalOpen.value = true;
  playPdaBeep(1000, 0.04);
  nextTick(() => { authorInput.value?.focus(); });
}

function closeModal() {
  modalOpen.value = false;
  editingId.value = null;
}

async function saveBook() {
  if (!form.author || !form.title) {
    showToast('Укажите автора и название книги');
    return;
  }

  if (!form.cover && form.title) {
    try {
      coverSearching.value = true;
      const found = await fetchCover(form.title, form.author);
      if (found) form.cover = found;
    } catch (e) {} finally {
      coverSearching.value = false;
    }
  }

  if (modalMode.value === 'add') {
    const newBook = {
      id: uid(),
      author: form.author,
      title: form.title,
      characters: form.characters,
      description: form.description,
      link: form.link,
      cover: form.cover,
      status: form.status,
      created: Date.now()
    };
    books.value.unshift(newBook);
    showToast('Книга добавлена');
  } else {
    const target = books.value.find(b => b.id === editingId.value);
    if (target) {
      target.author = form.author;
      target.title = form.title;
      target.characters = form.characters;
      target.description = form.description;
      target.link = form.link;
      target.cover = form.cover;
      target.status = form.status;
      target.updated = Date.now();
    }
    showToast('Изменения сохранены');
  }

  closeModal();
  playPdaBeep(1400, 0.05);
}

function deleteBook(id) {
  playPdaBeep(600, 0.06);
  if (!confirm('Удалить эту книгу из списка?')) return;
  books.value = books.value.filter(b => b.id !== id);
  showToast('Книга удалена');
}

function toggleStatusMenu(id) {
  activeStatusMenu.value = activeStatusMenu.value === id ? null : id;
  playPdaBeep(900, 0.03);
}

function updateStatus(id, newStatus) {
  const b = books.value.find(x => x.id === id);
  if (b) {
    b.status = newStatus;
    showToast('Статус изменён');
    playPdaBeep(1050, 0.04);
  }
  activeStatusMenu.value = null;
}

// --- Автопоиск обложки ---
async function fetchCover(title, author) {
  if (!title) return null;
  try {
    const q = `intitle:${title}` + (author ? `+inauthor:${author}` : '');
    const r = await fetch(`https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(q)}&maxResults=1`);
    if (r.ok) {
      const d = await r.json();
      const links = d.items?.[0]?.volumeInfo?.imageLinks;
      if (links) {
        let u = links.thumbnail || links.smallThumbnail || links.medium;
        if (u) return u.replace('http://', 'https://').replace('&zoom=1', '&zoom=3').replace('&edge=curl', '');
      }
    }
  } catch (e) {}

  try {
    const params = new URLSearchParams({ title, limit: '5' });
    if (author) params.set('author', author);
    const r = await fetch(`https://openlibrary.org/search.json?${params.toString()}`);
    if (r.ok) {
      const j = await r.json();
      for (const doc of j.docs || []) {
        if (doc.cover_i) return `https://covers.openlibrary.org/b/id/${doc.cover_i}-L.jpg`;
        if (doc.cover_edition_key) return `https://covers.openlibrary.org/b/olid/${doc.cover_edition_key}-L.jpg`;
      }
    }
  } catch (e) {}
  return null;
}

async function findCover() {
  if (!form.title) {
    showToast('Сначала введите название книги');
    return;
  }
  coverSearching.value = true;
  playPdaBeep(800, 0.05);
  const url = await fetchCover(form.title, form.author);
  coverSearching.value = false;
  if (url) {
    form.cover = url;
    showToast('Обложка найдена!');
    playPdaBeep(1300, 0.06);
  } else {
    showToast('Обложка не найдена, проверьте название');
  }
}

// --- Импорт и Экспорт ---
function downloadFile(filename, content, mime) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function exportJson() {
  if (!books.value.length) return showToast('Список книг пуст');
  const json = JSON.stringify(books.value, null, 2);
  downloadFile(`books-${new Date().toISOString().slice(0, 10)}.json`, json, 'application/json');
  showToast('JSON экспортирован');
  playPdaBeep(1200, 0.04);
}

function exportCsv() {
  if (!books.value.length) return showToast('Список книг пуст');
  const headers = ['author', 'title', 'characters', 'description', 'link', 'cover', 'status'];
  const rows = books.value.map(b =>
    headers.map(h => `"${String(b[h] || '').replace(/"/g, '""')}"`).join(',')
  );
  const csv = [headers.join(','), ...rows].join('\n');
  downloadFile(`books-${new Date().toISOString().slice(0, 10)}.csv`, csv, 'text/csv;charset=utf-8');
  showToast('CSV экспортирован');
  playPdaBeep(1200, 0.04);
}

async function copyJson() {
  if (!books.value.length) return showToast('Список книг пуст');
  try {
    await navigator.clipboard.writeText(JSON.stringify(books.value, null, 2));
    showToast('JSON скопирован в буфер обмена');
    playPdaBeep(1100, 0.04);
  } catch (e) {
    showToast('Не удалось скопировать');
  }
}

function parseCsvLine(line) {
  const out = [];
  let cur = '';
  let inQ = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (c === '"') {
      if (inQ && line[i + 1] === '"') { cur += '"'; i++; }
      else inQ = !inQ;
    } else if (c === ',' && !inQ) {
      out.push(cur);
      cur = '';
    } else {
      cur += c;
    }
  }
  out.push(cur);
  return out.map(s => s.trim());
}

async function handleFileImport(e) {
  const file = e.target.files?.[0];
  if (!file) return;
  try {
    const text = await file.text();
    let imported = [];
    if (file.name.endsWith('.json')) {
      const parsed = JSON.parse(text);
      imported = Array.isArray(parsed) ? parsed : [parsed];
    } else if (file.name.endsWith('.csv')) {
      const lines = text.split(/\r?\n/).filter(Boolean);
      const headers = lines[0].split(',').map(s => s.replace(/"/g, '').trim().toLowerCase());
      const idx = name => headers.indexOf(name);
      for (let i = 1; i < lines.length; i++) {
        const cols = parseCsvLine(lines[i]);
        imported.push({
          author: cols[idx('author')] || '',
          title: cols[idx('title')] || '',
          characters: cols[idx('characters')] || cols[idx('heroes')] || cols[idx('герои')] || '',
          description: cols[idx('description')] || cols[idx('desc')] || '',
          link: cols[idx('link')] || '',
          cover: cols[idx('cover')] || '',
          status: cols[idx('status')] || 'planned'
        });
      }
    } else {
      return showToast('Поддерживаются файлы .json и .csv');
    }

    let added = 0;
    imported.forEach(r => {
      if (!r.author || !r.title) return;
      const exists = books.value.some(b =>
        (r.link && b.link === r.link) ||
        (b.author.toLowerCase() === r.author.toLowerCase() && b.title.toLowerCase() === r.title.toLowerCase())
      );
      if (exists) return;
      books.value.push({
        id: uid(),
        author: String(r.author).trim(),
        title: String(r.title).trim(),
        characters: String(r.characters || '').trim(),
        description: String(r.description || '').trim(),
        link: String(r.link || '').trim(),
        cover: String(r.cover || '').trim(),
        status: ['planned', 'reading', 'read', 'dropped'].includes(r.status) ? r.status : 'planned',
        created: Date.now()
      });
      added++;
    });

    showToast(`Импортировано: ${added} книг (пропущено дубликатов: ${imported.length - added})`);
    playPdaBeep(1300, 0.05);
  } catch (err) {
    showToast('Ошибка импорта: ' + err.message);
  } finally {
    e.target.value = '';
  }
}

// --- Демо-данные ---
function loadDemo() {
  const demo = [
    {
      author: 'Фёдор Достоевский',
      title: 'Преступление и наказание',
      characters: 'Родион Раскольников, Соня Мармеладова, Порфирий Петрович',
      cover: 'https://covers.openlibrary.org/b/isbn/9785389057871-L.jpg',
      link: 'https://knigopoisk.com/dostoevsky_prestuplenie',
      description: 'Классический роман о морали, вине и искуплении студента Родиона Раскольникова.',
      status: 'read'
    },
    {
      author: 'Джордж Оруэлл',
      title: '1984',
      characters: 'Уинстон Смит, Джулия, О’Брайен',
      cover: 'https://covers.openlibrary.org/b/isbn/9785170801152-L.jpg',
      link: 'https://www.litres.ru/dzhordzh-oruell/1984-121402/',
      description: 'Культовая антиутопия о тоталитарном государстве, всевидящем Большом Брате и двоемыслии.',
      status: 'reading'
    },
    {
      author: 'Антуан де Сент-Экзюпери',
      title: 'Маленький принц',
      characters: 'Маленький принц, Лётчик, Лис, Роза',
      cover: '',
      link: '',
      description: 'Философская сказка-притча о дружбе, любви, верности и ответственности за тех, кого приручили.',
      status: 'planned'
    },
    {
      author: 'Харуки Мураками',
      title: 'Норвежский лес',
      characters: 'Тору Ватанабэ, Наоко, Мидори Кобаяси',
      cover: 'https://covers.openlibrary.org/b/isbn/9785699404097-L.jpg',
      link: 'https://example.com/murakami',
      description: 'Глубокий ностальгический роман о студенческих годах в Токио 60-х, потерях и взрослении.',
      status: 'dropped'
    }
  ];

  let added = 0;
  demo.forEach(d => {
    if (books.value.some(b => b.title === d.title && b.author === d.author)) return;
    books.value.unshift({ id: uid(), ...d, created: Date.now() - added * 1000 });
    added++;
  });
  showToast(added ? `Добавлено ${added} демо-книг` : 'Все демо-книги уже есть в списке');
  playPdaBeep(1400, 0.05);
}

function clearAll() {
  if (!books.value.length) return showToast('Список уже пуст');
  if (confirm(`Удалить все ${books.value.length} книг? Действие необратимо.`)) {
    books.value = [];
    showToast('Список очищен');
    playPdaBeep(500, 0.08);
  }
}

// --- Обработчики глобальных событий ---
onMounted(() => {
  loadStorage();

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.status-select-wrap')) {
      activeStatusMenu.value = null;
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
      activeStatusMenu.value = null;
    }
  });
});
</script>

// Сервис хранения данных (Storage Service)
// На данном этапе работает локально через LocalStorage + экспорт/импорт.
// Для будущего перехода на клиент-серверное веб-приложение достаточно
// заменить методы этого сервиса на вызовы REST API (axios / fetch).

const STORAGE_KEY = 'bookshelf_v2';
const THEME_KEY = 'bookshelf_theme';
const VIEW_KEY = 'bookshelf_view';

export const storageService = {
  // Получить все книги
  getBooks() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      const books = data ? JSON.parse(data) : [];
      return books.map(b => ({
        characters: '',
        description: '',
        cover: '',
        ...b
      }));
    } catch (e) {
      console.error('Ошибка чтения LocalStorage:', e);
      return [];
    }
  },

  // Сохранить книги
  saveBooks(books) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
    } catch (e) {
      console.error('Ошибка записи LocalStorage:', e);
    }
  },

  // Тема оформления
  getTheme() {
    try {
      return localStorage.getItem(THEME_KEY) || 'light';
    } catch (e) {
      return 'light';
    }
  },

  saveTheme(theme) {
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch (e) {}
  },

  // Режим отображения (grid / table)
  getViewMode() {
    try {
      return localStorage.getItem(VIEW_KEY) || 'grid';
    } catch (e) {
      return 'grid';
    }
  },

  saveViewMode(mode) {
    try {
      localStorage.setItem(VIEW_KEY, mode);
    } catch (e) {}
  },

  // Экспорт файлов
  exportJson(books) {
    const json = JSON.stringify(books, null, 2);
    this._downloadFile(`books-${new Date().toISOString().slice(0, 10)}.json`, json, 'application/json');
  },

  exportCsv(books) {
    const headers = ['author', 'title', 'characters', 'description', 'link', 'cover', 'status'];
    const rows = books.map(b =>
      headers.map(h => `"${String(b[h] || '').replace(/"/g, '""')}"`).join(',')
    );
    const csv = [headers.join(','), ...rows].join('\n');
    this._downloadFile(`books-${new Date().toISOString().slice(0, 10)}.csv`, csv, 'text/csv;charset=utf-8');
  },

  _downloadFile(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
};

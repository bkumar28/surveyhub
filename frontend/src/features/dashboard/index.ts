export { StatsCard } from './components';
export { DashboardPage } from './pages';
// Same pattern - export both the slice and reducer
export { default as dashboardReducer } from './dashboardSlice';
export { fetchDashboardStats } from './dashboardSlice';

import { configureStore } from '@reduxjs/toolkit';
import { authSlice } from '../../features/auth/store/authSlice';
import { dashboardSlice } from '../../features/dashboard/store/dashboardSlice';
import { surveySlice } from '../../features/surveys/store/surveySlice';

export const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
    dashboard: dashboardSlice.reducer,
    surveys: surveySlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiClient } from '../../shared/services/apiClient';
import { DashboardStats, DashboardState } from '../../shared/types/api';

const initialState: DashboardState = {
  stats: null,
  loading: false,
  error: null,
};

// Thunk
export const fetchDashboardStats = createAsyncThunk(
  'dashboard/fetchStats',
  async (_, { rejectWithValue }) => {
    try {
      // Updated path to match your actual API endpoint
      const response = await apiClient.get<DashboardStats>('/dashboard/stats/');
      return response.data;
    } catch (error: any) {
      // Return detailed error message but don't affect auth state
      return rejectWithValue(
        error.response?.data?.detail ||
        `Unable to load dashboard data (${error.response?.status || 'Network error'})`
      );
    }
  }
);

// Slice
const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    clearDashboardErrors: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboardStats.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDashboardStats.fulfilled, (state, action: PayloadAction<DashboardStats>) => {
        state.loading = false;
        state.stats = action.payload;
      })
      .addCase(fetchDashboardStats.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Failed to load dashboard stats';
        // Important: Do NOT modify auth state here
      });
  },
});

export const { clearDashboardErrors } = dashboardSlice.actions;
export default dashboardSlice.reducer;

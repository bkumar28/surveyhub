import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiClient } from '../../shared/services/apiClient';
import {
  User,
  LoginCredentials,
  LoginData,
  AuthState
} from '../../shared/types/api';

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('access_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),
  loading: false,
  error: null,
};

// Thunks
export const login = createAsyncThunk(
  'auth/login',
  async (credentials: LoginCredentials, { rejectWithValue }) => {
    try {
      const response = await apiClient.post<LoginData>('/token/', credentials);
      const { user, access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      // Optionally, persist user in localStorage if you want to restore on reload
      localStorage.setItem('user', JSON.stringify(user));
      return { user, access_token };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Login failed');
    }
  }
);

export const logout = createAsyncThunk('auth/logout', async () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
  return true;
});

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    restoreAuth: (state) => {
      const token = localStorage.getItem('access_token');
      const user = localStorage.getItem('user');
      state.token = token;
      state.isAuthenticated = !!token;
      state.user = user ? JSON.parse(user) : null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Login cases
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action: PayloadAction<{ user: User; access_token: string }>) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.access_token;
        state.error = null;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Logout cases
      .addCase(logout.fulfilled, (state) => {
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      });
  },
});

// Export the action creators
export const { clearError, restoreAuth } = authSlice.actions;

export default authSlice.reducer;

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

// Define auth state interface
interface AuthState {
  isAuthenticated: boolean;
  user: any | null;
  loading: boolean;
  error: string | null;
}

// Initial state
const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null,
};

// API URLs
const API_URL = '/api/v1';

// Async thunks for auth actions
export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password, rememberMe }: { email: string; password: string; rememberMe: boolean }, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/token/`, { email, password });

      // Store token in localStorage or sessionStorage based on rememberMe
      const storage = rememberMe ? localStorage : sessionStorage;
      storage.setItem('access_token', response.data.access_token);

      return response.data;
    } catch (error: any) {
      const message = error.response?.data?.message || error.message || 'Failed to login';
      return rejectWithValue(message);
    }
  }
);

// Register new user
export const register = createAsyncThunk(
  'auth/register',
  async ({
    name,
    email,
    password,
    confirmPassword
  }: {
    name: string;
    email: string;
    password: string;
    confirmPassword: string
  }, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/register`, {
        name,
        email,
        password,
        password_confirmation: confirmPassword
      });

      // Store token if automatically logged in after registration
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
      }

      return response.data;
    } catch (error: any) {
      const message = error.response?.data?.message || error.message || 'Failed to register';
      return rejectWithValue(message);
    }
  }
);

// Forgot password request
export const forgotPassword = createAsyncThunk(
  'auth/forgotPassword',
  async ({ email }: { email: string }, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/forgot-password`, { email });
      return response.data;
    } catch (error: any) {
      const message = error.response?.data?.message || error.message || 'Failed to send reset link';
      return rejectWithValue(message);
    }
  }
);

// Reset password with token
export const resetPassword = createAsyncThunk(
  'auth/resetPassword',
  async ({ token, password }: { token: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/reset-password`, {
        token,
        password,
        password_confirmation: password
      });
      return response.data;
    } catch (error: any) {
      const message = error.response?.data?.message || error.message || 'Failed to reset password';
      return rejectWithValue(message);
    }
  }
);

// Get current user info
export const getCurrentUser = createAsyncThunk(
  'auth/getCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${API_URL}/me`);
      return response.data;
    } catch (error: any) {
      const message = error.response?.data?.message || error.message || 'Failed to get user info';
      return rejectWithValue(message);
    }
  }
);

// Restore auth state from token
export const restoreAuth = createAsyncThunk(
  'auth/restoreAuth',
  async (_, { dispatch }) => {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');

    if (!token) {
      return { isAuthenticated: false };
    }

    // Set auth header
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    // Try to get current user
    try {
      const response = await dispatch(getCurrentUser()).unwrap();
      return {
        isAuthenticated: true,
        user: response.user
      };
    } catch (error) {
      // Clear tokens if invalid
      localStorage.removeItem('access_token');
      sessionStorage.removeItem('access_token');
      delete axios.defaults.headers.common['Authorization'];

      return { isAuthenticated: false };
    }
  }
);

// Logout
export const logout = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      // Call logout API if needed
      // await axios.post(`${API_URL}/logout`);

      // Clear tokens
      localStorage.removeItem('access_token');
      sessionStorage.removeItem('access_token');
      delete axios.defaults.headers.common['Authorization'];

      return true;
    } catch (error: any) {
      const message = error.response?.data?.message || error.message || 'Failed to logout';
      return rejectWithValue(message);
    }
  }
);

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearAuthError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Login reducers
    builder.addCase(login.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(login.fulfilled, (state, action) => {
      state.loading = false;
      state.isAuthenticated = true;
      state.user = action.payload.user;
    });
    builder.addCase(login.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Register reducers
    builder.addCase(register.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(register.fulfilled, (state, action) => {
      state.loading = false;
      if (action.payload.access_token) {
        state.isAuthenticated = true;
        state.user = action.payload.user;
      }
    });
    builder.addCase(register.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Forgot password reducers
    builder.addCase(forgotPassword.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(forgotPassword.fulfilled, (state) => {
      state.loading = false;
    });
    builder.addCase(forgotPassword.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Reset password reducers
    builder.addCase(resetPassword.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(resetPassword.fulfilled, (state) => {
      state.loading = false;
    });
    builder.addCase(resetPassword.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Get current user reducers
    builder.addCase(getCurrentUser.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(getCurrentUser.fulfilled, (state, action) => {
      state.loading = false;
      state.isAuthenticated = true;
      state.user = action.payload.user;
    });
    builder.addCase(getCurrentUser.rejected, (state, action) => {
      state.loading = false;
      state.isAuthenticated = false;
      state.error = action.payload as string;
    });

    // Restore auth reducers
    builder.addCase(restoreAuth.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(restoreAuth.fulfilled, (state, action) => {
      state.loading = false;
      state.isAuthenticated = action.payload.isAuthenticated;
      state.user = action.payload.user || null;
    });

    // Logout reducers
    builder.addCase(logout.fulfilled, (state) => {
      state.isAuthenticated = false;
      state.user = null;
    });
  },
});

export const { clearAuthError } = authSlice.actions;
export default authSlice.reducer;

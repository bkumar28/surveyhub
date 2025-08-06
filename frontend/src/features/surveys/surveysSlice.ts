import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiClient } from '../../shared/services/apiClient';

interface Survey {
  id: string;
  title: string;
  description: string;
  status: 'draft' | 'published' | 'closed';
  createdAt: string;
  updatedAt: string;
  responseCount: number;
}

interface SurveysState {
  surveys: Survey[];
  currentSurvey: Survey | null;
  loading: boolean;
  error: string | null;
}

export const fetchSurveys = createAsyncThunk(
  'surveys/fetchSurveys',
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiClient.get('/surveys/');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch surveys');
    }
  }
);

export const createSurvey = createAsyncThunk(
  'surveys/createSurvey',
  async (surveyData: Partial<Survey>, { rejectWithValue }) => {
    try {
      const response = await apiClient.post('/surveys/', surveyData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create survey');
    }
  }
);

const initialState: SurveysState = {
  surveys: [],
  currentSurvey: null,
  loading: false,
  error: null,
};

const surveysSlice = createSlice({
  name: 'surveys',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentSurvey: (state, action) => {
      state.currentSurvey = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchSurveys.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSurveys.fulfilled, (state, action) => {
        state.loading = false;
        state.surveys = action.payload;
      })
      .addCase(fetchSurveys.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createSurvey.fulfilled, (state, action) => {
        state.surveys.push(action.payload);
      });
  },
});

export const { clearError, setCurrentSurvey } = surveysSlice.actions;
export default surveysSlice.reducer;

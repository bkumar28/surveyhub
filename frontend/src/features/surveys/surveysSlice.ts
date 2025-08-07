import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiClient } from '../../shared/services/apiClient';
import { Survey, ApiResponse, PaginatedResponse } from '../../shared/types/api';

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
      state.currentSurvey = action.payload as Survey;
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
        // If your API returns paginated response:
        const payload = action.payload as PaginatedResponse<Survey>;
        state.surveys = payload.results;
        // OR if your API returns direct array:
        // state.surveys = action.payload as Survey[];
      })
      .addCase(fetchSurveys.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createSurvey.fulfilled, (state, action) => {
        const newSurvey = action.payload as ApiResponse<Survey>;
        state.surveys.push(newSurvey.data);
      });
  },
});

export const { clearError, setCurrentSurvey } = surveysSlice.actions;

// Export the slice itself for named export
export { surveysSlice };
// Keep default export for reducer
export default surveysSlice.reducer;

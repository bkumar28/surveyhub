import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Updated BASE_URL to match your actual API endpoint structure
const BASE_URL = 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 10000, // 10 seconds instead of 10ms which is too short
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - to handle errors properly
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error) => {
        // Only redirect on auth errors (401), not on 404/500
        if (error.response?.status === 401) {
          // Remove token but don't redirect from here
          localStorage.removeItem('access_token');
        }
        return Promise.reject(error);
      }
    );
  }

  public get<T>(url: string): Promise<AxiosResponse<T>> {
    return this.client.get<T>(url);
  }

  public post<T>(url: string, data?: any): Promise<AxiosResponse<T>> {
    return this.client.post<T>(url, data);
  }

  public put<T>(url: string, data?: any): Promise<AxiosResponse<T>> {
    return this.client.put<T>(url, data);
  }

  public delete<T>(url: string): Promise<AxiosResponse<T>> {
    return this.client.delete<T>(url);
  }
}

export const apiClient = new ApiClient();

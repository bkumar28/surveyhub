interface Config {
  API_BASE_URL: string;
  STRIPE_PUBLIC_KEY?: string;
  GA_TRACKING_ID?: string;
}

const config: Record<string, Config> = {
  development: {
    API_BASE_URL:
      process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api',
    STRIPE_PUBLIC_KEY: process.env.REACT_APP_STRIPE_PUBLIC_KEY,
    GA_TRACKING_ID: process.env.REACT_APP_GA_TRACKING_ID,
  },
  production: {
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL || '',
    STRIPE_PUBLIC_KEY: process.env.REACT_APP_STRIPE_PUBLIC_KEY,
    GA_TRACKING_ID: process.env.REACT_APP_GA_TRACKING_ID,
  },
};

const environment = process.env.NODE_ENV || 'development';

export default config[environment];

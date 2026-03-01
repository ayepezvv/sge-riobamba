// third party
import { Roboto } from 'next/font/google';

// types
import { ConfigStates } from 'types/config';

export const DASHBOARD_PATH = '/dashboard/default';
export const HORIZONTAL_MAX_ITEM = 7;

const roboto = Roboto({ subsets: ['latin'], weight: ['300', '400', '500', '700'] });

export const CSS_VAR_PREFIX = '';

export enum MenuOrientation {
  VERTICAL = 'vertical',
  HORIZONTAL = 'horizontal'
}

export enum ThemeMode {
  LIGHT = 'light',
  DARK = 'dark',
  SYSTEM = 'system'
}

export enum ThemeDirection {
  LTR = 'ltr',
  RTL = 'rtl'
}

export enum AuthProvider {
  JWT = 'jwt',
  FIREBASE = 'firebase',
  AUTH0 = 'auth0',
  AWS = 'aws',
  SUPABASE = 'supabase'
}

export enum DropzopType {
  default = 'DEFAULT',
  standard = 'STANDARD'
}

export const APP_AUTH: AuthProvider = AuthProvider.JWT;
export const DEFAULT_THEME_MODE: ThemeMode = ThemeMode.SYSTEM;

const config: ConfigStates = {
  menuOrientation: MenuOrientation.VERTICAL,
  miniDrawer: false,
  fontFamily: roboto.style.fontFamily,
  borderRadius: 8,
  outlinedFilled: true,
  presetColor: 'default',
  i18n: 'en',
  themeDirection: ThemeDirection.LTR,
  container: true
};

export default config;

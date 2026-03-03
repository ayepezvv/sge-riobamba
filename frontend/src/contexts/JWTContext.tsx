'use client';

import { createContext, ReactElement, useEffect, useReducer } from 'react';

// third party
import { Chance } from 'chance';
import { jwtDecode } from 'jwt-decode';

// reducer - state management
import { LOGIN, LOGOUT } from 'store/actions';
import accountReducer from 'store/accountReducer';

// project imports
import Loader from 'ui-component/Loader';
import axios from 'utils/axios';

// types
import { KeyedObject } from 'types';
import { InitialLoginContextProps, JWTContextType } from 'types/auth';

const chance = new Chance();

// constant
const initialState: InitialLoginContextProps = {
  isLoggedIn: false,
  isInitialized: false,
  user: null
};

const verifyToken: (st: string) => boolean = (serviceToken) => {
  if (!serviceToken) {
    return false;
  }
  const decoded: KeyedObject = jwtDecode(serviceToken);
  /**
   * Property 'exp' does not exist on type '<T = unknown>(token: string, options?: JwtDecodeOptions | undefined) => T'.
   */
  return decoded.exp > Date.now() / 1000;
};

const setSession = (serviceToken?: string | null) => {
  if (serviceToken) {
    localStorage.setItem('serviceToken', serviceToken);
    axios.defaults.headers.common.Authorization = `Bearer ${serviceToken}`;
  } else {
    localStorage.removeItem('serviceToken');
    delete axios.defaults.headers.common.Authorization;
  }
};

// ==============================|| JWT CONTEXT & PROVIDER ||============================== //
const JWTContext = createContext<JWTContextType | null>(null);

export const JWTProvider = ({ children }: { children: ReactElement }) => {
  const [state, dispatch] = useReducer(accountReducer, initialState);

  useEffect(() => {
    const init = async () => {
      try {
        const serviceToken = window.localStorage.getItem('serviceToken');
        if (serviceToken && verifyToken(serviceToken)) {
          setSession(serviceToken);
          const response = await axios.get('/api/users/me');
          const rawUser = response.data;
          const user = {
            ...rawUser,
            id: String(rawUser.id),
            name: `${rawUser.nombres} ${rawUser.apellidos}`,
            email: rawUser.correo,
            role: 'Admin'
          };
          dispatch({
            type: LOGIN,
            payload: {
              isLoggedIn: true,
              user
            }
          });
        } else {
          dispatch({
            type: LOGOUT
          });
        }
      } catch (err: any) {
        console.error("JWT Init Error:", err);
        setSession(null);
        dispatch({
          type: LOGOUT
        });
      }
    };

    init();
  }, []);

  const login = async (email: string, password: string) => {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    const response = await axios.post('/api/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    const serviceToken = response.data.access_token;
    setSession(serviceToken);
    
    const meResponse = await axios.get('/api/users/me');
    const rawUser = meResponse.data;
    const user = {
      ...rawUser,
      id: String(rawUser.id),
      name: `${rawUser.nombres} ${rawUser.apellidos}`,
      email: rawUser.correo,
      role: 'Admin'
    };
    
    dispatch({
      type: LOGIN,
      payload: {
        isLoggedIn: true,
        user
      }
    });
  };

  const register = async (email: string, password: string, firstName: string, lastName: string) => {
    // todo: this flow need to be recode as it not verified
    const id = chance.bb_pin();
    const response = await axios.post('/api/account/register', {
      id,
      email,
      password,
      firstName,
      lastName
    });
    let users = response.data;

    if (typeof window !== 'undefined') {
      if (window.localStorage.getItem('users') !== undefined && window.localStorage.getItem('users') !== null) {
        const localUsers = window.localStorage.getItem('users');
        users = [
          ...JSON.parse(localUsers!),
          {
            id,
            email,
            password,
            name: `${firstName} ${lastName}`
          }
        ];
      }

      window.localStorage.setItem('users', JSON.stringify(users));
    }
  };

  const logout = () => {
    setSession(null);
    dispatch({ type: LOGOUT });
  };

  const resetPassword = async (email: string) => {};

  const updateProfile = () => {};

  if (state.isInitialized !== undefined && !state.isInitialized) {
    return <Loader />;
  }

  return <JWTContext value={{ ...state, login, logout, register, resetPassword, updateProfile }}>{children}</JWTContext>;
};

export default JWTContext;

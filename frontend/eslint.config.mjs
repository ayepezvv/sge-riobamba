import eslint from '@eslint/js';
import { defineConfig, globalIgnores } from 'eslint/config';
import tseslint from 'typescript-eslint';
import nextCoreWebVitals from 'eslint-config-next/core-web-vitals';
import nextTs from 'eslint-config-next/typescript';
import nextPlugin from '@next/eslint-plugin-next';
import prettier from 'eslint-config-prettier/flat';
import prettierPlugin from 'eslint-plugin-prettier';
import tsParser from '@typescript-eslint/parser';

/**
 * ESLint Flat Config
 * Compatible with ESLint 9+ and TypeScript-ESLint 8+
 */
export default defineConfig([
  // Base ESLint + TypeScript recommendations
  eslint.configs.recommended,
  ...tseslint.configs.recommended,

  // Next.js recommended configs
  ...nextCoreWebVitals,
  ...nextTs,

  // Custom project setup
  {
    plugins: {
      next: nextPlugin,
      prettier: prettierPlugin
    },

    languageOptions: {
      parser: tsParser,
      ecmaVersion: 'latest',
      sourceType: 'module',
      parserOptions: {
        project: './tsconfig.json',
        createDefaultProgram: true
      }
    },

    rules: {
      // --- TypeScript & React rules ---
      'react/jsx-filename-extension': 'off',
      'no-param-reassign': 'off',
      'react/prop-types': 'off',
      'react/require-default-props': 'off',
      'react/no-array-index-key': 'off',
      'react/react-in-jsx-scope': 'off',
      'react/jsx-props-no-spreading': 'off',
      'react/display-name': 'off',
      'no-console': 'off',
      'no-shadow': 'off',
      'prefer-destructuring': 'off',

      '@typescript-eslint/naming-convention': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { vars: 'all', args: 'none' }],

      'react-hooks/purity': 'off',
      'react-hooks/refs': 'off',
      'react-hooks/set-state-in-effect': 'off',
      'react-hooks/immutability': 'off',

      // --- Import rules ---
      'import/no-cycle': 'off',
      'import/order': 'off',
      'import/no-extraneous-dependencies': 'off',
      'import/no-unresolved': ['off', { caseSensitive: false }],

      // --- Project-specific restrictions ---
      'no-restricted-imports': [
        'error',
        {
          patterns: ['@mui/*/*/*', '!@mui/material/test-utils/*']
        }
      ],

      // --- Prettier integration ---
      'prettier/prettier': 'warn'
    }
  },

  // Disable conflicting rules from all shareable configs
  prettier,

  // Global ignores (flat config replacement for .eslintignore)
  globalIgnores(['**/node_modules/**', '.next/**', 'out/**', 'build/**', 'next-env.d.ts'])
]);

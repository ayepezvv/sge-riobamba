const _url = process.env.NEXT_PUBLIC_API_URL;
if (!_url) {
  throw new Error(
    '[SGE] La variable de entorno NEXT_PUBLIC_API_URL no está definida. ' +
    'Configúrala en .env.local antes de iniciar la aplicación.'
  );
}
export const API_BASE_URL: string = _url;

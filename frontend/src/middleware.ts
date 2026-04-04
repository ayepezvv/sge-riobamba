import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Rutas que NO requieren autenticación
const RUTAS_PUBLICAS = ['/login', '/register', '/forgot-password'];

// Prefijos de rutas del dashboard que requieren token
const PREFIJOS_PROTEGIDOS = [
  '/(dashboard)',
  '/contabilidad',
  '/presupuesto',
  '/tesoreria',
  '/financiero',
  '/rrhh',
  '/usuarios',
  '/roles',
  '/contratacion',
  '/bodega',
  '/administrativo',
  '/informatica',
  '/catastro',
  '/dashboard',
];

function estaProtegida(pathname: string): boolean {
  if (RUTAS_PUBLICAS.some((pub) => pathname.startsWith(pub))) return false;
  return PREFIJOS_PROTEGIDOS.some((prefix) => pathname.startsWith(prefix));
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (!estaProtegida(pathname)) {
    return NextResponse.next();
  }

  // El token se almacena en localStorage (client-side), pero el middleware
  // corre en Edge Runtime. Verificamos la cookie 'serviceToken' que el
  // cliente puede escribir en login como respaldo server-side.
  const token =
    request.cookies.get('serviceToken')?.value ??
    request.headers.get('authorization')?.replace('Bearer ', '');

  if (!token) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('callbackUrl', pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  // Aplica el middleware a rutas del dashboard y módulos del SGE
  matcher: [
    '/dashboard/:path*',
    '/contabilidad/:path*',
    '/presupuesto/:path*',
    '/tesoreria/:path*',
    '/financiero/:path*',
    '/rrhh/:path*',
    '/usuarios/:path*',
    '/roles/:path*',
    '/contratacion/:path*',
    '/bodega/:path*',
    '/administrativo/:path*',
    '/informatica/:path*',
    '/catastro/:path*',
  ],
};

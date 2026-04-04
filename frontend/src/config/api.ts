const API_BASE_URL: string =
  (typeof process !== "undefined" && process.env?.NEXT_PUBLIC_API_URL) ||
  "http://192.168.1.15:8000";

export default API_BASE_URL;

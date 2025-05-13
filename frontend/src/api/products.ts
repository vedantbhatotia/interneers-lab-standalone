import { api } from "./setup";
export function listProducts(params?: any) {
  return api.get("products/", { params });
}

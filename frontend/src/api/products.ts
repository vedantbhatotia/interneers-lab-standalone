import { api } from "./setup";
export function listProducts(params?: any) {
  return api.get("products/", { params });
}
export function getProduct(productId: string) {
  return api.get(`products/${productId}`);
}

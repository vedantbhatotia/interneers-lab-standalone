import { api } from "./setup";
export function listProducts(params?: any) {
  return api.get("products/", { params });
}
export function getProduct(productId: string) {
  return api.get(`products/${productId}`);
}
export function updateProduct(productId: string, payload: any) {
  return api.put(`products/${productId}/`, payload);
}
export function deleteProduct(productId: string) {
  return api.delete(`products/${productId}/`);
}

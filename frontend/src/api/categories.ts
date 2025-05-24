import { api } from "./setup";

export function listCategories() {
  return api.get("categories/");
}
export function getCategory(categoryId: string) {
  return api.get(`categories/${categoryId}/`);
}

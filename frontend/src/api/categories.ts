import { api } from "./setup";

export function listCategories() {
  return api.get("categories/");
}

export interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
  description: string;
}

export const products: Product[] = [
  {
    id: 1,
    name: "Widget A",
    price: 9.99,
    stock: 100,
    description: "A basic widget.",
  },
  {
    id: 2,
    name: "Widget B",
    price: 19.99,
    stock: 50,
    description: "A premium widget.",
  },
  {
    id: 3,
    name: "Widget C",
    price: 14.99,
    stock: 75,
    description: "A mid-range widget.",
  },
];

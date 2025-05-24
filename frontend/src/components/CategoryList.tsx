import React, { useState } from "react";
import { CategoryCard } from "./Category Card";

type Category = {
  id: string;
  title: string;
  description: string;
};

type Props = {
  categories: Category[];
};

export const CategoryList = ({ categories }: Props) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
      {categories.map((cat) => (
        <CategoryCard
          key={cat.id}
          category={cat}
          expanded={cat.id === expandedId}
          onClick={() =>
            setExpandedId((prev) => (prev === cat.id ? null : cat.id))
          }
        />
      ))}
    </div>
  );
};

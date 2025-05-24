import React from "react";
import { useNavigate } from "react-router-dom";

type Category = {
  id: string;
  title: string;
  description: string;
};

type Props = {
  category: Category;
  expanded: boolean;
  onClick: () => void;
};

export const CategoryCard = ({ category, expanded, onClick }: Props) => {
  const navigate = useNavigate();

  const handleClick = () => {
    onClick();
    navigate(`/categories/${category.id}`);
  };

  return (
    <div
      onClick={handleClick}
      className={`border rounded-lg p-4 cursor-pointer transition-shadow ${
        expanded ? "shadow-lg bg-gray-100" : "hover:shadow-md bg-white"
      }`}
    >
      <h3 className="text-lg font-semibold text-gray-800">{category.title}</h3>
      <p className="text-gray-600 text-sm mt-1">{category.description}</p>
      {expanded && <p className="mt-2 text-gray-700 text-sm"></p>}
    </div>
  );
};

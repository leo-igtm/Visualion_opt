import Link from "next/link";
import { ReactNode } from "react";

interface ModuleCardProps {
  title: string;
  description: string;
  icon: ReactNode;
  href: string;
  color: "blue" | "indigo" | "green" | "orange" | "purple" | "pink";
}

const colorVariants = {
  blue: "border-blue-600/30 hover:bg-blue-600/10 hover:border-blue-400/50",
  indigo: "border-indigo-600/30 hover:bg-indigo-600/10 hover:border-indigo-400/50",
  green: "border-green-600/30 hover:bg-green-600/10 hover:border-green-400/50",
  orange: "border-orange-600/30 hover:bg-orange-600/10 hover:border-orange-400/50",
  purple: "border-purple-600/30 hover:bg-purple-600/10 hover:border-purple-400/50",
  pink: "border-pink-600/30 hover:bg-pink-600/10 hover:border-pink-400/50",
};

const badgeColors = {
  blue: "bg-blue-600/20 text-blue-300",
  indigo: "bg-indigo-600/20 text-indigo-300",
  green: "bg-green-600/20 text-green-300",
  orange: "bg-orange-600/20 text-orange-300",
  purple: "bg-purple-600/20 text-purple-300",
  pink: "bg-pink-600/20 text-pink-300",
};

export default function ModuleCard({
  title,
  description,
  icon,
  href,
  color,
}: ModuleCardProps) {
  return (
    <Link href={href}>
      <div
        className={`bg-gray-900 p-6 rounded-2xl shadow-md border border-gray-800 transition-all duration-300 cursor-pointer hover:shadow-lg ${colorVariants[color]}`}
      >
        <div className="flex items-start justify-between mb-4">
          <div className={`text-4xl ${badgeColors[color]} p-3 rounded-lg`}>
            {icon}
          </div>
        </div>

        <h3 className="text-xl font-bold text-gray-100 mb-2">{title}</h3>
        <p className="text-gray-400 text-sm mb-4 leading-relaxed">
          {description}
        </p>

        <div className="flex items-center text-sm font-medium text-gray-300 hover:text-gray-100 transition-colors">
          Ver módulo
          <span className="ml-2">→</span>
        </div>
      </div>
    </Link>
  );
}

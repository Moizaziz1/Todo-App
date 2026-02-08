"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signOut } from "@/lib/auth-client";

interface SignOutButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function SignOutButton({ className, children }: SignOutButtonProps) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSignOut = () => {
    setIsLoading(true);

    // Clear authentication tokens from localStorage
    signOut();

    // Redirect to sign-in page
    router.push("/sign-in");

    setIsLoading(false);
  };

  return (
    <button
      onClick={handleSignOut}
      disabled={isLoading}
      className={className || "px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 disabled:opacity-50"}
    >
      {isLoading ? "Signing out..." : children || "Sign out"}
    </button>
  );
}
